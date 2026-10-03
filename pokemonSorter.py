import pandas as pd
#handle ties
df = pd.read_csv('PokemonData.csv')
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Total"]
#clean duplicate Pokemon of different forms and optimize type format 
df = df.groupby("#").first()  
def displayCleanedData():
    print(f"Dataframe:\n{df}\n")
#Questions to answer:
#Add minimum base stat to qualify for awards??
#1. find the highest base stat of each type
def highestBaseStat():
    typeList = df.melt(id_vars=["Name", "Total"], value_vars = ["Type 1", "Type 2"], value_name="Type").drop(columns=["variable"]).dropna(subset=["Type"])
    maxes = typeList.loc[typeList.groupby("Type")["Total"].idxmax()].set_index("Type")
    print(f"Here are your strongest Pokes by type:\n{maxes}\n")
#2. Strongest non-legendary
def strongestNonLegendary():
    nonLegends = df[df["Legendary"]==False]
    #there may be ties 
    minBaseStat = nonLegends.nlargest(5, "Total").iloc[-1]["Total"]
    strongestNonLegends = nonLegends[nonLegends["Total"] >= minBaseStat].sort_values(by="Total", ascending=False)
    print(f"Here are your strongest Pokes that aren't blessed to be legendaries:\n{strongestNonLegends}\n")
#3. Bulkiest physically/specially/overall
def bulkiest():
    #upgrade efficiency n-largest > sort
    physBulk, specBulk = (df["Defense"] * df["HP"]), (df["Sp. Def"] * df["HP"])
    overallBulk = physBulk + specBulk
    physBulk.index = specBulk.index = overallBulk.index = df.Name
    minPhysBulk, minSpecBulk, minOverallBulk = physBulk.nlargest(5).iloc[-1], specBulk.nlargest(5).iloc[-1], overallBulk.nlargest(5).iloc[-1]
    print(f"Physically bulkiest: \n {physBulk[physBulk >= minPhysBulk].sort_values(ascending=False)}\n")
    print(f"Specially bulkiest: \n {specBulk[specBulk >= minSpecBulk].sort_values(ascending=False)}\n")
    print(f"Overall bulkiest: \n {overallBulk[overallBulk >= minOverallBulk].sort_values(ascending=False)}\n")
#4. Find glass cannons 
def glassCannons():
    qualifiedPokemon = df[df["Total"] > 450]
    offensiveRating = (qualifiedPokemon["Attack"].combine(qualifiedPokemon["Sp. Atk"], max))*qualifiedPokemon["Speed"]
    defensiveRating = (qualifiedPokemon["Defense"] + qualifiedPokemon["Sp. Def"]) * qualifiedPokemon["HP"]
    offensiveRating.index = defensiveRating.index = qualifiedPokemon.Name
    glassCannonRating = offensiveRating/defensiveRating #fix 
    print(f"Your biggest glass cannons are:\n{glassCannonRating.sort_values(ascending=False).head(10)}\n")
#5. Compare trends over generations
def generationalTrends():
    genData = df.groupby("Generation")[stats].mean()
    genData.rename_axis("Stat", axis = "columns", inplace = True)
    print(f"Average stats by generation\n{genData}\n")
    for stat in stats:
        print(f"Generation with highest {stat}: {genData[stat].idxmax()}")
    #name strongest, fastest, bulkiest, etc. 
    
#CHALLENGE 1: Pokemon similarity index (0 - 1)

def closestPokemon(pokedexNum):
    similarityScores = df["HP"] * df.loc[pokedexNum]["HP"]
    squaredSums = df["HP"]**2; 
    currSum = df.loc[pokedexNum]["HP"]**2; 
    for stat in stats[1:]:
        similarityScores += df[stat] * df.loc[pokedexNum][stat]
        squaredSums += df[stat]**2; 
        currSum += df.loc[pokedexNum][stat]**2; 
    magnitudeSimilarity = df["Total"]/df.loc[pokedexNum]["Total"]
    magnitudeSimilarity = magnitudeSimilarity.apply(lambda x: x if x <= 1 else 1/x)
    similarityScores /= squaredSums**.5 * currSum**.5
    similarityScores *= magnitudeSimilarity
    similarityScores.sort_values(inplace=True, ascending = False)
    closestPokemon = df.loc[similarityScores.head().index]
    closestPokemon["Similarity Index"] = similarityScores.head()
    print(closestPokemon)

#CHALLENGE 2: Which Pokemon are the most specialized?
def bestSpecialized():
    qualifiedPokemon = df[df["Total"] > 450]
    attackDiff = abs(qualifiedPokemon["Attack"] - qualifiedPokemon["Sp. Atk"])
    offensiveRating = (qualifiedPokemon["Attack"].combine(qualifiedPokemon["Sp. Atk"], max))*qualifiedPokemon["Speed"]
    defensiveRating = (qualifiedPokemon["Defense"] + qualifiedPokemon["Sp. Def"]) * qualifiedPokemon["HP"]/2
    offensiveRating.index = defensiveRating.index = attackDiff.index = qualifiedPokemon.Name
    allocatingRating = abs(offensiveRating-defensiveRating) + attackDiff*50
    print(attackDiff)
    print(f"Your most specialized Pokemon are:\n{allocatingRating.sort_values(ascending=False).head(10)}\n")
##Call funcs here
