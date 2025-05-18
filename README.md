#  DCrossFitness

"Website quản lý phòng gym được xây dựng bằng Flask, với hỗ trợ giao diện, thanh toán PayPal."

---

##  Tính năng chính

- Đăng ký/đăng nhập tài khoản
- Giao diện tĩnh với CSS/JS
- Tương tác với cơ sở dữ liệu MySQL
- Tích hợp PayPal REST API để thanh toán
- Tự động gửi thông báo qua Flash
- Mã hóa mật khẩu với `werkzeug.security`


### Yêu cầu hệ thống

- Python 3.10 hoặc mới hơn
- MySQL Server
- Trình duyệt hiện đại

## Hướng dẫn cài đặt

Danh sách các thư viện cần thiết:

Flask
python-dotenv
Flask-MySQLdb
paypalrestsdk
requests
pyzbar
Pillow
Werkzeug``


Cài đặt nhanh bằng pip:

```bash
pip install Flask python-dotenv Flask-MySQLdb paypalrestsdk requests pyzbar Pillow Werkzeug

```

## Thiết lập file `.env`

Tạo file `.env` với các biến sau (Phần trống tự thiết lập):

```env
SECRET_KEY=rest
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DB=gymdb


PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
```

##  Cấu trúc dự án

```
DCrossFitness/
│
├── static/
│   ├── images/
│   ├── form.css
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── *.html
│
├── extensions.py
├── main.py
├── models.py
├── routes.py
├── .env
├── Dump20250518.sql
└── README.md
```

## Tích hợp PayPal

Sử dụng thư viện `paypalrestsdk`

- Tạo ứng dụng tại https://developer.paypal.com/
- Lấy `Client ID` và `Secret`
- Đặt chúng vào `.env`


## MySql Server

Query tạo Schema trong file Dump20250518.sql
