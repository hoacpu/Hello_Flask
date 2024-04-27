#!/usr / bin / python 

import psycopg2 
from Hello_Flask.database.config import config 

def create_tables(): 
    """ create tables in the PostgreSQL database"""
    command = "select * from employee"

    conn = None
    try: 
        # read the connection parameters 
        params = config() 
        # connect to the PostgreSQL server 
        conn = psycopg2.connect(**params) 
        cur = conn.cursor() 
        # create table one by one

        cur.execute(command) 
        # close communication with the PostgreSQL database server 

        employee_records = cur.fetchall()
        for row in employee_records:
            print ("ID",row[0])
            print ("Name",row[1],"\n")

        cur.close() 
        # commit the changes 

    except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 
    finally: 
        if conn is not None: 
            conn.close() 


if __name__ == '__main__': 
	create_tables()
