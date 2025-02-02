# Image Description Tool using Ollama LLaVA

This script recursively scans a directory for images, uses **Ollama's LLaVA model** to generate descriptions, and saves the results in `.txt` files with the same filename as the image.

## Installation

### Step 1: Install Ollama
Ollama provides an easy way to run LLaVA locally. To install it, run:

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

Alternatively, download the installer from the official [Ollama website](https://ollama.com/).

### Step 2: Pull the LLaVA Model
To use LLaVA for image descriptions, pull the model by running:

```sh
ollama pull llava
```

This will download the model and prepare it for use.

## Running the Script

### Step 1: Install Dependencies
Ensure you have Python 3.7+ installed. Then, install the required Python libraries:

```sh
pip install requests
```

### Step 2: Run the Script
To process a directory of images, use:

```sh
python script.py /path/to/images
```

Replace `/path/to/images` with the actual directory containing images. The script will:
- Scan the folder recursively for images (`.jpg`, `.png`, `.gif`, etc.).
- Use **Ollama’s LLaVA** model to generate descriptions.
- Save each description in a `.txt` file with the same name as the image.

### Example Output
If you have:
```
/images/cat.jpg
/images/dog.png
```

The script will generate:
```
/images/cat.txt  (contains description of cat.jpg)
/images/dog.txt  (contains description of dog.png)
```

## Troubleshooting
- **Ollama is not running**: Ensure Ollama is installed and running by executing:
  ```sh
  ollama run llava
  ```
- **Missing dependencies**: Ensure `requests` is installed using `pip install requests`.
- **Invalid directory error**: Check that the provided path exists and is accessible.

## License
This script is open-source and available for modification and distribution.

