from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Column, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from dbemployee import DBEmployee

# Define the PostgreSQL URL
postgresql_url = 'postgresql+psycopg2://bdinh:linh1982@localhost:5432/company'

# Create an engine
engine = create_engine(postgresql_url)

# Configure Session class and bind it to the engine
Session = sessionmaker(bind=engine)
# Create a session
session = Session()

employees = session.query(DBEmployee).all()
for user in employees:
    print(user._asdict())


# Close the session
session.close()