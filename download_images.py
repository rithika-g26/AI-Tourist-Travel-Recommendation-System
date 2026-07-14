import os
import requests
import pandas as pd
from urllib.parse import quote

# Load CSV
image_df = pd.read_csv("database/place_images_final.csv")

# Create image folder
os.makedirs("static/images/places", exist_ok=True)

def download_image(place_name, filename):

    try:
        # Wikipedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(place_name)}"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ No Wikipedia page: {place_name}")
            return

        data = response.json()

        if "thumbnail" not in data:
            print(f"⚠ No image available: {place_name}")
            return

        image_url = data["thumbnail"]["source"]

        img = requests.get(image_url, timeout=10)

        save_path = os.path.join("static/images/places", filename)

        with open(save_path, "wb") as f:
            f.write(img.content)

        print(f"✅ Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Error downloading {place_name}: {e}")


# Download images
for _, row in image_df.iterrows():
    download_image(row["Name"], row["Image"])

print("\n🎉 Image download process completed!")