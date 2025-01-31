import duckdb
import pandas

class db:
    def __init__(self,db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = duckdb.connect(self.db_name)
        return 0
    
    def disconnect(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
            return 1
        else:
            print("Database connector is none.")
            return 1

    def create_tables(self):
        if self.conn == None:
            print("empty connector, run connect()")
            return 1
        credit_sequence = "CREATE SEQUENCE IF NOT EXISTS credit_id_seq START WITH 1 INCREMENT BY 1;"
        checking_sequence = "CREATE SEQUENCE IF NOT EXISTS checking_id_seq START WITH 1 INCREMENT BY 1;"
        credit_stmt = """
        CREATE TABLE Credit (
            id INTEGER PRIMARY KEY DEFAULT nextval('credit_id_seq'),
            statement_date DATE NOT NULL,
            description VARCHAR(255),
            amount DECIMAL(15,2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            card VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        checking_stmt = """
        CREATE TABLE Checking (
            id INTEGER PRIMARY KEY DEFAULT nextval('checking_id_seq'),
            posting_date DATE NOT NULL,
            description VARCHAR(255),
            amount DECIMAL(15,2) NOT NULL,
            type VARCHAR(20) NOT NULL,
            remaining_balance DECIMAL(15,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        statements = [credit_sequence,checking_sequence, credit_stmt, checking_stmt]
        [self.conn.execute(i) for i in statements]
        return 0

    def drop_tables(self):
        if self.conn == None:
            print("connector unavailable")
            return 1
        drop_credit_sequence = "DROP SEQUENCE IF EXISTS credit_id_seq"
        drop_checking_sequence = "DROP SEQUENCE IF EXISTS checking_id_seq"
        drop_checking = "DROP TABLE if exists Checking"
        drop_credit = "DROP TABLE if exists Credit"
        drops = [drop_credit_sequence, drop_checking_sequence, drop_checking, drop_credit]
        [self.conn.execute(i) for i in drops]
        return 0

    def insert_to_credit(self, cc_data, card):
        if self.conn == None:
            print("empty db connector")
            return 1
        if len(cc_data) > 0:
            for index, row in cc_data.iterrows():
                self.conn.execute(f"INSERT INTO Credit(statement_date, description, category, amount, card) VALUES (?,?,?,?,?)", (row["statement_date"], row["description"], row["category"], row["amount"],card))
            return 0
        else:
            print("Empty dataframe!")
            return 1


    def insert_to_checking(self,c_data):
        if self.conn == None:
            print("empty db connector")
            return 1
        if len(c_data) > 0:
            for index, row in c_data.iterrows():
                self.conn.execute(f"INSERT INTO Checking(posting_date, description, type, amount, remaining_balance) VALUES (?,?,?,?,?)", (row["posting_date"], row["description"], row["type"], row["amount"], row["remaining_balance"]))
            return 0
        else:
            print("Empty dataframe!")
            return 1

