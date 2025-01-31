from faker import Faker
import pandas as pd
import random

fake = Faker()
amexCategories = ['Merchandise & Supplies-General Retail',
 'Business Services-Office Supplies',
 'Merchandise & Supplies-Electronics Stores',
 'Merchandise & Supplies-Internet Purchase',
 'Fees & Adjustments-Fees & Adjustments',
 'Communications-Cable & Internet Comm',
 'Merchandise & Supplies-Computer Supplies',
 'Merchandise & Supplies-Mail Order','Transportation-Auto Services',
 'Merchandise & Supplies-Department Stores',
 'Merchandise & Supplies-Furnishing','Business Services-Internet Services',
 'Transportation-Fuel','Restaurant-Restaurant',
 'Business Services-Other Services','Communications-Other Telecom',
 'Merchandise & Supplies-Groceries',
 'Merchandise & Supplies-Wholesale Stores',
 'Merchandise & Supplies-Hardware Supplies',
 'Merchandise & Supplies-Pharmacies','Restaurant-Bar & Café',
 'Merchandise & Supplies-Clothing Stores',
 'Business Services-Mailing & Shipping',
 'Business Services-Professional Services',
 'Transportation-Parking Charges','Entertainment-Associations',
 'Other-Miscellaneous','Merchandise & Supplies-Book Stores',
 'Entertainment-General Attractions','Other-Charities']


num_rows = 1000

data = {
    "Date" : [fake.date(pattern="%m/%d/%Y") for _ in range(num_rows)],
    "Description": [fake.company() for _ in range(num_rows)],
    "Amount": [round(fake.random.uniform(-5000,5000),2) for _ in range(num_rows)],
    "Category": [random.choice(amexCategories) for _ in range(num_rows)]
}
df = pd.DataFrame(data)
df.to_csv("f_red.csv", index=False)
