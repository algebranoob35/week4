# Student Data Analytics & Simulation

Dự án mô phỏng quy trình xử lý dữ liệu lớn (Big Data) với Python và MySQL. Chương trình thực hiện sinh giả lập dữ liệu sinh viên, insert đa luồng vào database và thực hiện phân tích, trực quan hóa.

## 🚀 Tính năng chính

1.  Data Generation: Sinh tự động dữ liệu giả (Mock data) cho sinh viên (Họ tên, Lớp, Học phí, v.v.).
2.  Multiprocessing Insert: Sử dụng kỹ thuật đa luồng (`multiprocessing.Pool`) để tối ưu tốc độ insert dữ liệu vào MySQL (Mục tiêu ~5 triệu bản ghi).
3.  Data Analysis: Sử dụng `SQLAlchemy` và `Pandas` để truy vấn và tổng hợp dữ liệu.
4.  Visualization: Vẽ biểu đồ tương tác bằng `Plotly` (Biểu đồ Top 10 học phí & Tỷ lệ giới tính).

## 🛠 Cài đặt

1. Clone repository:
   ```bash
   git clone [https://github.com/your-username/repo-name.git](https://github.com/your-username/repo-name.git)
