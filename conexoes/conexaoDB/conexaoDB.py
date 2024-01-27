from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from robo_class import Robo
import datetime

engine = create_engine('mysql+mysqlconnector://user:password@localhost/dbname', echo=True)
