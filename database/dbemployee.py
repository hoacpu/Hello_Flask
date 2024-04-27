from sqlalchemy import Column, Integer, String, Date, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBEmployee(Base):
    __tablename__ = 'employee'
    
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    manager_id = Column(Integer)

    def __init__(self, employee_id, first, last, manager_id):
        self.employee_id = employee_id
        self.first_name = first
        self.last_name = last
        self.manager_id = manager_id
    
    def _asdict(self):
        return {'employee_id': self.employee_id, 'first_name': self.first_name, 'last_name': self.last_name, 'manager_id': self.manager_id}
