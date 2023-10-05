import jwt
import datetime
import os
import dotenv

dotenv.load_dotenv()

class Token:
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM")

    def __init__(self, user_id = None, user_password = None, token = None):
        """ Inicializa a classe Token """
        self.user = user_id
        self.password = user_password
        self.token = token
    
    def generate_token(self) -> str:
        """ Gera um token de acesso """
        payload = {
            "user": self.user,
            "password": self.password,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        return jwt.encode(payload, self.secret, self.algorithm)
    
    def autenticate_token(self):
        """ Autentica um token de acesso """
        try:
            payload = jwt.decode(self.token, self.secret, self.algorithm)
            return payload["user"]
        except jwt.ExpiredSignatureError:
            return "Token expirado"
        except jwt.InvalidTokenError:
            return "Token inválido"