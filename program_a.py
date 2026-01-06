# program_a.py

def ghi_file():
    print("--- NHẬP THÔNG TIN TÀI KHOẢN ---")
    username = input("Nhập username: ")
    password = input("Nhập password: ")
    email = input("Nhập email: ")
    fullname = input("Nhập Họ và Tên: ")
    dob = input("Nhập Ngày/Tháng/Năm sinh (vd: 1/1/2000): ")

    # Tạo chuỗi định dạng csv
    line = f"{username},{password},{email},{fullname},{dob}\n"

    # Mở file với mode 'a' (append) để ghi nối tiếp, không xóa dữ liệu cũ
    try:
        with open('account.txt', 'a', encoding='utf-8') as f:
            f.write(line)
        print("-> Đã ghi thông tin vào file account.txt thành công!")
    except Exception as e:
        print(f"Có lỗi khi ghi file: {e}")

if __name__ == "__main__":
    while True:
        ghi_file()
        cont = input("Bạn có muốn nhập tiếp không? (y/n): ")
        if cont.lower() != 'y':
            break