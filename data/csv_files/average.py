import os
import pandas as pd

def average_csv_files(directory_path, output_file):
    # Get a list of all CSV files in the directory
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the cumulative sum
    cumulative_sum = None

    
    for file in csv_files:
        df = pd.read_csv(os.path.join(directory_path, file))

        if cumulative_sum is None:
            cumulative_sum = df
        else:
            cumulative_sum += df

    # Calculate the average by dividing the cumulative sum by the number of CSV files
    average_df = cumulative_sum / len(csv_files)

    # Write the result to a new CSV file
    average_df.to_csv(output_file, index=False)


    # Specify the directory containing CSV files and the output file
input_directory = "data/csv_files"
output_file = 'data/csv_files/average.csv'

average_csv_files(input_directory, output_file)

print(f"Average CSV file saved to {output_file}")