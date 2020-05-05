import sqlite3  
  
con = sqlite3.connect("feedback.db")  
print("Database opened successfully")  
  
con.execute("create table feedback (Name TEXT, id TEXT,TOOL TEXT,feedback TEXT,Email TEXT,suggestion TEXT)")  
  
print("Table created successfully")  
  
con.close()