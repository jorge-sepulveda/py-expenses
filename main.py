import pandas as pd
import duckdb 
from datetime import datetime

conn = duckdb.connect("mydb.duckdb")

def read_amex(fileName):
    csv = pd.read_csv(fileName)
    new_column = {"Date":"statement_date","Description":"description","Category":"sub_category","Amount":"amount"}
    filtered_csv = csv[["Date", "Description", "Amount", "Category"]].copy()
    filtered_csv.rename(columns=new_column, inplace=True)
    filtered_csv["category"] = filtered_csv["sub_category"].str.extract(r"(.+)-")
    filtered_csv.loc[:, "sub_category"] = filtered_csv["sub_category"].str.replace(".+-","", regex=True)
    filtered_csv['statement_date'] = pd.to_datetime(filtered_csv['statement_date'],format="%m/%d/%Y")
    filtered_csv['statement_date'] = filtered_csv['statement_date'].dt.strftime('%Y-%m-%d')
    return filtered_csv

def read_chase_cc(fileName):
    csv = pd.read_csv(fileName)
    new_column = {"Post Date":"statement_date", "Description":"description", "Category":"category", "Amount":"amount"}
    filtered_csv = csv[["Post Date", "Description", "Amount", "Category"]].copy()
    filtered_csv.rename(columns=new_column, inplace=True)
    filtered_csv['statement_date'] = pd.to_datetime(filtered_csv['statement_date'],format="%m/%d/%Y")
    filtered_csv['statement_date'] = filtered_csv['statement_date'].dt.strftime('%Y-%m-%d')
    filtered_csv['amount'] = filtered_csv["amount"]*-1
    filtered_csv["sub_category"]="nan"
    return filtered_csv


    

conn.execute("DROP TABLE if exists Credit")
conn.execute("DROP SEQUENCE IF EXISTS credit_id_seq")
conn.execute("CREATE SEQUENCE IF NOT EXISTS credit_id_seq START WITH 1 INCREMENT BY 1;")

table_stmt = """
CREATE TABLE Credit (
    id INTEGER PRIMARY KEY DEFAULT nextval('credit_id_seq'),
    statement_date DATE NOT NULL,
    description VARCHAR(255),
    amount DECIMAL(15,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100),
    card VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


conn.execute(table_stmt)
conn.execute("truncate Credit")

gold = read_amex("stmts/Amex/gold/2024.csv")
c = read_chase_cc("stmts/Chase/CC/2024.csv")
plat = read_amex("stmts/Amex/plat/2024.csv")
blue = read_amex("stmts/Amex/blue/2024.csv")




def insert_to_db(df, card):
    for index, row in df.iterrows():
        conn.execute(f"INSERT INTO Credit(statement_date, description, category, sub_category, amount, card) VALUES (?,?,?,?,?,?)", (row["statement_date"], row["description"], row["category"], row["sub_category"], row["amount"],card))

insert_to_db(gold, "gold")
insert_to_db(c, "free")
insert_to_db(plat, "plat")
insert_to_db(blue, "blue")

#result = conn.execute("SELECT * FROM Credit").fetchall()
#result = conn.execute("select distinct sub_category from Credit").fetchall()
#print(result)


conn.close()
