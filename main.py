import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pretrained model
model = MobileNetV2(weights="imagenet")

def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def predict_image(img_path):
    processed_img = prepare_image(img_path)
    preds = model.predict(processed_img)
    results = decode_predictions(preds, top=3)[0]
    return [f"{label}: {prob:.2f}" for (_, label, prob) in results]

def load_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # Display image
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # Run prediction
    predictions = predict_image(file_path)
    result_text.set("\n".join(predictions))

# UI Setup
root = tk.Tk()
root.title("AI Image Recognition")

Button(root, text="Select Image", command=load_image).pack(pady=10)

image_label = Label(root)
image_label.pack()

result_text = tk.StringVar()
Label(root, textvariable=result_text, font=("Helvetica", 12), justify="left").pack(pady=10)

root.mainloop()