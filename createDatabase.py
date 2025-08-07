import sqlite3

command = """
CREATE TABLE contact_list(
    Id integer primary key,
    Email MEDIUMTEXT,
    Step INTEGER,
    Prefered_Day INTEGER,
    UNIQUE(Email)
    
);
"""


con = sqlite3.connect("contact_list.db")
cur = con.cursor()
cur.execute(command)
