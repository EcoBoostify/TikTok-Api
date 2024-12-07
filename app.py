import asyncio
import requests
import os
import logging
from TikTokApi import TikTokApi
from aiohttp import web
from datetime import datetime

# Initialize Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

ms_token = os.getenv("MS_TOKEN", None)
endpoint = os.getenv("API_ENDPOINT", "https://api-dev.ecoboostify.com/reel-setting")
CHROMIUM_EXECUTABLE_PATH = '/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome'
ms = ["1jP0CknhzaZ-L7FfDyWzhBudsayDGKfssuaeSlr6bp8ip2iMUtpxkTSp8qfRmLYIQk7n2kz-r-sU8tAlMey0GEAiXIuP_-JFsXK77DZKSO7w2QY2W-EgBVtsWWxyk1h7oJGKCOu3MpGDDuk="]
api = TikTokApi()

health_status = {
    "last_run": None,
    "last_status": "Not run yet",
    "last_error": None
}

# Function to get user info and cookies
async def get_user_and_cookies():
    logger.info("Starting to get user info and cookies")
    if not api.sessions:
        logger.info("No existing sessions. Creating new session.")
        logger.info("Path: " + CHROMIUM_EXECUTABLE_PATH)
        await api.create_sessions(
            ms_tokens=ms,
            num_sessions=1,
            sleep_after=10,
            executable_path=CHROMIUM_EXECUTABLE_PATH,
            browser="chromium"
        )
        logger.info("Session created successfully.")

    try:
        # Get user information
        logger.info("Fetching user information for username 'thuuyenjenabyu'")
        user = api.user(username="thuuyenjenabyu")
        user_data = await user.info()
        logger.debug(f"User data retrieved: {user_data}")

        # Get cookies
        logger.info("Fetching cookies")
        cookies = await api.get_cookies()
        logger.debug(f"Cookies retrieved: {cookies}")

        return user_data, cookies
    except Exception as e:
        logger.error(f"Error in get_user_and_cookies: {e}", exc_info=True)
        raise

# Function to send cookies to an endpoint
def send_cookies_to_endpoint(cookies):
    logger.info("Preparing to send cookies to the endpoint")
    headers = {"Content-Type": "application/json"}
    payload = {
        "cookies": cookies
    }
    logger.debug(f"Payload: {payload}")
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info("Cookies sent successfully!")
            return "success"
        else:
            logger.warning(f"Failed to send cookies, status code: {response.status_code}")
            return f"failed (status code: {response.status_code})"
    except Exception as e:
        logger.error(f"Exception while sending cookies: {e}", exc_info=True)
        return f"exception: {e}"

# Main service function that runs every minute
async def run_service():
    logger.info("Service started, will run every minute.")
    while True:
        try:
            logger.info("Running service cycle")
            # Get user data and cookies
            user_data, cookies = await get_user_and_cookies()

            # Send cookies to endpoint
            status = send_cookies_to_endpoint(cookies)

            # Update health status
            health_status["last_run"] = datetime.utcnow().isoformat() + "Z"
            health_status["last_status"] = status
            health_status["last_error"] = None
            logger.info(f"Service cycle completed successfully. Status: {status}")
        except Exception as e:
            logger.error(f"Error in run_service: {e}", exc_info=True)

            # Check if the error is a timeout
            if "Timeout" in str(e):
                try:
                    logger.warning("Timeout exceeded. Attempting to close sessions.")
                    await api.close_sessions()
                    logger.info("Sessions closed successfully.")
                except Exception as close_e:
                    logger.error(f"Error while closing sessions: {close_e}", exc_info=True)

            health_status["last_status"] = "error"
            health_status["last_error"] = str(e)

        # Wait for 1 minute before the next cycle
        logger.info("Waiting for 60 seconds before the next cycle")
        await asyncio.sleep(60)

# Handler for the /healthcheck endpoint
async def handle_health(request):
    logger.info("Received healthcheck request")
    return web.json_response({
        "status": "ok" if health_status["last_status"] != "error" else "error",
        "last_run": health_status["last_run"],
        "last_status": health_status["last_status"],
        "last_error": health_status["last_error"]
    })

# Function to start the web server
async def start_web_server():
    logger.info("Starting web server for healthcheck")
    app = web.Application()
    app.router.add_get('/healthcheck', handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Health check server started on port {port}")

# Main coroutine to run both the service and web server
async def main():
    logger.info("Main coroutine started")
    await asyncio.gather(
        run_service(),
        start_web_server(),
    )

if __name__ == "__main__":
    logger.info("Starting the application")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
