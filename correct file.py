from datetime import datetime
import os

#  Here’s a sample code snippet that demonstrates how to read multiple Excel files, extract the first two columns, and store them in a list:


import pandas as pd
import glob

   # List to hold the data from all files
data_list = []

   # Specify the path where your Excel files are located
path = r'C:\Users\games\Desktop\ppyy\attendence\*.xlsx'   # Adjust the path and extension as needed

   # Loop through each file in the directory
   
for filename in glob.glob(path):
       # Read the Excel file
    df = pd.read_excel(filename)
       
       # Extract the first two columns
    first_two_columns = df.iloc[:, :2]
       
       # Convert to a list of lists and append to data_list
    data_list.append(first_two_columns.values.tolist())

# Now data_list contains the first two columns from all files
print(data_list)


# Define the initial data as a multi-line string
data_string = """



"""

# Initialize a dictionary to hold lists by number
number_entries = {}

# Process each line of data
for entry in data_string.strip().split('\n'):
    number, timestamp = entry.split('\t')
    number = number.strip()
    timestamp = timestamp.strip()

    if number not in number_entries:
        number_entries[number] = []
    number_entries[number].append(timestamp)

# Create an output directory if it doesn't exist
output_dir = 'output_files'
os.makedirs(output_dir, exist_ok=True)

# Function to calculate enter and exit times for a given list of timestamps
def calculate_entries_exits(entries):
    entries_by_day = {}
    
    # Group entries by day
    for time_str in entries:
        date_time = datetime.strptime(time_str, "%d/%m/%y %H:%M")
        day_key = date_time.date()
        if day_key not in entries_by_day:
            entries_by_day[day_key] = []
        entries_by_day[day_key].append(time_str)

    # Pair entries and exits
    paired_results = []
    for day, entries in entries_by_day.items():
        entries.sort(key=lambda x: datetime.strptime(x, "%d/%m/%y %H:%M"))
        if entries:
            paired_results.append(f"Enter: {entries[0]}  Exit: {entries[-1]}")  # Earliest and latest
    return paired_results

# Iterate through each identifier in the number_entries
for identifier, timestamps in number_entries.items():
    # Separate entries into Morning and Evening
    morning_entries = []
    evening_entries = []

    for time_str in timestamps:
        date_time = datetime.strptime(time_str, "%d/%m/%y %H:%M")
        if date_time.hour < 14:  # Morning times
            morning_entries.append(time_str)
        else:  # Evening times
            evening_entries.append(time_str)

    # Sort the lists
    morning_entries.sort(key=lambda x: datetime.strptime(x, "%d/%m/%y %H:%M"))
    evening_entries.sort(key=lambda x: datetime.strptime(x, "%d/%m/%y %H:%M"))

    # Calculate enter and exit times for Morning and Evening
    morning_results = calculate_entries_exits(morning_entries)
    evening_results = calculate_entries_exits(evening_entries)

    # Create a filename for each identifier
    filename = os.path.join(output_dir, f"identifier_{identifier}.txt")
    
    # Write the processed information to the file
    with open(filename, 'w') as file:
      
        file.write(f"\nMorning Entries and Exits:\n")
        for result in morning_results:
            file.write(f"  - {result}\n")

        file.write(f"\nEvening Entries and Exits:\n")
        for result in evening_results:
            file.write(f"  - {result}\n")

print("Processed information has been written to separate files.")