import mysql.connector
import random
import time
from multiprocessing import Pool
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine, text

# ==========================================
# 1. CẤU HÌNH KẾT NỐI DATABASE
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'python_user',
    'password': '123456',
    'database': 'school_db'
}


# ==========================================
# 2. HÀM SINH DỮ LIỆU GIẢ (DATA GENERATOR)
# ==========================================
def generate_data_chunk(size):

    ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi"]
    dem = ["Văn", "Thị", "Anh", "Minh", "Đức", "Hoàng", "Ngọc", "Gia"]
    ten = ["Hùng", "Hoa", "Lan", "Tuấn", "Dũng", "Linh", "Thành", "Phương", "Quân"]
    lops = ["CNTT1", "KTPM2", "HTTT1", "KHMT3", "DTVT1", "ATTT2"]

    data = []
    for _ in range(size):
        row = (
            f"MSV_{random.randint(1000000, 9999999)}",
            f"{random.choice(ho)} {random.choice(dem)} {random.choice(ten)}",
            random.choice(lops),
            random.uniform(10_000_000, 50_000_000),
            random.choice(["Nam", "Nu"]),
            f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            random.uniform(0, 5_000_000),
            random.randint(1, 8)
        )
        data.append(row)
    return data


# ==========================================
# 3. WORKER INSERT (ĐA LUỒNG )
# ==========================================
def insert_worker(num_records):
    """Hàm này chạy trên từng nhân CPU để insert dữ liệu song song"""
    conn = None
    cursor = None
    try:
        # Mỗi process phải tự tạo kết nối riêng
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        data = generate_data_chunk(num_records)

        sql = """INSERT INTO Students
                     (MSV, HovaTen, Lop, HocPhi, GioiTinh, NgayNop, HocBong, KyHoc)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.executemany(sql, data)
        conn.commit()

    except Exception as err:
        print(f"Lỗi Insert: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ==========================================
# 4. HÀM PHÂN TÍCH (Dùng SQLAlchemy để fix lỗi Pandas)
# ==========================================
def run_analysis():
    print("\n--- Đang thực hiện truy vấn và phân tích dữ liệu ---")

    # Tạo chuỗi kết nối chuẩn SQLAlchemy: mysql+mysqlconnector://user:pass@host/db
    conn_str = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    engine = create_engine(conn_str)

    start_q = time.time()

    # Sử dụng 'with engine.connect()' để quản lý kết nối an toàn
    with engine.connect() as conn:
        print("1. Đang lấy Top 10 học phí cao nhất...")
        # Pandas đọc qua SQLAlchemy connection
        top10_df = pd.read_sql("SELECT HovaTen, HocPhi FROM Students ORDER BY HocPhi DESC LIMIT 10", conn)

        print("2. Đang tính tổng doanh thu...")
        # Dùng text() bọc câu query SQL
        result = conn.execute(text("SELECT SUM(HocPhi - HocBong) FROM Students"))
        revenue = result.scalar()

        print("3. Đang thống kê giới tính...")
        gender_df = pd.read_sql("SELECT GioiTinh, COUNT(*) as Count FROM Students GROUP BY GioiTinh", conn)

    print(f"-> Thời gian truy vấn xong: {time.time() - start_q:.2f} giây")
    return top10_df, revenue, gender_df


# ==========================================
# 5. CHƯƠNG TRÌNH CHÍNH (MAIN ENTRY POINT)
# ==========================================
if __name__ == '__main__':
    # CẤU HÌNH SỐ LƯỢNG
    TOTAL_RECORDS = 5_000_000
    CHUNK_SIZE = 25_000  # Mỗi lần insert 25k dòng
    NUM_PROCESSES = 8  # Số luồng CPU chạy song song

    num_chunks = TOTAL_RECORDS // CHUNK_SIZE

    print(f"=== BẮT ĐẦU CHƯƠNG TRÌNH ===")
    print(f"Mục tiêu: Insert {TOTAL_RECORDS:,} bản ghi.")

    # --- GIAI ĐOẠN 1: INSERT DATA ---
    start_time = time.time()

    # Khởi tạo Pool đa luồng
    with Pool(processes=NUM_PROCESSES) as pool:
        pool.map(insert_worker, [CHUNK_SIZE] * num_chunks)

    duration = time.time() - start_time
    print(f"\n[DONE] Hoàn thành Insert trong: {duration:.2f} giây")
    print(f"Tốc độ trung bình: {TOTAL_RECORDS / duration:,.0f} bản ghi/giây")

    # --- GIAI ĐOẠN 2: PHÂN TÍCH ---
    top10, rev, gender = run_analysis()

    print(f"\n=== KẾT QUẢ BÁO CÁO ===")
    print(f"Tổng doanh thu thực thu: {rev:,.0f} VND")
    print(f"Thống kê giới tính:\n{gender}")

    # --- GIAI ĐOẠN 3: VẼ BIỂU ĐỒ ---
    print("\nĐang hiển thị biểu đồ...")

    # Biểu đồ cột
    fig1 = go.Figure(data=[go.Bar(x=top10['HovaTen'], y=top10['HocPhi'], marker_color='indianred')])
    fig1.update_layout(title="Top 10 Sinh viên có Học phí cao nhất", xaxis_title="Họ tên", yaxis_title="Học phí")
    fig1.show()

    # Biểu đồ tròn
    fig2 = go.Figure(data=[go.Pie(labels=gender['GioiTinh'], values=gender['Count'], hole=.3)])
    fig2.update_layout(title="Tỷ lệ Giới tính Sinh viên")
    fig2.show()