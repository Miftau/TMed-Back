import jwt
import time
import os
from dotenv import load_dotenv

load_dotenv()

def generate_jitsi_jwt(room_name, user_name, user_email, is_moderator=False):
    app_id = "JITSI_APP_ID"
    secret = "JITSI_SECRET"

    payload = {
        "aud": "jitsi",
        "iss": app_id,
        "sub": "meet.jit.si",
        "room": room_name,
        "exp": int(time.time()) + 3600,
        "context": {
            "user": {
                "name": user_name,
                "email": user_email,
                "moderator": is_moderator
            }
        }
    }

    token = jwt.encode(payload, secret, algorithm='HS256')
    return token
