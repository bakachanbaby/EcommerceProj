# Food Store - Website Bán Đồ Ăn

Food Store là một website bán đồ ăn được xây dựng bằng Django, cho phép người dùng dễ dàng duyệt và đặt món ăn trực tuyến.

## Tính Năng

### Người Dùng
- Đăng ký/Đăng nhập tài khoản
- Xem danh sách sản phẩm theo danh mục
- Xem chi tiết sản phẩm
- Thêm sản phẩm vào giỏ hàng
- Quản lý giỏ hàng (thêm, sửa số lượng, xóa)
- Đặt hàng và theo dõi đơn hàng
- Xem lịch sử đơn hàng

### Giao Diện
- Thiết kế responsive, tương thích mobile
- Giao diện người dùng thân thiện
- Hiệu ứng chuyển động mượt mà
- Theme màu gradient đẹp mắt

## Công Nghệ Sử Dụng

### Backend
- Django 5.1.5
- SQLite Database
- Django Authentication System

### Frontend
- HTML5/CSS3
- Bootstrap 5
- Font Awesome Icons
- Animate.css

## Cài Đặt

1. Clone repository:
bash
git clone <repository-url>
2. Tạo và kích hoạt môi trường ảo:
bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
3. Cài đặt các dependencies:
bash
pip install -r requirements.txt
4. Thực hiện migrate database:
bash
python manage.py migrate
5. Tạo tài khoản admin:
bash
python manage.py createsuperuser
6. Chạy development server:
bash
python manage.py runserver
## Cấu Trúc Database

### Category (Danh Mục)
- name: Tên danh mục
- description: Mô tả danh mục

### Product (Sản Phẩm)
- name: Tên sản phẩm
- description: Mô tả sản phẩm
- price: Giá
- image: Hình ảnh
- category: Danh mục (ForeignKey)
- available: Trạng thái còn hàng

### Order (Đơn Hàng)
- user: Người đặt hàng
- created_at: Ngày tạo
- status: Trạng thái đơn hàng
- shipping_address: Địa chỉ giao hàng
- phone: Số điện thoại
- total_amount: Tổng tiền

### OrderItem (Chi Tiết Đơn Hàng)
- order: Đơn hàng (ForeignKey)
- product: Sản phẩm (ForeignKey)
- quantity: Số lượng
- price: Giá tại thời điểm đặt

## Tác Giả
[Tên của bạn]

## License
MIT License
