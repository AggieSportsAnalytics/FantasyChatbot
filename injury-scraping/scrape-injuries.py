from bs4 import BeautifulSoup
import pandas as pd

html = open('NFL Injury Status - 2023 Season - ESPN.html')
soup = BeautifulSoup(html, 'html.parser')

data = []

tables = soup.find_all('table', class_='Table')

for table in tables:
    temp = []

    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        player_name = cells[0].find('a').text.strip()
        position = cells[1].text.strip()
        status = cells[3].find('span').text.strip()
        injury_report = cells[4].text.strip()

        player_info = {
                'Player Name': player_name,
                'Position': position,
                'Status': status,
                'Injury Report': injury_report
            }

        temp.append(player_info)

    data.append(temp)

df = pd.DataFrame()
for s in data:
    df = pd.concat([df, pd.DataFrame(s)])

df.to_csv('injuryreports.csv', index=False)