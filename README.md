### 🏁 AI-powered Chatbot for draft and trade guidance in Fantasy Football and Basketball

Over 60 million Americans play fantasy sports every year. HIKE is a chatbot for amazing personalized guidance in Fantasy Football and Basketball. It provides conversational advice using a combination of time series analysis, score projections, and LLM-powered sentiment analysis. HIKE is the ultimate algorithm for Fantasy players to make decisions on drafting and trading players.

# 🔑 Key Features

## Comparing player statistics

This project is able to compare players of a similar contract range across different statistics.
<img width="990" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/e903d94a-e306-46fc-83eb-0d8741213365">

**This is a graph of all the supermax players in the NBA sorted from highest to lowest contract and their Points Per Game**

<img width="944" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/a3509f38-9ced-4f14-9980-eef83139ac4f">

**This is a graph of Chet Holmgren's Rebounds Per Game compared to other players of a similar contract**

<img width="952" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/6eb6bbbe-6245-49ad-b66e-f16773c6c402">

**This is a graph of the Player Efficiency ratings of the Washington Wizards sorted by salary**

From all of this info it is easy to determine which players are over and under performing their contracts.

<img width="884" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/d929649d-3b78-4cc0-8911-01a6a7f79549">

**This image has the information on the over and underachieving players on the Wizards**

### 💻 Code

To determine the over and underachieveing players we calculated the mean PER for each salary tier from max and supermax contracts down to minimum contracts. We then calculated the standard deviation for the each tier. Any player more than 1SD above the mean was considered to be outperforming his contract and vise versa.

```py
def standardDeviation(superAvg, maxAvg, minAvg, t1, t2, t3, t4, t5, t6, superCount, maxCount, minCount, c1, c2, c3, c4, c5, c6, allPlayers, labelVal):
    sdSuper, sdMax, sdMin, sd1, sd2, sd3, sd4, sd5, sd6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    counterSuper, counterMax, counterMin, counter1, counter2, counter3, counter4, counter5, counter6 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for player in allPlayers:
        if player.isSupermax:
            counterSuper = counterSuper + (player.PER - superAvg)**2
        elif player.ismax:
            counterMax = counterMax + (player.PER - maxAvg)**2
        elif player.isMin:
            counterMin = counterMin + (player.PER - minAvg)**2
        elif 31830356 > player.salary >= 25000000:
            counter1 = counter1 + (player.PER - t1)**2
        elif 25000000 > player.salary >= 20000000:
            counter2 = counter2 + (player.PER - t2)**2
        elif 20000000 > player.salary >= 15000000:
            counter3 = counter3 + (player.PER - t3)**2
        elif 15000000 > player.salary >= 10000000:
            counter4 = counter4 + (player.PER - t4)**2
        elif 10000000 > player.salary >= 5000000:
            counter5 = counter5 + (player.PER - t5)**2
        elif 5000000 > player.salary:
            counter6 = counter6 + (player.PER - t6)**2
 ...
```

There is more to this function but it essentially calculates the standard deviation for PER of each salary tier.

## Comparing Salary distrbution from teams

<img width="1067" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/37deff39-58b0-4209-b2b7-aed2251b5902">

**This image has the information on each of the following factors we used to distribute salary on the Thunder**

<img width="1064" alt="image" src="https://github.com/AggieSportsAnalytics/NBASalaryAnalysis/assets/68085422/85b3abc7-092a-469d-ab35-d8903fc607cb">

**This image has the information on each of the following factors we used to distribute salary on the Lakers**

One Way we categorized our data was based on a Player's position. We grouped the total salaries of Guards, Forwards and Centers and divided by the total team salaries. After calculating that percentage, we plotted these values on a pie chart for specific teams.

### 💻 Code

Merging and distributing the data into different groups.

