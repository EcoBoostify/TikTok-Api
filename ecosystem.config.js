module.exports = {
    apps: [
        {
            name: 'python-app',     // Tên ứng dụng
            script: 'xvfb-run',     // Chạy xvfb-run
            args: 'python3 /path/to/your/venv/bin/app.py',  // Thêm đường dẫn đúng đến script Python
            interpreter: '/path/to/your/venv/bin/python3', // Sử dụng Python trong virtual environment
            instances: 1,           // Chạy 1 instance (hoặc nhiều nếu cần)
            autorestart: true,      // Tự động khởi động lại khi ứng dụng gặp sự cố
            watch: false,           // Không theo dõi thay đổi mã nguồn
            max_memory_restart: '1G',  // Restart nếu sử dụng bộ nhớ vượt quá 1GB
        }
    ]
};
