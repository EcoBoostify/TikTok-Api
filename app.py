import asyncio
import requests
import os
from TikTokApi import TikTokApi
from aiohttp import web
from datetime import datetime

ms_token = os.getenv("MS_TOKEN", None)
endpoint = os.getenv("API_ENDPOINT", None)
CHROMIUM_EXECUTABLE_PATH = os.getenv("CHROMIUM_EXECUTABLE_PATH", "/app/browsers/chromium-1091/chrome-linux/chrome/chromium-1091/chrome-linux/chrome")

api = TikTokApi()

health_status = {
    "last_run": None,
    "last_status": "Not run yet",
    "last_error": None
}

# Tạo function lấy thông tin người dùng và cookies
async def get_user_and_cookies():
    if not api.sessions:
        await api.create_sessions(
            headless=True,
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=300,
            executable_path=CHROMIUM_EXECUTABLE_PATH
        )

    # Lấy thông tin người dùng
    user = api.user(username="thuuyenjenabyu")
    user_data = await user.info()

    # Lấy cookies
    cookies = await api.get_cookies()

    # Trả về user_data và cookies
    return user_data, cookies

# Function gửi cookies đến một endpoint
def send_cookies_to_endpoint(cookies):
    headers = {"Content-Type": "application/json"}
    payload = {
        "cookies": cookies
    }
    print(payload)
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            print("Cookies sent successfully!")
            return "success"
        else:
            print(f"Failed to send cookies, status code: {response.status_code}")
            return f"failed (status code: {response.status_code})"
    except Exception as e:
        print(f"Exception while sending cookies: {e}")
        return f"exception: {e}"

# Hàm chính chạy mỗi phút
async def run_service():
    while True:
        try:
            # Lấy thông tin người dùng và cookies
            user_data, cookies = await get_user_and_cookies()

            # Gửi cookies tới endpoint
            status = send_cookies_to_endpoint(cookies)

            # Cập nhật trạng thái health
            health_status["last_run"] = datetime.utcnow().isoformat() + "Z"
            health_status["last_status"] = status
            health_status["last_error"] = None
        except Exception as e:
            print(f"Error in run_service: {e}")
            health_status["last_status"] = "error"
            health_status["last_error"] = str(e)

        # Đợi 1 phút
        await asyncio.sleep(60)

# Handler cho endpoint /health
async def handle_health(request):
    return web.json_response({
        "status": "ok" if health_status["last_status"] != "error" else "error",
        "last_run": health_status["last_run"],
        "last_status": health_status["last_status"],
        "last_error": health_status["last_error"]
    })

# Function để khởi động web server
async def start_web_server():
    app = web.Application()
    app.router.add_get('/healthcheck', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print("Health check server started on port 8080")

# Main coroutine để chạy cả service và web server
async def main():
    await asyncio.gather(
        run_service(),
        start_web_server(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service stopped by user")
