import os
import numpy as np
import cv2
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Configure TensorFlow before importing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info messages
try:
    import tensorflow as tf
    # Suppress TensorFlow warnings
    tf.get_logger().setLevel('ERROR')
except Exception as e:
    print(f"Warning: Could not configure TensorFlow - {e}")

from tensorflow.keras.models import load_model


# Flask App Setup


app = Flask(__name__)
app.config["SECRET_KEY"] = "password123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# User Model


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Admin Decorator


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You do not have permission to access this page.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# Load Trained Model


model = None
class_names = []

print("Loading model...")
try:
    import tensorflow as tf
    from tensorflow.keras import layers
    
    # Try to handle the groups parameter issue in DepthwiseConv2D
    original_depthwise = layers.DepthwiseConv2D
    
    class CompatibleDepthwiseConv2D(original_depthwise):
        def __init__(self, *args, **kwargs):
            # Remove 'groups' parameter if it exists (newer TF versions)
            kwargs.pop('groups', None)
            super().__init__(*args, **kwargs)
    
    # Register the compatible version
    custom_objects = {
        'DepthwiseConv2D': CompatibleDepthwiseConv2D,
    }
    
    # Try loading with custom objects
    try:
        model = load_model("model.h5", custom_objects=custom_objects)
        print("[+] Model Loaded Successfully!")
    except FileNotFoundError:
        print("[-] model.h5 file not found!")
        print("    Please ensure model.h5 is in the project root directory.")
        model = None
    except Exception as e:
        print(f"[-] Error loading model: {e}")
        # Try standard load as fallback
        try:
            model = load_model("model.h5")
            print("[+] Model Loaded with standard loader")
        except:
            print("[-] The app will work but predictions will not be available.")
            model = None
            
except Exception as e:
    print(f"Warning: Could not setup model loading - {e}")
    model = None


# Class Names (IMPORTANT)


# Replace these with your actual class names
try:
    class_names = sorted(os.listdir("dataset/train"))
    print("Classes Loaded:", class_names)
except Exception as e:
    print(f"Warning: Could not load class names - {e}")


# Image Preprocessing Function


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (160, 160))   # Must match training size
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# Routes


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("prediction.html")
    else:
        return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not username or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("signup"))

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {username}! You're now in the prediction window.", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# Admin Routes


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    admin_count = User.query.filter_by(is_admin=True).count()
    regular_users = total_users - admin_count
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        admin_count=admin_count,
        regular_users=regular_users,
        recent_users=recent_users
    )

@app.route("/admin/users")
@admin_required
def admin_users():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=10)
    return render_template("admin/users.html", users=users)

@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash("You cannot delete your own account!", "danger")
        return redirect(url_for("admin_users"))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f"User '{username}' has been deleted.", "success")
    return redirect(url_for("admin_users"))

@app.route("/admin/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent changing your own admin status
    if user.id == current_user.id:
        flash("You cannot change your own admin status!", "danger")
        return redirect(url_for("admin_users"))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    status = "promoted to" if user.is_admin else "demoted from"
    flash(f"User '{user.username}' has been {status} admin.", "success")
    return redirect(url_for("admin_users"))

@app.route("/admin/users/<int:user_id>/reset-password", methods=["POST"])
@admin_required
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = "TempPassword123!"
    user.set_password(new_password)
    db.session.commit()
    flash(f"Password for '{user.username}' has been reset to: {new_password}", "info")
    return redirect(url_for("admin_users"))

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    if model is None:
        flash("Model is not loaded. Please contact administrator.", "danger")
        return redirect(url_for("home"))
    
    if not class_names:
        flash("Class names not available. Please contact administrator.", "danger")
        return redirect(url_for("home"))
    
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


# Run App


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Create default admin if it doesn't exist
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(username="admin", email="admin@cowvision.local", is_admin=True)
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: username='admin', password='admin123'")
            print("IMPORTANT: Change the admin password after first login!")
    
    app.run(debug=True)
