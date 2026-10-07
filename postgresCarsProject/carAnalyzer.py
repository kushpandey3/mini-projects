import pandas as pd, psycopg, os
from dotenv import load_dotenv
#clean with pandas
def cleanData():
    df = pd.read_csv("cars.csv").dropna()
    #print(df.columns)
    #fix horsepower, total speed (kph) -> total speed (mph), performance, price, torque, seats, cc/battery capacity (watch for exceptions)
    df["HorsePower"] = df["HorsePower"].apply(horsepowerSwitcher)
    df["Total Speed"] = df["Total Speed"].apply(lambda x: round(int(x.split()[0])*.621371))
    df["Performance(0 - 100 )KM/H"] = df["Performance(0 - 100 )KM/H"].apply(lambda x : float(x.split()[0] if isinstance(x, str) else x))
    df["Cars Prices"] = df["Cars Prices"].apply(priceSwitcher)
    df["Torque"] = df["Cars Prices"].apply(lambda x: int(x.split()[0].replace(",","") if isinstance(x, str) else x))
    df.rename(columns={"Total Speed":"Top Speed","HorsePower":"Horse Power", "Performance(0 - 100 )KM/H":"0-100 kph"}, inplace=True)
    print(df["Horse Power"], df["Top Speed"], df["0-100 kph"], df["Cars Prices"], df["Torque"], sep ="\n")
    return df
def horsepowerSwitcher(hp):
    if "-" in hp:
        hps = hp.split("-") 
        hps[1] = int(hps[1].split()[0])
        hp = (int(hps[0])+hps[1])//2
        return hp
    if "~" in hp:
        hp = hp[1]
    if "Up to" in hp:
        hp = hp[hp.find("Up to") + 6:]
    return int(hp.split()[0].replace(",",""))

def priceSwitcher(price):
    price = price.strip()
    if "-" in price:
        prices = price.split("-") 
        prices[0], prices[1] = prices[0].strip()[1:].replace(",", "").strip() , prices[1].strip()[1:].replace(",", "")
        return (int(prices[0]) + int(prices[1]))//2
    if "–" in price:
            prices = price.split("–") 
            prices[0], prices[1] = prices[0].strip()[1:].replace(",", "").strip() , prices[1].strip()[1:].replace(",", "")
            return (int(prices[0]) + int(prices[1]))//2
    if "/" in price:
                prices = price.split("/") 
                prices[0], prices[1] = prices[0].strip()[1:].replace(",", "").strip() , prices[1].strip()[1:].replace(",", "")
                return (int(prices[0]) + int(prices[1]))//2
    print(price)
    return int(price.split()[0][1:].replace(",", ""))


#load to sql
def initizeDatabase():
    conn = psycopg.connect(host=os.getenv("DB_HOST"), port = os.getenv("DB_PORT"), user=os.getenv("DB_USER"), db_name=os.getenv("DB_NAME"))
    cursor = conn.cursor()
    with open("cars.csv") as f:
        cursor.execute("CREATE TABLE Cars (Company Names TEXT, Cars Names TEXT, Engines TEXT, CC/Battery Capacity TEXT, HorePower )")
        for line_num, line in enumerate(f):
            rowData = line.split(",")
            if(line_num==0):
                for val in rowData:
                    cursor.execute("CREATE TABLE Cars ()", )
    cursor.close()
    conn.close()
#take out from sql to pandas
#analyze with pandas
            

#initizeDatabase()
print(cleanData())

