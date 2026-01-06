from flask import Flask, jsonify, request

# Khởi tạo ứng dụng Flask
app = Flask(__name__)


# --- VÍ DỤ 1: API GET cơ bản (Hello World) ---
# Endpoint: http://127.0.0.1:5000/
@app.route('/', methods=['GET'])
def home():
    data = {
        "message": "Chào mừng đến với Flask API",
        "status": "success"
    }
    # jsonify giúp chuyển Python Dict thành JSON Response chuẩn
    return jsonify(data), 200


# --- VÍ DỤ 2: API GET có tham số (Dynamic Routing) ---
# Mục tiêu: Lấy thông tin user theo ID
# Endpoint: http://127.0.0.1:5000/user/123
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Giả lập database
    users_db = {
        1: "Nguyen Van A",
        2: "Tran Thi B"
    }

    name = users_db.get(user_id)

    if name:
        return jsonify({"id": user_id, "name": name}), 200
    else:
        return jsonify({"error": "Không tìm thấy user"}), 404


# --- VÍ DỤ 3: API POST nhận dữ liệu JSON ---
# Mục tiêu: Tạo mới một sản phẩm
# Endpoint: http://127.0.0.1:5000/product
@app.route('/product', methods=['POST'])
def create_product():
    # Lấy dữ liệu JSON client gửi lên
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Thiếu thông tin tên sản phẩm"}), 400

    product_name = data['name']
    price = data.get('price', 0)

    # Xử lý logic lưu vào DB ở đây...

    response_data = {
        "message": "Tạo sản phẩm thành công",
        "product": {
            "name": product_name,
            "price": price
        }
    }
    return jsonify(response_data), 201


# Chạy server
if __name__ == '__main__':
    app.run(debug=True)  # debug=True giúp tự reload khi sửa code