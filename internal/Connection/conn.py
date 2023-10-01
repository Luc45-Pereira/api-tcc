from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv

dotenv.load_dotenv()

class Session():
    engine = create_engine(url=f"mysql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_URL')}/{os.environ.get('DATABASE_NAME')}")
    
    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def get_engine(self):
        return self.engine