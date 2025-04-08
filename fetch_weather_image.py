import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import io

URL = "https://kindle.hrincar.eu/weather/index.html?city=&lat=40.785027&lon=-73.974510&utcOffset=&lang=en&rotation=none&units=imperial&tempType=actual&night=off&appId="
OUTPUT_FILE = "bg_ss00.png"
KINDLE_SIZE = (1072, 1448)  # Kindle screen size in portrait

async def capture_kindle_image():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()

        # Viewport should match expected content layout (landscape shape)
        await page.set_viewport_size({"width": 1448, "height": 1072})
        await page.goto(URL, wait_until="networkidle")

        # Capture full page screenshot
        screenshot_bytes = await page.screenshot(type="png", full_page=True)
        await browser.close()

        # Open with Pillow
        img = Image.open(io.BytesIO(screenshot_bytes)).convert("L")  # grayscale

        # Rotate to match Kindle portrait orientation
        img = img.rotate(90, expand=True)

        # Resize to exact Kindle resolution
        img = img.resize(KINDLE_SIZE, Image.LANCZOS)

        img.save(OUTPUT_FILE, format="PNG")
        print(f"Saved rotated and resized Kindle image as {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(capture_kindle_image())
