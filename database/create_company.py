#!/usr / bin / python 

import psycopg2 
from Hello_Flask.database.config import config 

def create_tables(): 
	""" create tables in the PostgreSQL database"""
	commands = ( 
        """ 
        CREATE TABLE employee (
            employee_id SERIAL PRIMARY KEY,
            first_name VARCHAR (255) NOT NULL,
            last_name VARCHAR (255) NOT NULL,
            manager_id INT,
            FOREIGN KEY (manager_id) 
            REFERENCES employee (employee_id) 
            ON DELETE CASCADE
        );
        """,  
        """ 
       INSERT INTO employee (
    employee_id,
    first_name,
    last_name,
    manager_id
)
VALUES
    (1, 'Sandeep', 'Jain', NULL),
    (2, 'Abhishek ', 'Kelenia', 1),
    (3, 'Harsh', 'Aggarwal', 1),
    (4, 'Raju', 'Kumar', 2),
    (5, 'Nikhil', 'Aggarwal', 2),
    (6, 'Anshul', 'Aggarwal', 2),
    (7, 'Virat', 'Kohli', 3),
    (8, 'Rohit', 'Sharma', 3);
        """) 
	conn = None
	try: 
		# read the connection parameters 
		params = config() 
		# connect to the PostgreSQL server 
		conn = psycopg2.connect(**params) 
		cur = conn.cursor() 
		# create table one by one 
		for command in commands: 
			cur.execute(command) 
		# close communication with the PostgreSQL database server 
		cur.close() 
		# commit the changes 
		conn.commit() 
	except (Exception, psycopg2.DatabaseError) as error: 
		print(error) 
	finally: 
		if conn is not None: 
			conn.close() 


if __name__ == '__main__': 
	create_tables()
