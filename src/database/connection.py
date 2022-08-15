
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.schema import EventType
from database.schema import Course
from database.schema import Player
from database.schema import Tournament
from database.schema import TournamentPlayerResult


load_dotenv('../../../.env')
DB_USER = os.getenv('POSTGRES_USER')
DB_PW = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('golf_db')

Session = None


def get_db_session():
    db_conn_string = f'postgres://{DB_USER}:{DB_PW}@localhost:5432/{DB_NAME}'

    engine = create_engine(
        db_conn_string,
        pool_size=1,
        max_overflow=0,
        pool_recycle=3600,
        pool_pre_ping=True,
        pool_use_lifo=True
    )

    EventType.__table__.create(bind=engine, checkfirst=True)
    Course.__table__.create(bind=engine, checkfirst=True)
    Player.__table__.create(bind=engine, checkfirst=True)
    Tournament.__table__.create(bind=engine, checkfirst=True)
    TournamentPlayerResult.__table__.create(bind=engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    return Session()
