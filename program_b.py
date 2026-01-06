# program_b.py
import mysql.connector
from datetime import datetime


def insert_to_db():
    # 1. Kết nối đến MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Thay bằng user của bạn (thường là root)
            password="280704",  # Thay bằng password MySQL của bạn
            database="quanlytaikhoan"
        )
        cursor = conn.cursor()
        print("-> Kết nối CSDL thành công!")

        # 2. Đọc dữ liệu từ file
        with open('account.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            if line.strip():  # Kiểm tra dòng không rỗng
                # Tách chuỗi dựa trên dấu phẩy
                data = line.strip().split(',')

                # Kiểm tra đủ 5 trường dữ liệu để tránh lỗi index
                if len(data) == 5:
                    username = data[0]
                    password = data[1]
                    email = data[2]
                    fullname = data[3]
                    dob_raw = data[4]

                    # Chuyển đổi ngày sinh từ dd/mm/yyyy sang yyyy-mm-dd cho MySQL
                    try:
                        dob_obj = datetime.strptime(dob_raw, '%d/%m/%Y')
                        dob_mysql = dob_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Lỗi định dạng ngày ở dòng: {line.strip()}")
                        continue

                    # 3. Thực hiện Insert
                    sql = "INSERT INTO accounts (username, password, email, fullname, dob) VALUES (%s, %s, %s, %s, %s)"
                    val = (username, password, email, fullname, dob_mysql)
                    cursor.execute(sql, val)
                    count += 1

        # Lưu thay đổi (Commit)
        conn.commit()
        print(f"-> Đã import thành công {count} tài khoản vào Database.")

    except mysql.connector.Error as err:
        print(f"Lỗi kết nối MySQL: {err}")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file account.txt. Hãy chạy chương trình A trước.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("-> Đã đóng kết nối.")


if __name__ == "__main__":
    insert_to_db()