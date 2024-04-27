from sqlalchemy import Column, Integer, String, Date, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(50))
    password = Column(VARCHAR(50))
    name = Column(Integer)

    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
    
    def _asdict(self):
        return {'id': self.id, 'email': self.email, 'password': self.password, 'name': self.name}
