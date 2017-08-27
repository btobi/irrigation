import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import config

engine = create_engine(URL(**config.DATABASE))

Base = declarative_base()
Session = sessionmaker(bind=engine)


class SensorLog(Base):
    __tablename__ = 'irrogation'

    def __init__(self, entity_id, type, data):
        self.entity_id = entity_id
        self.type = type
        self.data = data
        self.date = datetime.datetime.now()

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    data = Column(Float, nullable=False)

Base.metadata.create_all(engine)

session = Session()