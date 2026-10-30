# 🐄 Cow Breed Identification System Using Deep Learning

A web-based **Cow Breed Identification System** that uses Deep Learning and Computer Vision to identify Indian cow breeds from uploaded images. The system allows users to upload cow images and receive predicted breed names along with confidence scores through an interactive web application.

Built using Python, Flask, TensorFlow, Keras, OpenCV, and SQLite.

---

## 📌 Project Overview

The Cow Breed Identification System is designed to recognize different Indian cow breeds using a trained deep learning model.

The application provides a user-friendly interface where users can register, log in, upload cow images, and view prediction results. It also includes an administrator dashboard for managing registered users.

The system processes uploaded images using OpenCV and passes them to a pre-trained TensorFlow/Keras model to identify the most likely cow breed.

## 🎯 Project Objectives

- Identify different Indian cow breeds using Deep Learning.
- Develop an image-based cow breed classification system.
- Provide an interactive web application for breed identification.
- Display predicted breed names and confidence scores.
- Implement user authentication and session management.
- Provide an admin dashboard for user management.

## ✨ Key Features

### 1. User Authentication
- User registration and login.
- Secure password hashing.
- Session management using Flask-Login.
- User logout functionality.

### 2. Cow Breed Identification
- Upload cow images through the web interface.
- Image preprocessing using OpenCV.
- Automatic breed identification using a trained deep learning model.
- Support for 23 cow breed categories.

### 3. Prediction Results
- Display the predicted cow breed.
- Show prediction confidence percentage.
- Display the top three predicted breeds.
- Show the uploaded image with prediction results.

### 4. Admin Dashboard
- View total registered users.
- View administrator and regular user counts.
- View recently registered users.
- Manage registered users.
- Promote or demote user accounts.
- Delete user accounts.
- Reset user passwords.

### 5. Additional Features
- Responsive web interface.
- Custom CSS styling.
- Theme customization using JavaScript.
- SQLite database integration.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Backend programming |
| Flask | Web application framework |
| TensorFlow 2.10.0 | Deep learning framework |
| Keras | Model loading and prediction |
| OpenCV 4.8.1 | Image processing |
| NumPy 1.23.5 | Numerical operations |
| Pillow | Image handling |
| Flask-Login | User authentication |
| Flask-SQLAlchemy | Database integration |
| SQLite | Database management |
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | Client-side functionality |

## 🧠 Deep Learning Model

The application uses a trained deep learning model saved in HDF5 format.

**Model File:** `model.h5`

The model is loaded using TensorFlow/Keras and used to classify uploaded cow images into one of the supported breed categories.

### Image Preprocessing

Before prediction, the uploaded image goes through the following preprocessing steps:

1. Read the uploaded image using OpenCV.
2. Resize the image to 160 × 160 pixels.
3. Normalize pixel values by dividing by 255.
4. Expand the image dimensions to match the model input format.
5. Pass the processed image to the trained model.

### Prediction Process

1. The trained model generates prediction probabilities.
2. The highest probability determines the predicted breed.
3. The corresponding breed name is retrieved from the dataset class names.
4. The system calculates the prediction confidence.
5. The top three predicted breeds are displayed with their confidence scores.

### Dataset Organization

The dataset contains 23 cow breed categories, organized into separate folders.

The application dynamically retrieves breed names from the `dataset/train/` directory.

## 📂 Project Structure

```text
Cow-Breed-Recoginsition/
│
├── app.py
├── train_model.py
├── model.h5
├── requirements.txt
├── training_graph.png
│
├── dataset/
│   └── train/
│       ├── Breed_1/
│       ├── Breed_2/
│       └── ... (23 breed categories)
│
├── instance/
│   └── users.db
│
├── static/
│   ├── css/
│   │   ├── admin.css
│   │   └── style.css
│   │
│   ├── js/
│   │   └── theme.js
│   │
│   ├── uploads/
│   └── model.h5
│
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   └── users.html
│   │
│   ├── index.html
│   ├── landing.html
│   ├── login.html
│   ├── signup.html
│   ├── prediction.html
│   └── result.html
│
└── README.md
```

**Note:** The `venv/` and `__pycache__/` directories are generated locally and are not required in the GitHub repository. The application loads `model.h5` from the project root.

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Make sure the following software is installed:

- Python 3.10
- Visual Studio Code
- Git
- Web browser

### Step 1: Clone the Repository

Open your terminal and execute:

```bash
git clone https://github.com/surajnaikwade-cmyk/Cow-Breed-Recoginsition.git
```

Navigate to the project directory:

