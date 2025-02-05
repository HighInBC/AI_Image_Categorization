import os
import requests
import base64
import argparse
from pathlib import Path
import platform
import subprocess
import time

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def restart_ollama():
    print("Restarting Ollama...")
    if platform.system() == "Windows":
        subprocess.run("ollama stop llava && ollama run llava", shell=True)
    else:
        os.system("ollama stop llava; ollama start llava")

def describe_image(image_path, ollama_url, timeout, max_retries=3):
    image_data = encode_image(image_path)
    payload = {
        "model": "llava",
        "prompt": "Describe this image in detail. Also create a list of keywords related to objects, themes etc.",
        "images": [image_data],
        "stream": False
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(ollama_url, json=payload, timeout=timeout)
            if response.status_code != 200:
                # restart_ollama()
                # time.sleep(5) 
                continue
            response.raise_for_status()
            json_response = response.json()
            description = json_response.get("response")
            if description:
                return description
            else:
                print(f"Attempt {attempt + 1} failed: No description generated.")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
        except ValueError as e:
            print(f"Attempt {attempt + 1} failed: JSON parsing error: {str(e)}\nRaw response: {response.text}")
        time.sleep(2)
    return "Error: Unable to generate description after multiple attempts."

def process_images(directory, ollama_url, timeout):
    directory = Path(directory)
    for image_path in directory.rglob("*"):
        if image_path.suffix.lower() in VALID_EXTENSIONS:
            txt_path = image_path.with_suffix(".txt")
            
            if txt_path.exists() and txt_path.stat().st_size > 0:
                print(f"Skipping: {image_path} (description already exists)")
                continue

            print(f"Processing: {image_path}")

            description = describe_image(image_path, ollama_url, timeout)

            if "Error" not in description:
                with open(txt_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(description)
                print(f"{image_path.name}: {description}")
                print(f"Saved description to: {txt_path}")
            else:
                print(f"Skipping: {image_path} due to repeated failures.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images in a given directory.")
    parser.add_argument("directory", type=str, help="Path to the directory containing images.")
    parser.add_argument("--ollama_url", type=str, default="http://localhost:11434/api/generate", help="URL of the Ollama API.")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout for API requests in seconds.")
    args = parser.parse_args()
    
    image_folder = args.directory
    ollama_url = args.ollama_url
    
    if os.path.isdir(image_folder):
        process_images(image_folder, ollama_url, args.timeout)
        print("\nProcessing complete!")
    else:
        print("Invalid directory. Please enter a valid path.")
