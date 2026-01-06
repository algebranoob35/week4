import mysql.connector
import random
import time
from multiprocessing import Pool
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine, text
# 1. Cấu hình kết nối
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '280704',
    'database': 'school_db'
}


# 2. Hàm sinh dữ liệu ngẫu nhiên theo lô (Bulk)
def generate_data_chunk(size):
    ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi"]
    dem = ["Văn", "Thị", "Anh", "Minh", "Đức", "Hoàng", "Ngọc"]
    ten = ["Hùng", "Hoa", "Lan", "Tuấn", "Dũng", "Linh", "Thành", "Phương"]
    lops = ["CNTT1", "KTPM2", "HTTT1", "KHMT3", "DTVT1"]

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


# 3. Worker xử lý Insert
def insert_worker(num_records):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    data = generate_data_chunk(num_records)

    sql = "INSERT INTO Students (MSV, HovaTen, Lop, HocPhi, GioiTinh, NgayNop, HocBong, KyHoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()
    conn.close()


# 4. Các hàm chức năng
def run_queries():
    conn = mysql.connector.connect(**DB_CONFIG)

    # Top 10 học phí
    top10 = pd.read_sql("SELECT HovaTen, HocPhi FROM Students ORDER BY HocPhi DESC LIMIT 10", conn)

    # Doanh thu (Doanh thu = Học phí - Học bổng)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(HocPhi - HocBong) FROM Students")
    revenue = cursor.fetchone()[0]

    # Số lượng theo giới tính
    gender_count = pd.read_sql("SELECT GioiTinh, COUNT(*) as Count FROM Students GROUP BY GioiTinh", conn)

    conn.close()
    return top10, revenue, gender_count


if __name__ == '__main__':
    # THỰC HIỆN INSERT 5 TRIỆU BẢN GHI
    total_records = 5_000_000
    chunk_size = 20_000  # Mỗi lần insert 20k dòng
    num_chunks = total_records // chunk_size

    print("Bắt đầu Insert đa luồng...")
    start_time = time.time()

    # Sử dụng Pool để tận dụng toàn bộ nhân CPU
    with Pool(processes=8) as pool:
        pool.map(insert_worker, [chunk_size] * num_chunks)

    print(f"Hoàn thành Insert trong: {time.time() - start_time:.2f} giây")

    # TRUY VẤN DỮ LIỆU
    top10, rev, gender = run_queries()
    print(f"Tổng doanh thu nhà trường: {rev:,.0f} VND")

    # VẼ BIỂU ĐỒ BẰNG PLOTLY
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top10['HovaTen'], y=top10['HocPhi'], name='Học phí Top 10'))
    fig.update_layout(title="Top 10 Sinh viên học phí cao nhất")
    fig.show()