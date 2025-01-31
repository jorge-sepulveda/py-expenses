from CreditCard import CreditCard
from db import db
from Checking import Checking


def main():
    ducky = db("mydb.duckdb")
    ducky.connect()
    ducky.drop_tables()
    ducky.create_tables()
    fake = CreditCard("green", "fakedata/f_blue.csv", "amex")
    fake_two = CreditCard("black", "fakedata/f_red.csv", "amex")
    chase = Checking("../stmts/Chase/Checking/2024.CSV", "chase")

    fake.read_file()
    fake_two.read_file()
    chase.read_file()
    ducky.insert_to_credit(fake.cc_data, fake.card)
    ducky.insert_to_credit(fake_two.cc_data, fake_two.card)
    ducky.insert_to_checking(chase.c_data)
    ducky.disconnect()
    return 0

if __name__ == "__main__":
    main()
