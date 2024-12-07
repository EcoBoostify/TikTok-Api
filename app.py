import asyncio
import requests
from TikTokApi import TikTokApi

# Đặt ms_token của bạn ở đây
ms_token = "Mw8mgiotxB_Yx9kYdIDwyoYgVt3o_yxirLVH4o9fnbWlh8ODp-LzcYdp9xj2cljPl06SSQ-qDGF1IEx94kDOW4wXG5RE3mnoMIJ1OZoWX0SWGoeO7GRy2yE8ahCs3c4kc-Fg8gE1_pmO"

# Khởi tạo TikTok API
api = TikTokApi()

# Tạo function lấy thông tin người dùng và cookies
async def get_user_and_cookies():
    if not api.sessions:
        await api.create_sessions(
            headless=True,
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=300,
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
    endpoint = "https://ecoboostify.ngrok.dev/reel-setting"  # Thay thế với endpoint của bạn
    headers = {"Content-Type": "application/json"}
    payload = {
        "cookies": cookies
    }
    print(payload)
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        print("Cookies sent successfully!")
    else:
        print(f"Failed to send cookies, status code: {response.status_code}")

# Hàm chính chạy mỗi phút
async def run_service():
    while True:
        # Lấy thông tin người dùng và cookies
        user_data, cookies = await get_user_and_cookies()

        # Gửi cookies tới endpoint
        send_cookies_to_endpoint(cookies)

        # Đợi 1 phút
        await asyncio.sleep(60)

if __name__ == "__main__":
    # Chạy service
    asyncio.run(run_service())
