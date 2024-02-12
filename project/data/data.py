import json

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def main():
    player_data = {}
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

            # Accumulate data for each player
            if name not in player_data:
                player_data[name] = {'team': team, 'position': position, 'proj': 0, 'total': 0, 'count': 0}
            player_data[name]['proj'] += proj
            player_data[name]['total'] += total
            player_data[name]['count'] += 1

    # Calculate averages and prepare the final data
    final_data = []
    for name, data in player_data.items():
        if data['count'] > 0:
            avg_proj = data['proj'] / data['count']
            avg_total = data['total'] / data['count']
            final_data.append({
                'name': name,
                'team': data['team'],
                'position': data['position'],
                'avg_proj': avg_proj,
                'avg_total': avg_total
            })

    output_file = 'final_data.json'
    with open(output_file, 'w') as file:
        json.dump(final_data, file, indent=4)

    print(f"Data successfully written to {output_file}")

    # Output the final data
    for player in final_data:
        print(player)

if __name__ == "__main__":
    main()
