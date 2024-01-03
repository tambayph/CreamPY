# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 08:12:21 2023

@author: WF026
"""

import requests
import pandas as pd

# Replace 'your_api_url_here' with the actual API URL that provides the JSON data.
api_url = 'http://10.11.1.107/api/rainfall/202309010000'

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()

    # Create an empty DataFrame
    df = pd.DataFrame(columns=["#", "Name", "lat", "lon","RR"])

    # Iterate through the data and extract the required information
    for station in data:
        stn_number = station["stn_number"]
        stn_name = station["stn_name"]
        lat = station["lat"]
        lon = station["lon"]
        total_value = None

        for entry in station["rainfall"]:
            if entry["valueType"] == "total":
                total_value = entry["value"]

        df = df.append({"#": stn_number, "Name": stn_name, "lat": lat, "lon": lon, "RR": total_value}, ignore_index=True)

    # Save the DataFrame to a CSV file
    df.to_csv("output.csv", index=False)

    print("CSV file has been created: output.csv")

else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)
