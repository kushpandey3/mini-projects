import pandas as pd
df = pd.read_csv('PokemonData.csv')
print(f"Dataframe:\n{df}\n")
#Questions to answer: 
#1. find the highest base stat of each type
#2. Strongest non-legendary
#3. Pokemon that have way too balanced attack/spatk
#4. format mega's names
#5. Bulkiest physically/specially
#6. Find glass cannons
#7. Compare trends over generations  - > regression, highest __ 
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
genData = df.groupby("Generation")[stats].mean()
genData.rename_axis("Stat", axis = "columns", inplace = True)
print(f"Average stats by generation\n{genData}\n")