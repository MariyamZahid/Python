import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


master_cafe_sales = pd.read_csv(r"C:\Users\HP\Downloads\dirty_cafe_sales.csv")

cafe_sales = master_cafe_sales.copy()

print(cafe_sales.info())

cafe_sales["Transaction ID"] = cafe_sales["Transaction ID"].astype(str).str.strip()
cafe_sales["Item"] = cafe_sales["Item"].replace(["ERROR","UNKNOWN","nan"],pd.NA).str.strip().astype("category")
cafe_sales["Quantity"] = pd.to_numeric(cafe_sales["Quantity"], errors="coerce")
cafe_sales["Price Per Unit"] = pd.to_numeric(cafe_sales["Price Per Unit"], errors="coerce")
cafe_sales["Total Spent"] = pd.to_numeric(cafe_sales["Total Spent"], errors="coerce")
cafe_sales["Payment Method"] = cafe_sales["Payment Method"].replace(["ERROR","UNKNOWN","nan"],pd.NA).str.strip().astype("category")
cafe_sales["Location"] = cafe_sales["Location"].replace(["UNKNOWN","ERROR","NaN"],pd.NA).str.strip().astype("category")
cafe_sales["Transaction Date"] = pd.to_datetime(cafe_sales["Transaction Date"], errors="coerce")

print(cafe_sales.info())

cafe_sales["Price Per Unit"] = cafe_sales["Price Per Unit"].fillna(cafe_sales["Total Spent"]/cafe_sales["Quantity"])
cafe_sales["Price Per Unit"] = cafe_sales["Price Per Unit"].fillna(cafe_sales.groupby("Item", observed = True)["Price Per Unit"].transform("mean"))
cafe_sales["Price Per Unit"] = cafe_sales["Price Per Unit"].fillna(cafe_sales["Price Per Unit"].mode()[0])

# Groupby unique prices
unique_price_map = cafe_sales.groupby("Item", observed = False)["Price Per Unit"].unique()
# Filter items with only one price
single_price_items = {item: prices[0] for item, prices in unique_price_map.items() if len(prices) == 1}
# Reverse mapping: Price -> Item
price_to_item = {price: item for item, price in single_price_items.items()}
# Fill missing Item where Price exists
mask = cafe_sales["Item"].isna() & cafe_sales["Price Per Unit"].notna()
cafe_sales.loc[mask, "Item"] = cafe_sales.loc[mask, "Price Per Unit"].map(price_to_item)
cafe_sales["Item"] = cafe_sales["Item"].fillna(cafe_sales["Item"].mode()[0])


#cafe_sales["Quantity"] = cafe_sales["Quantity"].fillna(cafe_sales["Total Spent"]/cafe_sales["Price Per Unit"])
cafe_sales["Quantity"] = cafe_sales["Quantity"].fillna(cafe_sales["Quantity"].median())
cafe_sales["Total Spent"] = cafe_sales["Quantity"]*cafe_sales["Price Per Unit"]

cafe_sales["Transaction Date"] = cafe_sales["Transaction Date"].ffill()


cafe_sales["Payment Method"] = cafe_sales["Payment Method"].fillna(cafe_sales["Payment Method"].mode()[0])
cafe_sales["Location"] = cafe_sales["Location"].fillna(cafe_sales["Location"].mode()[0])



cafe_sales_summary = pd.DataFrame({
    "Total_count": len(cafe_sales),
    "null count": cafe_sales.isnull().sum(),
    "Non_null count": cafe_sales.count(),
    "unique count": cafe_sales.nunique()
})


pd.set_option("display.max_column",None)



print(cafe_sales_summary)



cafe_sales.to_csv(r"C:\Users\HP\Downloads\clean_cafe_sales_data.csv", index=False)

