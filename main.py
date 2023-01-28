import os
import sys
import webbrowser
import pywebio
import pandas as pd
import plotext as plt
import plotly.express as px

def main():
    csv_path = sys.argv[1]

    if csv_path == "--help":
        # print help string
        # exit 
        pass

    #if not os.path.exists(csv_path):
    #   print('File not found!')
    #    # offer to show help message
    #    pass

    print("Reading csv...")

    # Get full data from CSV
    df = pd.read_csv(csv_path, parse_dates=True)

    print("CSV read. Formatting data...")

    # convert datetime field to separated date and time 
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    df['time'] = pd.to_datetime(df['timestamp']).dt.time

    print("Data formatted. Preparing for output...")

    # limit range to a certain span 


    # output graph to plotly
    graph = px.bar(df, x='date', y='overall_score')
    graph.show()    

if __name__ == "__main__":
    main()

"""
format: 
sleep_log_entry_id (int)
timestamp (datestr)
overall_score (int)
composition_score (int)
revitalization_score (int)
duration_score (int)
deep_sleep_in_minutes, (int)
resting_heart_rate,(int)
restlessness (float)
"""