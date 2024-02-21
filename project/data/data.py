import json
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def main():
    player_data = {}
    ts_proj = pd.DataFrame()
    ts_total = pd.DataFrame()
    num_weeks = 18

    # Loop through each week
    for week in range(1, num_weeks + 1):
        file_name = f'week{week}.json'
        week_data = read_json_file(file_name)
        week_data_filter = week_data["data"]

        # Process each player in the week
        for player in week_data_filter:
            name = player.get('PLAYER NAME', '')
            team = player.get('PLAYER TEAM', '')
            position = player.get('PLAYER POSITION', '')
            proj = player.get('PROJ', 0)
            total = player.get('TOTAL', 0)

            # Convert PROJ and TOTAL to float, handle empty or invalid values
            try:
                proj = float(proj) if proj else 0
                total = float(total) if total else 0
            except ValueError:
                proj = 0
                total = 0
            
            #add data for player by week to time series data      
            ts_proj.loc[week, name] = proj
            ts_total.loc[week, name] = total

            # Accumulate data for each player
            if name not in player_data:
                player_data[name] = {'team': team, 'position': position, 'proj': 0, 'total': 0, 'count': 0}
            player_data[name]['proj'] += proj
            player_data[name]['total'] += total
            player_data[name]['count'] += 1
    
    # replace nan values
    ts_total.fillna(0, inplace=True)
    ts_proj.fillna(0, inplace=True)

    # reset index to datetime format
    ts_proj.index = pd.date_range(start='2024-01-01', periods=len(ts_proj), freq='W')
    ts_total.index = ts_proj.index

    # Calculate averages and prepare the final data
    final_data = []
    for name, data in player_data.items():
        # calculate optimal autoregressive, differencing, moving average components
        # proj_auto = auto_arima(ts_proj[name], suppress_warnings=True, trace=False)

        proj_arima = ARIMA(ts_proj[name], order=(1, 0, 1), enforce_invertibility=True, enforce_stationarity=True).fit()
        total_arima = ARIMA(ts_total[name], order=(1, 0, 1), enforce_invertibility=True, enforce_stationarity=True).fit()


        if data['count'] > 0:
            avg_proj = data['proj'] / data['count']
            avg_total = data['total'] / data['count']
            final_data.append({
                'name': name,
                'team': data['team'],
                'position': data['position'],
                'avg_proj': avg_proj,
                'avg_total': avg_total,
                'proj_trend_influence': proj_arima.arparams[0],
                'proj_variation_sensitivity': proj_arima.maparams[0],
                'total_trend_influence': total_arima.arparams[0],
                'total_variation_sensitivity': total_arima.maparams[0]
            })

    output_file = 'final_data.json'
    with open(output_file, 'w') as file:
        json.dump(final_data, file, indent=4)

    print(f"Data successfully written to {output_file}")

    # # Output the final data
    # for player in final_data:
    #     print(player)

if __name__ == "__main__":
    main()
