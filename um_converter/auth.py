import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# ---------------- SIGNUP ----------------
def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return {"success": True, "message": "Account created successfully"}
    except Exception as e:
        error = str(e)

        if "EMAIL_EXISTS" in error:
            return {"success": False, "message": "Email already exists"}
        elif "WEAK_PASSWORD" in error:
            return {"success": False, "message": "Password too weak"}
        else:
            return {"success": False, "message": "Signup failed"}

# ---------------- LOGIN ----------------
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return {"success": True, "message": "Login successful"}
    except Exception:
        return {"success": False, "message": "Invalid credentials"}

# ---------------- FORGOT PASSWORD ----------------
def forgot_password(email):
    try:
        auth.send_password_reset_email(email)
        return {"success": True, "message": "Password reset email sent 📩"}
    except Exception:
        return {"success": False, "message": "Failed to send reset email"}