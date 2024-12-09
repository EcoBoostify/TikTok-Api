module.exports = {
    apps: [
        {
            name: 'python-app',   // Tên ứng dụng
            script: 'xvfb-run',   // Chạy xvfb-run
            args: 'python3 app.py', // Thêm lệnh chạy ứng dụng Python
            interpreter: 'bash',  // Dùng bash để chạy lệnh
            instances: 1,         // Số lượng instance, nếu bạn muốn chạy nhiều tiến trình thì chỉnh sửa ở đây
            autorestart: true,    // Tự động khởi động lại nếu ứng dụng gặp sự cố
            watch: false,         // Không theo dõi thay đổi mã nguồn
            max_memory_restart: '1G',  // Restart nếu tiêu thụ bộ nhớ vượt quá 1GB
        }
    ]
};
