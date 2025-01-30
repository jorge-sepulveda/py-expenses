from CreditCard import CreditCard
from db import db


def main():
    ducky = db("mydb.duckdb")
    ducky.connect()
    ducky.drop_tables()
    ducky.create_tables()
    fake = CreditCard("fake", "fakedata/fake_amex.csv", "amex")
    fake.read_file()
    print(fake.cc_data)
    ducky.insert_to_credit(fake.cc_data, fake.card)

    ducky.disconnect()
    return 0

if __name__ == "__main__":
    main()
