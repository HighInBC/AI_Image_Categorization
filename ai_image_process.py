import os
import requests
import base64
import argparse
from pathlib import Path

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def describe_image(image_path, ollama_url):
    image_data = encode_image(image_path)
    payload = {
        "model": "llava",
        "prompt": "Describe this image in detail. Also create a list of keywords related to objects, themes etc.",
        "images": [image_data],
        "stream": False
    }
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
                
        json_response = response.json()
        return json_response.get("response", "No description generated.")
    except requests.exceptions.RequestException as e:
        return f"Error processing image: {str(e)}"
    except ValueError as e:
        return f"JSON parsing error: {str(e)}\nRaw response: {response.text}"

def process_images(directory, ollama_url):
    directory = Path(directory)
    for image_path in directory.rglob("*"):
        if image_path.suffix.lower() in VALID_EXTENSIONS:
            txt_path = image_path.with_suffix(".txt")
            
            if txt_path.exists() and txt_path.stat().st_size > 0:
                print(f"Skipping: {image_path} (description already exists)")
                continue

            print(f"Processing: {image_path}")

            description = describe_image(image_path, ollama_url)

            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(description)
            print(f"{image_path.name}: {description}")

            print(f"Saved description to: {txt_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images in a given directory.")
    parser.add_argument("directory", type=str, help="Path to the directory containing images.")
    parser.add_argument("--ollama_url", type=str, default="http://localhost:11434/api/generate", help="URL of the Ollama API.")
    args = parser.parse_args()
    
    image_folder = args.directory
    ollama_url = args.ollama_url
    
    if os.path.isdir(image_folder):
        process_images(image_folder, ollama_url)
        print("\nProcessing complete!")
    else:
        print("Invalid directory. Please enter a valid path.")