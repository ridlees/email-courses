import sqlite3
from multiprocessing import Pool, freeze_support
from sender import send_email

from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

port = os.environ.get("PORT")
smtp_server = os.environ.get("SMTP_SERVER")
sender_email = os.environ.get("SENDER_EMAIL")
password = os.environ.get("PASSWORD")
path_to_content = os.environ.get("CONTENT")
max_step = os.environ.get("LIMIT") 

def connect_to_database(path):
    try:
        con = sqlite3.connect("contact_list.db")
        cur = con.cursor()
        return con, cur
    except:
        print("Failed to init database")
        return 0

def update_step(con,cur,):
    try:
        query = f"""
    UPDATE contact_list
    SET Step = CASE
                  WHEN Step + 1 > {max_step} THEN {max_step}
                  ELSE Step + 1
              END;
    """
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        
    
        
#  TODO Logic for prefered days
def sender_logic(email, step):
    try:
        if step == int(max_step):
            return "Finished the course"
        path_to_message = f"{path_to_content}/{step}.txt"
        with open(path_to_message, "r") as f:
            message = f.read()
            send_email(port, smtp_server, sender_email, password, email, message) 
        return f"Sent {step} to {email}"
    except Exception as e:
        return e

def main():
    con, cur = connect_to_database("contact_list.db")
    try:
        emails = cur.execute("SELECT * FROM contact_list")
        freeze_support()
        with Pool(processes=10) as pool:
            results = [pool.apply_async(sender_logic, args=(email[1], email[2])) for email in emails]
            final_results = [r.get() for r in results]
            print(final_results)
            update_step(con, cur)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main() 
