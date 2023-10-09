import os
import traceback

from dotenv import load_dotenv
from sqlalchemy import create_engine

from Utils.DAL.connector import MySQLBase

# Initialize and manage database connections
def init_db():
    host = os.environ["DATABASE_HOST"]
    port = os.environ["DATABASE_PORT"]
    user = os.environ["DATABASE_USERNAME"]
    password = os.environ["DATABASE_PASSWORD"]
    database = os.environ["DATABASE"]

    conn_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    try:
        MySQLBase._engine = create_engine(conn_string)
        Meta = MySQLBase.metadata
        Meta.create_all(MySQLBase._engine)
        print("MySQL DB Connection Successful!!")
    except Exception as e:
        print(traceback.format_exc())


# Load environment variables and initialize the database
def startup_handler():
    load_dotenv()
    init_db()


def shutdown_handler():
    pass
