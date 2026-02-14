import os
import numpy as np
import cv2
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model

# ==============================
# Flask App Setup
# ==============================

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# Load Trained Model
# ==============================

print("Loading model...")
model = load_model("model.h5")
print("Model Loaded Successfully!")

# ==============================
# Class Names (IMPORTANT)
# ==============================

# Replace these with your actual class names
class_names = sorted(os.listdir("dataset/train"))

print("Classes Loaded:", class_names)

# ==============================
# Image Preprocessing Function
# ==============================

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (160, 160))   # Must match training size
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ==============================
# Routes
# ==============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    # Save file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Preprocess image
    processed_image = preprocess_image(filepath)

    # Prediction
    prediction = model.predict(processed_image)
    
    predicted_index = np.argmax(prediction)
    predicted_class = class_names[predicted_index]
    confidence = round(float(np.max(prediction)) * 100, 2)

    # Top 3 predictions
    top3_indices = prediction[0].argsort()[-3:][::-1]
    top3 = [(class_names[i], round(float(prediction[0][i]) * 100, 2)) for i in top3_indices]

    return render_template(
        "result.html",
        breed=predicted_class,
        confidence=confidence,
        top3=top3,
        image=filepath
    )

# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
