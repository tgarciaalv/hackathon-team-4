import pandas as pd

# Load the data
file_path = '/workspaces/hackathon-team-4/data/FLIGHTS_CLEANED.CSV'
data = pd.read_csv(file_path)

# Extract unique airport IDs and names
airports = data[['OriginAirportID', 'OriginAirportName']].drop_duplicates()
airports = airports.rename(columns={'OriginAirportID': 'AirportID', 'OriginAirportName': 'AirportName'})

# Extract unique destination airport IDs and names and merge with origin airports
dest_airports = data[['DestAirportID', 'DestAirportName']].drop_duplicates()
dest_airports = dest_airports.rename(columns={'DestAirportID': 'AirportID', 'DestAirportName': 'AirportName'})

# Combine origin and destination airports
all_airports = pd.concat([airports, dest_airports]).drop_duplicates().reset_index(drop=True)

# Save to a new CSV file
output_file_path = '/workspaces/hackathon-team-4/data/airports_list.csv'
all_airports.to_csv(output_file_path, index=False)
print(f"Airport list saved to {output_file_path}")