import pandas as pd
from io import StringIO
account_columns = {"chase":{"Posting Date":"posting_date", "Description":"description", "Type":"type", "Amount":"amount", "Balance":"remaining_balance"}}
account_mappings = { "chase": ["Posting Date", "Description", "Amount", "Type", "Balance"]}

class Checking:
    def __init__(self, filePath, company):
        self.fp = filePath
        self.company = company
        self.c_data = pd.DataFrame

    def read_file(self):

        # Read the file and clean it in memory
        with open(self.fp, "r") as infile:
            cleaned_lines = [line.rstrip(",\n") + "\n" for line in infile]

        cleaned_data = "\n".join(cleaned_lines)
        cleaned_file = StringIO(cleaned_data)
        csv = pd.read_csv(cleaned_file)
        filtered_csv = csv[account_mappings[self.company]].copy()
        print(filtered_csv)
        filtered_csv.rename(columns=account_columns[self.company], inplace=True)
        filtered_csv['posting_date'] = pd.to_datetime(filtered_csv['posting_date'],format="%m/%d/%Y")
        filtered_csv['posting_date'] = filtered_csv['posting_date'].dt.strftime('%Y-%m-%d')
        print(filtered_csv)
        self.c_data = filtered_csv
        return 0


