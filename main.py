## main.py
import redataprocessing.sreality as sreality
import sqlite3
import pandas as pd
from datetime import datetime
import os

os.makedirs("data", exist_ok=True)
db_path = "data/sreality_data.db"
conn = sqlite3.connect(db_path)

all_offers = []
all_details = []

category_mains = list(sreality.category_main_dict.keys())
category_types = list(sreality.category_type_dict.keys())
region = "Hlavní město Praha"  # Prague only

for main_cat in category_mains:
    for type_cat in category_types:
        print(f"Fetching: category_main='{main_cat}', category_type='{type_cat}', region='{region}'")
        try:
            offers = sreality.get_re_offers(db_path, main_cat, type_cat, region)
            if offers:
                all_offers.extend(offers)

                details = sreality.get_re_offers_description(offers)
                if details:
                    all_details.extend(details)
                else:
                    print(f"No details returned for offers in {main_cat} / {type_cat} / {region}")
            else:
                print(f"No offers returned for {main_cat} / {type_cat} / {region}")
        except Exception as e:
            print(f"Error for {main_cat} / {type_cat} / {region}: {e}")

# Convert to DataFrames
df_offers = pd.DataFrame(all_offers)
df_offers["scrape_date"] = datetime.now().strftime("%Y-%m-%d")

if all_details:
    df_details = pd.DataFrame(all_details)
    df_details["scrape_date"] = datetime.now().strftime("%Y-%m-%d")
    df_details.to_sql("details", conn, if_exists="append", index=False)

# Save offers to SQLite DB
df_offers.to_sql("offers", conn, if_exists="append", index=False)

conn.close()
print("Finished fetching all listings for Prague.")
