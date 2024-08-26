import os
import requests

# Filter out in the export the url that is from couldfront example https://xxx.cloudfront.net/image/xxxx/xxx.jpeg  the end could be also .mp4 etc that doesn't matter
# for this script then save all the url in one file and call it image_urls.txt
def download_image(url, save_folder, count):
    try:
        # Get the content of the image
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Extract the image format from the URL (e.g., .jpg, .png)
        ext = os.path.splitext(url)[1]
        
        # Define the path where the image will be saved
        image_path = os.path.join(save_folder, f"image_{count}{ext}")
        
        # Save the image to the specified path
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded {url} as {image_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Main function to download images from a list of URLs
def download_images_from_txt(file_path, save_folder):
    # Create the folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)
    
    # Read the URLs from the text file
    with open(file_path, 'r') as file:
        urls = file.readlines()
    
    # Download each image
    for count, url in enumerate(urls, start=1):
        url = url.strip()  # Remove any leading/trailing whitespace
        if url:
            download_image(url, save_folder, count)

if __name__ == "__main__":
    # Specify the path to your .txt file and the folder where images will be saved
    txt_file_path = "image_urls.txt"
    output_folder = "downloaded_images"
    
    # Start the download process
    download_images_from_txt(txt_file_path, output_folder)
