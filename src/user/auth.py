from datetime import datetime, timezone, timedelta
import bcrypt
import jwt


def hash_user_password(clear_password: str) -> str:
    return bcrypt.hashpw(clear_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def check_user_password(clear_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        clear_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_jwt_token(user_name, secret_key, days_to_expire: int):
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(days=days_to_expire)

    claims = {
        "iss": "voucher-io",
        "iat": issued_at,
        "exp": expires_at,
        "subject": user_name,
    }
    encoded = jwt.encode(claims, secret_key, algorithm="HS256")
    return encoded


def validate_jwt_token(token: str, secret_key: str) -> str:
    decoded = jwt.decode(token, secret_key, algorithms="HS256")
    return decoded["subject"]
