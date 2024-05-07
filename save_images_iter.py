import os
import requests
from bs4 import BeautifulSoup
import regex 
import time
import datetime
import waybackpy 



def get_wayback_timestamps(url):
    try:
        response = requests.get(f"https://archive.org/wayback/available?url={url}")
        response.raise_for_status()
        data = response.json()
        return data['archived_snapshots']['closest']['timestamp']
        time.sleep(5)
    except requests.RequestException as e:
        print("Failed to fetch Wayback Machine data:", e)
        return None

# 

def get_all_wayback_timestamps(url):
    all_timestamps = []
    current_year = datetime.datetime.now().year

    # Iterate over years from 1996 to the current year
    for year in range(1996, current_year + 1):
        try:
            response = requests.get(f"https://archive.org/wayback/available?url={url}&timestamp={year}0101")
            response.raise_for_status()
            data = response.json()
            timestamp = data['archived_snapshots']['closest']['timestamp']
            all_timestamps.append(timestamp)
            time.sleep(5)
        except requests.RequestException as e:
            print(f"Failed to fetch Wayback Machine data for {year}:", e)
    
    return all_timestamps


def download_images_from_timestamp(archived_url, timestamp):
    try:
        # Construct URL for the given timestamp
        full_url = f"https://web.archive.org/web/{timestamp}/{archived_url}"

        # Fetch the archived webpage
        response = requests.get(full_url)
        response.raise_for_status()  # Raise HTTPError for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all area tags
        area_tags = soup.find_all('area')
        print(f"Found {len(area_tags)} area tags")

        # Create images folder if not exists
        if not os.path.exists('images'):
            os.makedirs('images')

        # Iterate over area tags and extract image URLs
        for index, area_tag in enumerate(area_tags):
            try:
                # Get image source URL
                img_url = area_tag.get('href')
                print(f"Processing image {index} from timestamp {timestamp}: {img_url}")
                img_url = regex.sub(r'web/\d{14}/https://bangla\.ganashakti\.co\.in', '', img_url)
                print(f"Processed image {index} from timestamp {timestamp}: {img_url}")
                if not img_url.startswith('http'):
                    # Handle relative URLs
                    img_url = f"https://bangla.ganashakti.co.in{img_url}"

                # Fetch the image
                img_response = requests.get(img_url)
                img_response.raise_for_status()  # Raise HTTPError for bad status codes

                # Save the image to the images folder
                with open(f'images/{timestamp}_ganashakti_image_{index}.jpg', 'wb') as img_file:
                    img_file.write(img_response.content)
                time.sleep(5)
            except Exception as e:
                print(f"Failed to process image: {img_url}")
                print(e)
    except requests.RequestException as e:
        print("Failed to fetch the webpage:", e)

# def main():
#     url = "https://bangla.ganashakti.co.in/"
#     timestamp = get_wayback_timestamps(url)
#     if timestamp:
#         download_images_from_timestamp(url, timestamp)
#     else:
#         print("Failed to get Wayback Machine timestamp.")

def main():

    from waybackpy import WaybackMachine

# Create a WaybackMachine object
    wb = WaybackMachine()

    url = "https://bangla.ganashakti.co.in/"

    # Retrieve all available timestamps for the URL
    timestamps = wb.get_timestamps(url)
    # Print the timestamps
    for timestamp in timestamps:
        print(timestamp)

    url = "https://bangla.ganashakti.co.in/"
    all_timestamps = get_all_wayback_timestamps(url)
    print("Found timestamps:", len(all_timestamps))
    if all_timestamps:
        print("Found timestamps:", all_timestamps)
        for timestamp in all_timestamps:
            download_images_from_timestamp(url, timestamp)
    else:
        print("Failed to get Wayback Machine timestamps.")

if __name__ == "__main__":
    main()
