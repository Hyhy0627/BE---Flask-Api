#!/bin/bash
set -e

# Chờ MySQL khởi động (nếu sử dụng MySQL)
# Không cần thiết cho SQLite

# Tạo thư mục instance nếu chưa tồn tại
mkdir -p /app/instance

# Chạy migrate và tạo bảng
python manage.py

# Khởi động ứng dụng
exec python app.py
