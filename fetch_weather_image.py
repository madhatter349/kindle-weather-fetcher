import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import io

URL = "https://kindle.hrincar.eu/weather/index.html?city=&lat=40.785027&lon=-73.974510&utcOffset=&lang=en&rotation=none&units=imperial&tempType=actual&night=off&appId="
OUTPUT_FILE = "bg_ss00.png"
VIEWPORT = {"width": 800, "height": 600}  # You can leave this as-is

TARGET_SIZE = (768, 1024)  # Kindle screensaver size (portrait)

async def capture_kindle_image():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        await page.set_viewport_size(VIEWPORT)
        await page.goto(URL, wait_until="networkidle")

        # Capture screenshot as bytes
        screenshot_bytes = await page.screenshot(type="png")
        await browser.close()

        # Convert and resize with Pillow
        img = Image.open(io.BytesIO(screenshot_bytes))
        img = img.convert("L")  # 8-bit grayscale
        img = img.resize(TARGET_SIZE)  # Resize to Kindle resolution

        img.save(OUTPUT_FILE, format="PNG")
        print(f"Kindle-ready image saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(capture_kindle_image())
