import sqlite3

# connect to the SQLite Database
conn = sqlite3.connect('zillow_data.db')
cursor = conn.cursor()

# remove any listings where there is no bedroom or bathroom data
cursor.execute("DELETE FROM listings WHERE bedrooms IS NULL OR bathrooms IS NULL")
cursor.execute("DELETE FROM listings WHERE bedrooms = 0 OR bathrooms = 0")

# remove any listings where there is no price data
cursor.execute("DELETE FROM listings WHERE price IS NULL")
cursor.execute("DELETE FROM listings where price = 0")

# remove any listings where there is no (living and lot) area data
cursor.execute("DELETE FROM listings WHERE area IS NULL")
cursor.execute("DELETE FROM listings where area = 0")
cursor.execute("DELETE FROM listings WHERE lotAreaValue IS NULL or lotAreaUnit IS NULL")
cursor.execute("DELETE FROM listings where lotAreaValue = 0")

# update taxAssessedValue to be the price column where it is 0 or null
cursor.execute("""
               UPDATE listings 
               SET taxAssessedValue = price 
               WHERE taxAssessedValue IS NULL OR taxAssessedValue = 0
               """)


# updating any entries with null latitude and longitude

# create a temporary table to map zip codes with latitude and longitude values
cursor.execute("""
               CREATE TEMP TABLE valid_lat_long AS
               SELECT addressZipcode, latitude, longitude
               FROM listings
               WHERE (latitude IS NOT NULL AND longitude IS NOT NULL) OR (latitude != 0 AND longitude != 0)
               """)

# update listings' null latitude and longitude values by randomly choosing them from addresses with the same zip code
cursor.execute("""
               UPDATE listings
               SET latitude = (
                   SELECT latitude
                   FROM valid_lat_long
                   WHERE valid_lat_long.addressZipcode = listings.addressZipcode
                   ORDER BY RANDOM()
                   LIMIT 1
               ),
               longitude = (
                   SELECT longitude
                   FROM valid_lat_long
                   WHERE valid_lat_long.addressZipcode = listings.addressZipcode
                   ORDER BY RANDOM()
                   LIMIT 1
               )
               WHERE latitude IS NULL OR longitude IS NULL OR latitude = 0 OR longitude = 0
               """)

cursor.execute("""DROP TABLE valid_lat_long""")

conn.commit()
conn.close()
print("Entries have been cleaned up and tax assessed values updated.")