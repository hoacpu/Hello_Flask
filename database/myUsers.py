from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Column, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from dbuser import DBUser

# Define the PostgreSQL URL
postgresql_url = 'postgresql+psycopg2://bdinh:linh1982@localhost:5432/company'

# Create an engine
engine = create_engine(postgresql_url)

# Configure Session class and bind it to the engine
Session = sessionmaker(bind=engine)
# Create a session
session = Session()

users = session.query(DBUser).all()
for user in users:
    print(user._asdict())


# Close the session
session.close()