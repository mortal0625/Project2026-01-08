import os
# Suppress TensorFlow logging (INFO and WARNING messages)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
from keras.models import load_model
from PIL import Image, ImageOps, ImageFont, ImageDraw
import numpy as np

# Load the model and labels
model_loaded = False
try:
    model = load_model("keras_Model.h5", compile=False)
    class_names = open("labels.txt", "r", encoding="utf-8").readlines()
    # Load a font that supports Chinese characters
    font_path = "C:/Windows/Fonts/msjh.ttc"  # Microsoft JhengHei
    font = ImageFont.truetype(font_path, 24)
    model_loaded = True
except FileNotFoundError:
    print("Error: keras_Model.h5, labels.txt, or font file not found.")
    print("Please ensure 'keras_Model.h5' and 'labels.txt' are in the same directory.")
    print("Continuing without prediction functionality.")

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to create a non-mirrored view
    frame = cv2.flip(frame, 1)

    # --- Prediction logic ---
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Convert the frame to a temporary PIL image for prediction
    image_for_pred = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # Resize and crop the image
    size = (224, 224)
    image_for_pred = ImageOps.fit(image_for_pred, size, Image.Resampling.LANCZOS)
    # Turn the image into a numpy array and normalize
    image_array = np.asarray(image_for_pred)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    # Load the image into the array
    data[0] = normalized_image_array


    # --- Text drawing logic ---
    if model_loaded:
        prediction = model.predict(data, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Format the text to display, stripping newline characters from class_name
        prediction_text = f"類別: {class_name.strip()}"
        confidence_text = f"信心度: {confidence_score:.2%}"

        # Convert OpenCV frame (BGR) to PIL Image (RGB) for drawing
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        
        # Draw text on the image
        draw.text((10, 30), prediction_text, font=font, fill=(0, 255, 0))
        draw.text((10, 60), confidence_text, font=font, fill=(0, 255, 0))

        # Convert PIL Image back to OpenCV frame (BGR)
        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    else:
        # Use cv2.putText for English text if model is not loaded
        cv2.putText(frame, "Model not loaded. Please provide keras_Model.h5 and labels.txt", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Camera Feed with Prediction', frame)

    # Break the loop if 'q' is pressed or window is closed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Camera Feed with Prediction', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
