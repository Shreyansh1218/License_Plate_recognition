from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import easyocr
import re

# -------------------------------
# LOAD MODELS ONCE
# -------------------------------
model = YOLO("model/license_plate_detector.pt")
reader = easyocr.Reader(['en'], gpu=False)

# -------------------------------
# REGEX CLEANUP
# -------------------------------
def clean_plate_text(text):
    if not text:
        return None

    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)

    replacements = {
        'O': '0',
        'I': '1',
        'Z': '2',
        'S': '5',
        'B': '8'
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    pattern = r'[A-Z]{2}\d{2}[A-Z]{2}\d{4}'
    match = re.search(pattern, text)

    return match.group() if match else text


# -------------------------------
# OCR PREPROCESSING
# -------------------------------
def preprocess_for_ocr(plate_img):
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    return thresh


# -------------------------------
# MULTIPLE PLATE DETECTION
# -------------------------------
def detect_license_plate(pil_image, conf_threshold=0.4):
    """
    Returns:
        annotated_image (PIL)
        detections (list of dicts)
    """

    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = model(image, conf=conf_threshold)
    detections = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])

            plate_crop = image[y1:y2, x1:x2]
            processed_plate = preprocess_for_ocr(plate_crop)

            ocr_result = reader.readtext(processed_plate)
            if ocr_result:
                raw_text = ocr_result[0][1]
                plate_text = clean_plate_text(raw_text)
            else:
                plate_text = "Unreadable"

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)

            label = f"{plate_text} ({confidence:.2f})"
            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            detections.append({
                "plate": plate_text,
                "confidence": confidence
            })

        annotated_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        annotated_image = Image.fromarray(annotated_image)

    return annotated_image, plate_text, confidence

