import os
import io
import time
import base64  
import requests
from PIL import Image
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service

url = ""

# Enter query for Google search
query = "1024x1024 photos license plates"

# Convert the query into URL format
query_url = quote(query)

# Specify the desired folder path on the desktop
folder_name = ".\Temp"

try:
    # Create the folder if it doesn't exist
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)
except Exception as e:
    print(f"Error creating the folder: {str(e)}")

# Initialize the Edge web browser using options and a service
driver = webdriver.Edge()

# URL for Google Images search
def get_url(name:None, query):
    if name == "google":
        return f"https://www.google.com/search?q={query}&tbm=isch"
    elif name == "bing":
        return f"https://www.bing.com/images/search?q={query}"
    elif name == "unsplash":
        return f"https://unsplash.com/s/photos/{query}"
    elif name == "pexels":
        return f"https://www.pexels.com/search/{query}"
    elif name == "pixabay":
        return f"https://pixabay.com/images/search/{query}"
    elif name == "stocksnap":
        return f"https://stocksnap.io/search/{query}"
    elif name == "flickr":
        return f"https://www.flickr.com/search/?text={query}"
    elif name == "freeimages":
        return f"https://www.freeimages.com/search/{query}"
    elif name == "gettyimages":
        return f"https://www.gettyimages.com/search/2/image-film?phrase={query}&family=creative&sort=mostpopular"
    elif name == "istock":
        return f"https://www.istockphoto.com/search/2/image-film?phrase={query}"
    elif name == 'yahoo':
        return f'https://images.search.yahoo.com/search/images?p={query}'
    

# Open the URL in the web browser
driver.get(get_url("pexels", query_url))

def get_int(name):
    return int(name.split(".")[0])

def get_last():
    last = 0
    files = sorted(os.listdir(folder_name), key=get_int)
    if files:
        file = files[-1]
        last = get_int(file)
    return last

# Simulate scrolling to load more images
for _ in range(4):  # Adjust the number based on the number of images wanted
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for images to load
    print(f"Scrolling {_:02d}")

try:
    elements = driver.find_elements(By.CSS_SELECTOR, "img")
    print(f"Found {len(elements)} images")                                    
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Download and save images
for i, img in enumerate(elements):

    #Get the source URL
    img_url = img.get_attribute("src")

    #Save the image to the computer
    if img_url and img_url.startswith('http'):
        img_response = requests.get(img_url)
        last = get_last()
        img_name = f"{last + 1}.jpg"  
        img_path = os.path.join(folder_name, img_name)

        # Save the image to computer
        with open(img_path, "wb") as img_file:
            img_file.write(img_response.content)
    elif img_url and img_url.startswith('data:image/jpeg;base64'):
        # Open the image in a new tab
        ActionChains(driver).key_down(Keys.CONTROL).click(img).key_up(Keys.CONTROL).perform()
        # Decode base64 image data and save it
        img_data = img_url.split('base64,')[1]
        img = Image.open(io.BytesIO(base64.b64decode(img_data)))
        last = get_last()
        img_name = f"{last + 1}.jpg"
        img_path = os.path.join(folder_name, img_name)
        img.save(img_path)
    
    
print(f"Images have been downloaded and saved in the folder: {folder_name}")
