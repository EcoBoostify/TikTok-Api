module.exports = {
    apps: [
        {
            name: 'ecobrowser',                        // Tên ứng dụng của bạn
            script: 'xvfb-run',                        // Chạy xvfb-run
            args: 'python3 app.py',                    // Đường dẫn tới file Python của bạn
            interpreter: 'venv/bin/python3',           // Đảm bảo sử dụng Python trong virtual environment (nếu có)
            instances: 1,                              // Số lượng instance, bạn có thể thay đổi nếu cần
            autorestart: true,                         // Tự động khởi động lại khi ứng dụng gặp sự cố
            watch: false,                              // Không theo dõi thay đổi mã nguồn
            max_memory_restart: '1G',                  // Restart nếu bộ nhớ vượt quá 1GB
            env: {
                DISPLAY: ':99'                         // Đặt biến môi trường DISPLAY cho Xvfb
            },
            error_file: './logs/ecobrowser-error.log', // Đường dẫn lưu log lỗi
            out_file: './logs/ecobrowser-out.log',     // Đường dẫn lưu log đầu ra
            log_date_format: 'YYYY-MM-DD HH:mm:ss'    // Định dạng ngày giờ trong log
        }
    ]
};
