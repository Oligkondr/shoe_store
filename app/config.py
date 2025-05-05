import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


def get_db_url():
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_auth_data():
    return {"secret_key": secret_key, "algorithm": algorithm}
