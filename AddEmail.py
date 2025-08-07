import sqlite3
email = ""
con = sqlite3.connect("contact_list.db")
cur = con.cursor()
cur.execute(
    "INSERT INTO contact_list (Email, Step, Prefered_day) VALUES (?, 0, 0)",
    (email,)
)
con.commit()
