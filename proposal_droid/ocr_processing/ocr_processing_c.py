import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import pytesseract


import openai
import base64
import requests


def extract_text_from_image(api_key, image_path):
    """
    tanslating image to base64 and then performaning ocr on it
    """
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Encode the image
    base64_image = encode_image(image_path)

    # Define headers and payload for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":  "you are given handwritten text image which you are tasked to convert it to text, just provide the text nothing else no expelenation "
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Extract and return the text from the response
    if response.status_code == 200:
        response_data = response.json()
        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code} - {response.text}"



def preprocess_handwritten_image(image_path):
    """
    prepare image for ocr
    """
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image is loaded properly
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Step 1: Noise reduction
    denoised_image = cv2.medianBlur(image, 1)
    #display_image('Denoised Image', denoised_image)

    # Step 2: Binarization
    _, binary_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #display_image('Binary Image', binary_image)

    # Save the preprocessed image
    cv2.imwrite('preprocessed_handwritten_image.jpg', binary_image)

    print("Preprocessing complete and image saved as 'preprocessed_handwritten_image.jpg'")

def load_model_and_predict(image_path):
    """
    ocr via MS handrwritting model
    """
    try:
        # Load the processor and model
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-large-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-large-handwritten")

        # Open the image
        image = Image.open(image_path).convert("RGB")  # Ensure the image has 3 channels (RGB)

        # Preprocess the image
        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        # Generate text predictions
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def tes_ext(path):
  """
  OCR by tesseract worst option
  """
  custom_config = r'--oem 3 --psm 6'
  raw_text_4 = pytesseract.image_to_string(path, config=custom_config)
  return raw_text_4