```bash
cd Cow-Breed-Recoginsition
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again.

### Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 5: Install Required Dependencies

Install TensorFlow and NumPy:

```bash
pip install tensorflow==2.10.0 numpy==1.23.5
```

Install OpenCV:

```bash
pip install opencv-python==4.8.1.78
```

Install Flask and other dependencies:

```bash
pip install flask pillow flask-login flask-sqlalchemy werkzeug
```

### Step 6: Verify Installation

Check TensorFlow:

```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

Check OpenCV:

```bash
python -c "import cv2; print(cv2.__version__)"
```

Check NumPy:

```bash
python -c "import numpy; print(numpy.__version__)"
```

Expected versions:

```text
TensorFlow: 2.10.0
OpenCV: 4.8.1
NumPy: 1.23.5
```

### Step 7: Run the Application

Make sure the trained model `model.h5` is available in the project root directory.

Execute:

```bash
python app.py
```

The Flask development server will start at:

```text
http://127.0.0.1:5000
```

Open the URL in your browser to access the Cow Breed Identification System.

## 🔄 Application Workflow

```text
          Start Application
                 |
                 v
          Open Web Interface
                 |
                 v
          User Registration
                 |
                 v
             User Login
                 |
                 v
          Upload Cow Image
                 |
                 v
          Image Preprocessing
                 |
                 v
          Load Trained Model
                 |
                 v
           Model Prediction
                 |
                 v
          Identify Cow Breed
                 |
                 v
        Calculate Confidence Score
                 |
                 v
          Generate Top 3 Results
                 |
                 v
          Display Result Page
                 |
                 v
                 End
```

## 🗄️ Database Management

The application uses **SQLite** with Flask-SQLAlchemy for database management.

The database stores user information, including:

| Field | Description |
|---|---|
| id | Unique user identification |
| username | User's username |
| email | Registered email address |
| password | Hashed user password |
| is_admin | Administrator access status |
| created_at | Account creation date |

The database tables are automatically created when the application starts.

Database location:

```text
instance/users.db
```

## 🔐 Default Admin Credentials

The application automatically creates a default administrator account when the database is initialized for the first time.

| Field | Credentials |
|---|---|
| Username | admin |
| Password | admin123 |

**Important:** Change the default administrator password before using the application in a shared or production environment.

## ⚠️ Troubleshooting

### 1. TensorFlow Installation Error

Use Python 3.10 and install the compatible TensorFlow version:

```bash
pip install tensorflow==2.10.0
```

### 2. NumPy Compatibility Error

If TensorFlow displays errors related to NumPy 2.x, install:

```bash
pip uninstall numpy -y
pip install numpy==1.23.5
```

### 3. OpenCV Module Not Found

Install the compatible OpenCV version:

```bash
pip install opencv-python==4.8.1.78
```

### 4. Model File Not Found

Make sure `model.h5` exists in the project root directory.

### 5. Dataset Classes Not Found

Ensure that the dataset is organized as follows:

```text
dataset/
└── train/
    ├── Breed_1/
    ├── Breed_2/
    └── ...
```

### 6. CUDA Warning

TensorFlow may display CUDA-related warnings if the required GPU libraries are unavailable. The application can still run using CPU processing.

## 🔒 Security Considerations

- User passwords are stored using Werkzeug password hashing.
- User sessions are managed through Flask-Login.
- Administrative routes require administrator privileges.
- Change the default admin password.
- Use a secure environment-based Flask secret key.
- Disable debug mode before production deployment.
- Validate uploaded images and restrict file sizes before public deployment.

## 🚀 Future Enhancements

- Improve prediction accuracy with additional training images.
- Add more Indian cow breed categories.
- Maintain prediction history for registered users.
- Display detailed information about identified breeds.
- Improve image validation and upload security.
- Develop a mobile-friendly interface.
- Deploy the application to a cloud platform.

## 👨‍💻 Project Information

| Details | Description |
|---|---|
| Project Name | Cow Breed Identification System |
| Project Type | Web Application |
| Domain | Artificial Intelligence and Machine Learning |
| Application | Image Classification |
| Backend | Python Flask |
| Deep Learning | TensorFlow / Keras |
| Image Processing | OpenCV |
| Database | SQLite |

## 🔗 GitHub Repository

**Repository:** [Cow Breed Identification System](https://github.com/surajnaikwade-cmyk/Cow-Breed-Recoginsition)

## 📜 License

This project is developed for educational and academic purposes. An appropriate open-source license can be added before public distribution.

---

**Developed using Python, Deep Learning, Computer Vision, and Flask.**