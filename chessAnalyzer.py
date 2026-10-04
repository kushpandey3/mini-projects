import pandas as pd
df = pd.read_csv("games.csv")
totalEntries = df.shape[0]
#print(df)
#print(df.columns)
#Win rate by color
def colorStats():
    colorInfo = df["winner"].value_counts()
    print(f"White wins {(colorInfo.loc['white']/totalEntries*100):.2f}% of the time here.")
    print(f"Black wins {(colorInfo.loc['black']/totalEntries*100):.2f}% of the time here.")
    print(f"The game is drawn {(colorInfo.loc['draw']/totalEntries*100):.2f}% of the time here.")
#Compare results in rated vs unrated. Turns, resign, tie rate, average rating (rating difference?)
def ratedVsUnrated():
    ratedGames, unratedGames = df[df["rated"]], df[df["rated"]==False]
    numRated, numUnrated = ratedGames.shape[0], unratedGames.shape[0]
    ratedGamesColorInfo, unratedGamesColorInfo = ratedGames["winner"].value_counts(), unratedGames["winner"].value_counts()
    diffInWhiteWin = (ratedGamesColorInfo.loc['white']/numRated*100)-(unratedGamesColorInfo['white']/numUnrated*100)
    print(f"{'White' if diffInWhiteWin>0 else 'Black'} wins {abs(diffInWhiteWin):.2f}% more in rated games compared to unrated ones.")
    diffInTurns = ratedGames["turns"].mean() - unratedGames["turns"].mean()
    print(f"{'Rated' if diffInTurns > 0 else "Unrated"} games last {diffInTurns:.2f} turns longer than {'unrated' if diffInTurns > 0 else 'unrated'} ones.")
    victoryStatusDifferences = (ratedGames["victory_status"].value_counts()/numRated - unratedGames["victory_status"].value_counts()/numUnrated)*100
    for stat, percentage in victoryStatusDifferences.items():
        print(f"The final condition of {stat} happens {abs(percentage):.2f}% more in {'rated' if percentage > 0 else 'unrated'} games.")
    print(f"While the average rating in rated games is {(ratedGames['black_rating'].mean() + ratedGames['white_rating'].mean())/2 :.2f}, it is {(unratedGames['black_rating'].mean() + unratedGames['white_rating'].mean())/2 : .2f} in unrated games.")
#Compare time formats 
def timeFormatStats():
    formatCounts = df["increment_code"].value_counts().sort_values(ascending=False)
    print(f"Your five most common increment codes are: \n{formatCounts.head(5)}")
    #To have reasonable analytics, let's exclude formats with under 100 games of data
    qualifiedData = df[df['increment_code'].isin(formatCounts[formatCounts >= 100].index)]
    formatGroups = qualifiedData.groupby("increment_code")
    winPercentages = (formatGroups['winner'].value_counts()/formatCounts * 100)
    print(f"Here are white's win percentages by time format:\n {winPercentages.xs('white', level='winner').sort_values(ascending=False)}")

    conditionGroups = formatGroups["victory_status"].value_counts()/formatCounts * 100
    statuses = {"resign", "outoftime", "draw", "mate"}
    for stat in statuses:
        print(f"Games ending by {stat}\n {conditionGroups.xs(stat, level='victory_status').sort_values(ascending=False)}")
#Evaluate the most successful openings
#Evaluate the most drawish openings
def openingEvaluation():
    openingCounts = df["opening_name"].value_counts()
    #Exclude openings with less than 20 games of data
    qualifiedOpenings = df[df['opening_name'].isin(openingCounts[openingCounts >= 20].index)]
    openingGroups = qualifiedOpenings.groupby("opening_name")
    winPercentages = openingGroups['winner'].value_counts()/openingCounts * 100
    print(f"The most succesful openings for white are: \n {winPercentages.xs('white', level='winner').nlargest(5)}")
    print(f"The most succesful openings for black are: \n {winPercentages.xs('black', level='winner').nlargest(5)}")
    print(f"The most drawish openings are: \n {winPercentages.xs('draw', level='winner').nlargest(5)}")
#colorStats()
#ratedVsUnrated()
#timeFormatStats()
#openingEvaluation()