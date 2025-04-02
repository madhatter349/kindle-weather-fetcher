import asyncio
from playwright.async_api import async_playwright

URL = "https://kindle.hrincar.eu/weather/index.html?city=&lat=40.785027&lon=-73.974510&utcOffset=&lang=en&rotation=none&units=imperial&tempType=actual&night=off&appId="
OUTPUT_FILE = "weather.png"
VIEWPORT = {"width": 800, "height": 600}

async def capture_kindle_image():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        await page.set_viewport_size(VIEWPORT)
        await page.goto(URL, wait_until="networkidle")
        await page.screenshot(path=OUTPUT_FILE)
        await browser.close()
        print(f"Screenshot saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(capture_kindle_image())
