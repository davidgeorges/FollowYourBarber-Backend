from datetime import datetime, timedelta
from follow_your_barber import settings
import jwt
import time

class TokenError(Exception):
    pass

class TokenManager :
    __token_error = " "

    def __init__(self):
        self.jwt_algorithm = settings.JWT_ALGORITHM
        self.access_token_secret = settings.JWT_ACCESS_TOKEN_SECRET
        self.refresh_token_secret = settings.JWT_REFRESH_TOKEN_SECRET
        self.access_token_expires_in = settings.JWT_ACCESS_TOKEN_EXPIRES_IN
        self.refresh_token_expires_in = settings.JWT_REFRESH_TOKEN_EXPIRES_IN

    def get_data(self, data_to_get, token_receive, token_type):
        try:
            if token_type == "ACCESS" or token_type == "REFRESH" :
                token = token_receive.replace("Bearer ", "", 1)
                token_secret = self.access_token_secret if token_type == "ACCESS" else self.refresh_token_secret
                decode_token = jwt.decode(token, token_secret, algorithms=[self.jwt_algorithm])
                return decode_token.get(data_to_get)
            else:
                raise ValueError("Invalid token_type. Expected 'ACCESS' or 'REFRESH'.")
        except jwt.ExpiredSignatureError:
            raise TokenError(f"Token expired: {data_to_get}")
        except jwt.DecodeError as e:
            raise TokenError(f"Error decoding token {data_to_get}: {e}")

    def check_if_is_expired(self, token_receive, token_type):
        try:
            if token_type == "ACCESS" or token_type == "REFRESH" :
                token = token_receive.replace("Bearer ", "", 1)
                token_secret = self.access_token_secret if token_type == "ACCESS" else self.refresh_token_secret
                decode_token = jwt.decode(token, token_secret, algorithms=[self.jwt_algorithm])
                exp_time = decode_token.get("exp", 0)
                if exp_time >= time.time():
                    return False
                else:
                    return True
            else:
                raise ValueError("Invalid token_type. Expected 'ACCESS' or 'REFRESH'.")
        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired")
        except jwt.DecodeError as e:
            raise TokenError(f"Decode Error: {e}")

    def create_token(self, id_receive, role_receive, account_status_receive, token_type):
        try:
            if token_type == "ACCESS" or token_type == "REFRESH" :
                token_secret = self.access_token_secret if token_type == "ACCESS" else self.refresh_token_secret
                expires_in = self.access_token_expires_in if token_type == "ACCESS" else self.refresh_token_expires_in
                exp_time = datetime.utcnow() + timedelta(minutes=expires_in)
                payload = {"id": id_receive, "role": role_receive, "accountStatus" : account_status_receive, "exp": exp_time}
                return jwt.encode(payload, token_secret, algorithm=self.jwt_algorithm)
            else:
                raise ValueError("Invalid token_type. Expected 'ACCESS' or 'REFRESH'.")
        except jwt.PyJWTError as e:
            raise TokenError(f"Error creating user token: {e}")

    def set_token_error(self, error_message):
        self.__token_error = error_message

    def get_token_error(self):
        return self.__token_error

token_manager = TokenManager()
