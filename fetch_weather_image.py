import requests

url = "https://kindle-weather-9fnr.onrender.com/screenshot"  # your FastAPI screenshot endpoint
output_path = "weather.png"

response = requests.get(url)

if response.status_code == 200:
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("Image saved successfully.")
else:
    print(f"Failed to fetch image. Status code: {response.status_code}")
