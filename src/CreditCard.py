import pandas as pd
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

        


