import pandas as pd, psycopg, os
from dotenv import load_dotenv
#clean with pandas
def cleanData():
    df = pd.read_csv("postgresCarsProject/cars.csv").dropna().drop(columns=["CC/Battery Capacity"])
    #print(df.columns)
    #fix horsepower, total speed (kph) -> total speed (mph), performance, price, torque, seats (watch for exceptions)
    df["HorsePower"] = df["HorsePower"].apply(horsepowerSwitcher)
    df["Total Speed"] = df["Total Speed"].apply(lambda x: round(int(x.split()[0])*.621371))
    df["Performance(0 - 100 )KM/H"] = df["Performance(0 - 100 )KM/H"].apply(lambda x : float(x.split()[0] if isinstance(x, str) else x))
    df["Cars Prices"] = df["Cars Prices"].apply(priceSwitcher)
    df["Torque"] = df["Torque"].apply(torqueSwitcher)
    df["Seats"] = df["Seats"].apply(lambda x: evalSeats(x))
    df.rename(columns={"Company Names":"Brand", "Cars Names":"Model", "Total Speed":"Top Speed","HorsePower":"Horse Power", "Performance(0 - 100 )KM/H":"0-100 kph", "Cars Prices": "Price"}, inplace=True)
    #print(df["Horse Power"], df["Top Speed"], df["0-100 kph"], df["Cars Prices"], df["Torque"], df["Seats"], sep ="\n")
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
    return int(price.split()[0][1:].replace(",", ""))

def evalSeats(seats):
     if "+" in seats:
        splitted = seats.split("+")
        return int(splitted[0]) + int(splitted[1])
     if "-" in seats:
        return int(seats[seats.find("-")+1:])
     if "–" in seats:
             return int(seats[seats.find("–")+1:])
     return int(seats)

def torqueSwitcher(torque):
    if "-" in torque:
        splitted = torque.strip().replace(",", "").split("-")
        return (int(splitted[0]) + int(splitted[1].strip()[:splitted[1].strip().find(" ")]))//2
    if "+" in torque:
        return int(torque[:torque.find("+")].strip().replace(",", ""))
    return int(torque.replace(",","").split()[0])
     
#load to sql
def initializeDatabase():
    conn = psycopg.connect(host=os.getenv("DB_HOST"), port = os.getenv("DB_PORT"), user=os.getenv("DB_USER"), dbname=os.getenv("DB_NAME"))
    cursor = conn.cursor()
    df = cleanData()
    try:
        cursor.execute("CREATE TABLE Cars (Brand TEXT, Model TEXT, Engines TEXT, HorsePower INT, TopSpeed INT, AccelTime FLOAT, Price INT, FuelTypes TEXT, Seats INT, Torque INT)")
        for index in range(df.shape[0]):
            row = df.iloc[index]
            cursor.execute("""INSERT INTO Cars (Brand, Model, Engines, HorsePower, TopSpeed, AccelTime, Price, FuelTypes, Seats, Torque) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (row["Brand"], row["Model"], row["Engines"], row["Horse Power"], row["Top Speed"], 
            row["0-100 kph"], row["Price"], row["Fuel Types"], row["Seats"], row["Torque"]))
        cursor.execute("SELECT Brand FROM Cars")
        print(cursor.fetchall())
        conn.commit()
        print("Successfully done")
    except Exception as e:
        conn.rollback()
        print("Had to roll back:", e)
    finally:
        cursor.close()
        conn.close()
#take out from sql to pandas
def restoreDataframe():
    conn = psycopg.connect(host=os.getenv("DB_HOST"), port = os.getenv("DB_PORT"), user=os.getenv("DB_USER"), dbname=os.getenv("DB_NAME"))
    cursor = conn.cursor()
    try:
        return pd.read_sql("SELECT * FROM Cars", conn)
    except Exception as e:
         print("Failed to read SQL:", e)
    finally:
         cursor.close()
         conn.close()

#analyze with pandas
def analyzeData():
    df = restoreDataframe()
    cheapestLuxuryBrandCar(df)
    accelMerchants(df)
    hpToCostRatio(df)

def cheapestLuxuryBrandCar(df):
    meanPrices = df.groupby("brand")["price"].mean().sort_values()
    luxuryBrandCars = df[df["brand"].isin(meanPrices.tail().index)].sort_values(by="price")
    print(luxuryBrandCars.head())

def accelMerchants(df):
    merchants = df.loc[(df["acceltime"]*df["topspeed"]).sort_values().index]
    print(merchants[["brand", "model", "acceltime", "topspeed"]])

def hpToCostRatio(df):
    merchants = df.loc[(df["horsepower"]/df["price"]).sort_values(ascending=False).index]
    print(merchants[["brand", "model", "horsepower", "price"]].head())

#initizeDatabase()
#print(cleanData())
#initializeDatabase()
#restoreDataframe()
analyzeData()

