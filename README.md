# py-expenses

This is a very nascent software built in Python to track expenses. The database behind all of this is [https://duckdb.org/](https://duckdb.org/), an in-process OLAP database tuned for analytical workloads. It can run in memory, really snappy and fast at reading. Version 1.0 was released last summer. 

The overall goal of this project is to have control of your own data and step into the world of budgeting. If you have multiple credit card companies, it can get tedious to connect everything. Banks provide CSV's of your statements for your own processing and we aim to leverage this data. 

## How to use

Once you download the repo, download the virtual environment. This is not necessary, but I advise installing duckDB on your machine. 

### Download CSV statements
Currently this project only supports Chase and American Express credit cards. The next one I have planned is Citi and Chase Checking accounts. If you want to parse your own CSV's take a look at `CreditCard.py` and make a pull requests by editing `card_columns`, `card_mappings` and `read_file()`. 

### Set up the virtual environment

```bash
cd py-expenses
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Drop the statements into the `statements` folder(or your own folder) and with that path, you'll instantiate `CreditCard` with the card codename, the file path and the company that the CSV belongs to. I've some fake data inside of `src` to generate fake amex data and use that to maintain privacy. In `main.py`
it will look like this. 

```python
    ducky = db("mydb.duckdb")
    ducky.connect()
    ducky.drop_tables()
    ducky.create_tables()
    fake = CreditCard("fake", "fakedata/fake_amex.csv", "amex")
    fake.read_file()
    print(fake.cc_data)
    ducky.insert_to_credit(fake.cc_data, fake.card)
```

And then run `main.py`. If you installed DuckDB locally you can connect to it using

`duckdb mydb.duckdb`

And we can query the data. 
```
D select * from Credit
  ;
┌───────┬────────────────┬────────────────────────────────┬───────────────┬─────────────────────┬─────────┬─────────────────────────┐
│  id   │ statement_date │          description           │    amount     │      category       │  card   │       created_at        │
│ int32 │      date      │            varchar             │ decimal(15,2) │       varchar       │ varchar │        timestamp        │
├───────┼────────────────┼────────────────────────────────┼───────────────┼─────────────────────┼─────────┼─────────────────────────┤
│     1 │ 1977-04-08     │ Wiggins and Sons               │       3738.90 │ Fuel                │ fake    │ 2025-01-30 11:25:42.97  │
│     2 │ 1979-12-28     │ Larson, Mcintyre and Williams  │       3915.99 │ Computer Supplies   │ fake    │ 2025-01-30 11:25:42.971 │
│     3 │ 1995-03-02     │ Bolton Ltd                     │        877.08 │ Book Stores         │ fake    │ 2025-01-30 11:25:42.971 │
│     4 │ 2002-08-04     │ Nelson, Davis and Smith        │      -4629.24 │ Office Supplies     │ fake    │ 2025-01-30 11:25:42.971 │
│     5 │ 1985-11-13     │ Tran-Dean                      │      -2188.84 │ General Retail      │ fake    │ 2025-01-30 11:25:42.972 │
│     6 │ 2009-12-24     │ Herring Group                  │         12.07 │ General Attractions │ fake    │ 2025-01-30 11:25:42.972 │
│     7 │ 1979-11-25     │ Hunt, Moore and Taylor         │       3617.31 │ Miscellaneous       │ fake    │ 2025-01-30 11:25:42.972 │
│     8 │ 1998-12-14     │ Rose, Nguyen and Rojas         │        535.19 │ Other Services      │ fake    │ 2025-01-30 11:25:42.972 │
│     9 │ 2011-11-12     │ Gentry Group                   │      -2040.82 │ Department Stores   │ fake    │ 2025-01-30 11:25:42.973 │
│    10 │ 1974-12-13     │ Johnson-Davis                  │      -3592.03 │ Parking Charges     │ fake    │ 2025-01-30 11:25:42.973 │
│    11 │ 1985-08-17     │ Andersen, Woods and Valenzuela │       4324.99 │ Book Stores         │ fake    │ 2025-01-30 11:25:42.973 │
│    12 │ 2018-08-27     │ Contreras, Velasquez and Moore │       3849.47 │ Department Stores   │ fake    │ 2025-01-30 11:25:42.974 │
│    13 │ 1988-05-08     │ French, Myers and Fox          │       -957.94 │ Other Telecom       │ fake    │ 2025-01-30 11:25:42.974 │
│    14 │ 2008-06-30     │ Cummings-Walker                │       3594.99 │ Computer Supplies   │ fake    │ 2025-01-30 11:25:42.974 │
│    15 │ 1995-09-18     │ Cabrera-Stanley                │       4805.67 │ Other Services      │ fake    │ 2025-01-30 11:25:42.974 │
│    16 │ 2022-10-25     │ Martin-Johnson                 │       4344.48 │ General Attractions │ fake    │ 2025-01-30 11:25:42.975 │
│    17 │ 2006-11-22     │ Young-Blake                    │       3300.25 │ Department Stores   │ fake    │ 2025-01-30 11:25:42.975 │
│    18 │ 1975-12-31     │ Stone, Hancock and Campbell    │      -3810.37 │ Electronics Stores  │ fake    │ 2025-01-30 11:25:42.975 │
│    19 │ 1992-01-15     │ Blankenship Ltd                │      -3955.90 │ Pharmacies          │ fake    │ 2025-01-30 11:25:42.975 │
│    20 │ 1977-02-07     │ Owen-Nunez                     │        263.28 │ Electronics Stores  │ fake    │ 2025-01-30 11:25:42.976 │
├───────┴────────────────┴────────────────────────────────┴───────────────┴─────────────────────┴─────────┴─────────────────────────┤
│ 20 rows                                                                                                                 7 columns │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

And there we have it! I plan to add more cards and even using graph libraries for easier visualization. Feel free to follow development on my blog.
[https://jorgesepulveda.dev/](https://jorgesepulveda.dev/)
