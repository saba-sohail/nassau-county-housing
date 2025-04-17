import sqlite3
import pandas as pd

# create SQLite Database and Table
conn = sqlite3.connect('zillow_data.db')
cursor = conn.cursor()

# check if the table already exists and drop it if it does (to avoid errors)
cursor.execute("DROP TABLE IF EXISTS listings")

# create the table with the specified columns
cursor.execute("""
               CREATE TABLE listings 
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               address TEXT,
               addressCity TEXT,
               addressState TEXT,
               addressZipcode TEXT,
               bedrooms INTEGER,
               bathrooms INTEGER,
               area REAL,
               daysOnZillow INTEGER,
               price INTEGER,
               lotAreaValue REAL,
               lotAreaUnit TEXT,
               taxAssessedValue INTEGER,
               homeStatus TEXT,
               latitude REAL,
               longitude REAL)
               """)

# commit the changes
conn.commit()

# read the CSV file
df = pd.read_csv('dataset_2025-04-16_01-47-15-990.csv')

# select only the relevant columns
relevant_columns = [
    'address', 
    'addressCity', 
    'addressState', 
    'addressZipcode', 
    'beds', 
    'baths', 
    'area', 
    'hdpData/homeInfo/daysOnZillow', 
    'hdpData/homeInfo/price', 
    'hdpData/homeInfo/lotAreaValue', 
    'hdpData/homeInfo/lotAreaUnit', 
    'hdpData/homeInfo/taxAssessedValue', 
    'hdpData/homeInfo/homeStatus', 
    'hdpData/homeInfo/latitude', 
    'hdpData/homeInfo/longitude', 
]

# rename columns to match the table schema
df = df[relevant_columns].rename(columns={
    'beds': 'bedrooms',
    'baths': 'bathrooms',
    'hdpData/homeInfo/daysOnZillow': 'daysOnZillow',
    'hdpData/homeInfo/price': 'price',
    'hdpData/homeInfo/lotAreaValue': 'lotAreaValue',
    'hdpData/homeInfo/lotAreaUnit': 'lotAreaUnit',
    'hdpData/homeInfo/taxAssessedValue': 'taxAssessedValue',
    'hdpData/homeInfo/homeStatus': 'homeStatus',
    'hdpData/homeInfo/livingArea': 'area',
    'hdpData/homeInfo/latitude': 'latitude',
    'hdpData/homeInfo/longitude': 'longitude',
    'carouselPhotos/0/url' : 'photoUrl'
})

# insert data into the SQLite table
df.to_sql('listings', conn, if_exists='append', index=False)

conn.commit()
conn.close()
print("Data has been successfully inserted into the database.")