import easyocr
from PIL import Image
import re
import pandas as pd
import numpy as np

# Regex for phone numbers
phone_pattern = re.compile(r'\+?\d[\d\s\-]{8,15}')

# Setup EasyOCR once
easyocr_reader = easyocr.Reader(['en'], gpu=False)

def extract_contacts_from_images(images, method="handwritten"):
    results = []

    for uploaded in images:
        if hasattr(uploaded, 'read'):
            img = Image.open(uploaded)
            name = uploaded.name
        else:
            img = uploaded
            name = "unknown.jpg"

        # Use EasyOCR (for both typed and handwritten to avoid Tesseract)
        ocr_result = easyocr_reader.readtext(np.array(img))
        text = " ".join([item[1] for item in ocr_result])

        # Extract phone numbers
        numbers = phone_pattern.findall(text)
        for number in numbers:
            results.append({
                "Image": name,
                "Phone Number": number.strip()
            })

    return pd.DataFrame(results)
