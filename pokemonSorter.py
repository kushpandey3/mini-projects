import pandas as pd
df = pd.read_csv('PokemonData.csv')
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
#clean duplicate Pokemon of different forms
df = df.groupby("#").first()
print(f"Dataframe:\n{df}\n")

#Questions to answer: 
#1. find the highest base stat of each type
type1Indices= df.groupby("Type 1")["Total"].idxmax()
type2Indices = df.groupby("Type 2")["Total"].idxmax()
combinedIndices = type1Indices.combine(type2Indices, lambda x, y: x if df.loc[x]["Total"] > df.loc[y]["Total"] else y)
maxTypes = df.loc[combinedIndices][["Name", "Total"]]
maxTypes.index = combinedIndices.index
maxTypes.sort_values(by="Total", inplace = True)
print(f"Here are your strongest Pokes by type:\n{maxTypes}\n")
#2. Strongest non-legendary
strongestNonLegends = df[df["Legendary"]== False].sort_values(by="Total")[["Name", "Total"]].tail(5)
print(f"Here are your strongest Pokes that aren't blessed to be legendaries:\n{strongestNonLegends}\n")
#3. Bulkiest physically/specially/overall
physBulk = (df["Defense"] * df["HP"])
speciallyBulk = (df["Sp. Def"] * df["HP"])
overallBulk = physBulk + speciallyBulk
physBulk.index = speciallyBulk.index = overallBulk.index = df.Name
physBulk.sort_values(inplace=True)
speciallyBulk.sort_values(inplace=True)
overallBulk.sort_values(inplace=True)
print(f"Physically bulkiest: \n {physBulk.tail()}\n")
print(f"Specially bulkiest: \n {speciallyBulk.tail()}\n")
print(f"Overall bulkiest: \n {overallBulk.sort_values().tail()}\n")
#4. Find glass cannons
offensiveRating = (df["Attack"].combine(df["Sp. Atk"], max))*df["Speed"]
#5. Compare trends over generations  - > regression, highest __ 
genData = df.groupby("Generation")[stats].mean()
genData.rename_axis("Stat", axis = "columns", inplace = True)
print(f"Average stats by generation\n{genData}\n")
#CHALLENGE 1: Pokemon similarity index (0 - 1)

#CHALLENGE 2: Which Pokemon allocates its base stats in the best manner?