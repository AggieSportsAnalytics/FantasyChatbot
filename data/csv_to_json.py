import csv
import json
import os

def csv_to_json(file_paths):
    for file_path in file_paths:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            week_number = file_name.replace('week', '')  # Extracting week number from file name

            # Creating JSON structure with week number
            json_data = {
                "week_number": week_number,
                "data": list(csv_reader)
            }

            # Saving each file as a separate JSON file
            json_file_name = f"{file_name}.json"
            with open(json_file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# File paths for weeks 1 to 18
file_paths = ["data/week1.csv", "data/week2.csv", "data/week3.csv", 
              "data/week4.csv", "data/week5.csv", "data/week6.csv", 
              "data/week7.csv", "data/week8.csv", "data/week9.csv", 
              "data/week10.csv", "data/week11.csv", "data/week12.csv", 
              "data/week13.csv", "data/week14.csv", "data/week15.csv", 
              "data/week16.csv", "data/week17.csv", "data/week18.csv"]

# Converting each CSV to a separate JSON file
csv_to_json(file_paths)