```py
if 'Player' in Salary.columns and 'Player' in Roster.columns:
    merged_data = pd.merge(Roster, Salary, on='Player', how='inner')
else:
    print("Required columns not found in the data.")
    return

    # Process merged data for salary
merged_data['Salary'] = merged_data['Salary'].replace('[\$,]', '', regex=True).astype(int)

total_salary = merged_data['Salary'].sum()
PosVal = {
    "Guard": merged_data.loc[merged_data['Pos'].isin(['PG', 'SG']), 'Salary'].sum(),
    "Forward": merged_data.loc[merged_data['Pos'].isin(['SF', 'PF']), 'Salary'].sum(),
    "Center": merged_data.loc[merged_data['Pos'] == 'C', 'Salary'].sum()
}
# Filter out positions with no salary
PosVal = {k: v for k, v in PosVal.items() if v > 0}
```

After obtaining multiple csv files containing a player's salary and stats, we merged them all into one singular dataframe. From this dataframe, I seperated the data into the PosVal dictionary that contains the three different positions and the sum of all the Salarys towards the players who play that position respectively.

Another criteria was if a player is a starter or a bench player. We determine player roles (starters and bench) based on predefined criteria. It calculates and compares the total salary of starters and bench players. This provides insights into the financial structure of the team based on player roles.

### 💻 Code

For retrieving and graphing data of player salary, team standings, and player stats, we use Pandas and Matplotlib libraries.

```py
stats_file = f"Data/{team_name}PlayerStats.csv"
salary_file = f"Data/{team_name}Salary.csv"
standings_file = "NBAStandings.csv"

stats_data = pd.read_csv(stats_file)
salary_data = pd.read_csv(salary_file)
standings_data = pd.read_csv(standings_file)
```

\
Then after merging all the data together, we calculate the salaries.

```py
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n(${v:,})'.format(p=pct, v=val)
    return my_format
```

\
Finally, we plot a pie chart using the Matplotlib.

```py
plt.figure(figsize=(10, 10))
plt.pie(total_salary, labels=total_salary.index, autopct=autopct_format(total_salary), colors=colors)
plt.title(f'Salary Distribution based on Starters and Bench for {team_record["Team"]}\nTotal Salary: ${total_team_salary:,.0f}\n{team_record_str}')
plt.show()
```

### 💻 Code

For retrieving and graphing data of player salary, team standings, and player stats, we use Pandas and Matplotlib libraries.

```py
stats_file = f"Data/{team_name}PlayerStats.csv"
salary_file = f"Data/{team_name}Salary.csv"
standings_file = "NBAStandings.csv"

stats_data = pd.read_csv(stats_file)
salary_data = pd.read_csv(salary_file)
standings_data = pd.read_csv(standings_file)
```

\
To compare salaries based upon age groups, we chose four age groups which accurately depict the different types of contracts in the NBA. The first age group, 23 and under, represents players on rookie contracts. Next, the age groups between 23-28 and 29-33 represent most NBA players' next two major contracts. Finally, the age group 33+ represents the older players remaining in the league, often operating on league minimum contracts. The salary analyzer calculates what percent of each team’s total salary cap falls under each age group.
From the "Salary" team csv files files inputted, we then separated the players by age group.

```py
# Age group processing
age_groups = {'Under 23': 0, '23-28': 0, '29-33': 0, 'Over 33': 0}
for _, row in merged_data.iterrows():
    age = row['Age']
    salary = row['2023-24']
    if age < 23:
        age_groups['Under 23'] += salary
    elif 23 <= age <= 28:
        age_groups['23-28'] += salary
    elif 29 <= age <= 33:
        age_groups['29-33'] += salary
    else:
        age_groups['Over 33'] += salary
# Filter out age groups with no salary
age_groups = {k: v for k, v in age_groups.items() if v > 0}
```

\
Then after merging all the data together, we calculate the salaries.

```py
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n(${v:,})'.format(p=pct, v=val)
    return my_format
```

\
Finally, we plot a pie chart using the Matplotlib.

```py
plt.figure(figsize=(10, 10))
plt.pie(total_salary, labels=total_salary.index, autopct=autopct_format(total_salary), colors=colors)
plt.title(f'Salary Distribution based on Starters and Bench for {team_record["Team"]}\nTotal Salary: ${total_team_salary:,.0f}\n{team_record_str}')
plt.show()
```
