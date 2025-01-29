import pandas as pd
import duckdb 
from datetime import datetime
from db import db

card_columns = {"amex": {"Date":"statement_date","Description":"description","Category":"category","Amount":"amount"},
                 "chase":{"Post Date":"statement_date", "Description":"description", "Category":"category", "Amount":"amount"}}
card_mappings = {"amex": ["Date", "Description", "Amount", "Category"],
                 "chase": ["Post Date", "Description", "Amount", "Category"]}

class CreditCard:
    def __init__(self, card, fileName, company):
        self.card = card
        self.fn = fileName
        self.company = company
        self.cc_data = pd.DataFrame()

    def read_file(self):
        csv = pd.read_csv(self.fn)
        filtered_csv = csv[card_mappings[self.company]].copy()
        filtered_csv.rename(columns=card_columns[self.company], inplace=True)
        if self.company == "amex":
            filtered_csv["category"] = filtered_csv["category"].str.replace(".+-","",regex=True)
        elif self.company == "chase":
            filtered_csv['amount'] = filtered_csv["amount"]*-1
        else:
            print("something went wrong with company name, aborting")
            return 1
        filtered_csv['statement_date'] = pd.to_datetime(filtered_csv['statement_date'],format="%m/%d/%Y")
        filtered_csv['statement_date'] = filtered_csv['statement_date'].dt.strftime('%Y-%m-%d')
        self.cc_data = filtered_csv
        return 0

        
# Keeo for future blog posts
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


ducky = db("mydb.duckdb")
ducky.connect()

g = CreditCard("gold","../stmts/Amex/gold/2024.csv","amex" )
b = CreditCard("blue","../stmts/Amex/blue/2024.csv","amex" )
p = CreditCard("plat","../stmts/Amex/plat/2024.csv","amex" )
c = CreditCard("free","../stmts/Chase/CC/2024.csv","chase" )

g.read_file()
b.read_file()
p.read_file()
c.read_file()

ducky.drop_tables()
ducky.create_tables()

ducky.insert_to_credit(g.cc_data, g.card)
ducky.insert_to_credit(b.cc_data, b.card)
ducky.insert_to_credit(p.cc_data, p.card)
ducky.insert_to_credit(c.cc_data, c.card)

ducky.disconnect()
