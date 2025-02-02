import os
import requests
import base64
from pathlib import Path

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# List of valid image extensions
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}

# Function to encode an image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to generate a description using Ollama LLaVA
def describe_image(image_path):
    image_data = encode_image(image_path)
    payload = {
        "model": "llava",
        "prompt": "Describe this image in detail. Also create a list of keywords related to objects, themes etc.",
        "images": [image_data],
        "stream": False  # Disable streaming
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        
        # DEBUG: Print raw response for troubleshooting
        print(f"Raw Response: {response.text}")
        
        # Ensure valid JSON response
        json_response = response.json()
        return json_response.get("response", "No description generated.")
    except requests.exceptions.RequestException as e:
        return f"Error processing image: {str(e)}"
    except ValueError as e:
        return f"JSON parsing error: {str(e)}\nRaw response: {response.text}"

# Function to process all images in a directory recursively
def process_images(directory):
    directory = Path(directory)
    for image_path in directory.rglob("*"):
        if image_path.suffix.lower() in VALID_EXTENSIONS:
            print(f"Processing: {image_path}")

            # Get description from Ollama
            description = describe_image(image_path)

            # Save output as a .txt file
            txt_path = image_path.with_suffix(".txt")
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(description)
            # print filename: description
            print(f"{image_path.name}: {description}")

            print(f"Saved description to: {txt_path}")

# Main execution
if __name__ == "__main__":
    image_folder = ''
    if os.path.isdir(image_folder):
        process_images(image_folder)
        print("\nProcessing complete!")
    else:
        print("Invalid directory. Please enter a valid path.")
