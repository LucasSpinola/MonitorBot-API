from firebase_admin import db
from passlib.context import CryptContext
import bcrypt
from fastapi import HTTPException, Depends
from app.api.auth.jwt_bearer import JWTBearer

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def add_user_to_firebase(user):
    if check_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    hashed_password = get_password(user.password)
    new_user_ref = db.reference("/users").push(
        {
            "email": user.email,
            "password": hashed_password,
        }
    )

    return new_user_ref.key

def check_duplicate_email(email):
    users_ref = db.reference("/users")
    users_snapshot = users_ref.get()

    if users_snapshot:
        for _, user_data in users_snapshot.items():
            if user_data.get("email") == email:
                return True

    return False

def check_user_in_firebase(data):
    users_ref = db.reference("/users")
    users_snapshot = users_ref.get()

    if users_snapshot:
        for user_id, user_data in users_snapshot.items():
            stored_password = user_data.get("password")
            if user_data.get("email") == data.email and verify_password(data.password, stored_password):
                return True

    return False

def get_current_user(token: str = Depends(JWTBearer())):
    return token