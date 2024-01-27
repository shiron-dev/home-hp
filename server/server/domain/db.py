from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

db_path = os.environ.get("DB_PATH", "/home-hp.db")
db_url = f"sqlite://{db_path}"

ENGINE = create_engine(db_url, echo=True)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

Base = declarative_base()
