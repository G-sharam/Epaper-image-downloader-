import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timedelta

def download_image(image_url, folder_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 100:
            

            image_name = os.path.basename(image_url)
            image_path = os.path.join(folder_path, image_name)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_name}")
        else:
            print(f"Failed to download: {image_url}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

def scrape_images(url, folder_path, max_images=100):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all('img')
    count = 0

    for img in images:
        if count >= max_images:
            break
        img_url = urljoin(url, img['src'])
        download_image(img_url, folder_path)
        count += 1

def main():
    base_url = input("Enter the URL of the e-paper: ")
    folder_name = "downloaded_images"
    

    for day in range(10):
        date = datetime.now() - timedelta(days=day)
        formatted_date = date.strftime("%Y-%m-%d") 
        url = f"{base_url}/{formatted_date}"  
        print(f"Scraping images from: {url}")
        scrape_images(url, folder_name)

if __name__ == "__main__":
    main()
