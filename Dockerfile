# Sử dụng ảnh Ubuntu làm ảnh cơ sở
FROM ubuntu

# Cập nhật và cài đặt các gói cần thiết
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Sao chép mã nguồn bot vào thư mục /app
COPY . /app

# Cài đặt các gói phụ thuộc cho bot
RUN pip3 install -r /app/requirements.txt

# Thiết lập biến môi trường cho bot
ENV BOT_TOKEN=''

# Thiết lập thư mục làm việc
WORKDIR /app

# Chạy bot
CMD ["python3", "stupidBOT.py"]
