import os
from firebase_admin import credentials, initialize_app, db
from firebase_admin import db

current_dir = os.path.dirname(os.path.abspath(__file__))


service_account_path = os.path.join(current_dir, "serviceAccountKey.json")

if not os.path.isfile(service_account_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {service_account_path}")

cred = credentials.Certificate(service_account_path)
firebase_app = initialize_app(cred, {
    "databaseURL": ""
})
firebase_db = db.reference("/users")

def add_user_to_firebase(user):
    new_user_ref = db.reference("/users").push()
    new_user_ref.set({
        "email": user.email,
        "password": user.password,
    })
    return new_user_ref.key
