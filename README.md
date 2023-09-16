# CS 361 - FitBit Data Visualizer

This is a data visualization webapp that allows users to view long-term graphs and rolling averages of their Fitbit sleep data; these features are not included in the official Fitbit app. The webapp uses Pandas to load and transform the user's CSV-formatted sleep data, and Plotly Dash to generate interactive graphs. 

This was a project for Oregon State's **CS 361 - Software Engineering I**.

## Installation

After cloning the repo, set up a Python virtual environment of your choice, then run `pip -r requirements.txt` to install the needed dependencies. Once the dependencies are installed, you can run a local Dash server with `python app.py` and view the resulting page on a web browser. 

## Usage

To obtain a compatible sleep data CSV file, submit a request to FitBit at https://www.fitbit.com/settings/data/export. The export may take 24-72 hours to complete; once it does, download the file and locate the file at `Sleep/sleep_score.csv`. This is the file you will upload when prompted. (**Note: user data remains entirely local when running the app locally, and is not accessible to the developer or any other party.**)

Once the app has been started with `python app.py`, visit the localhost address specified in the terminal. Click the blue button near the top of the page to load your data. 

The three graphs on the page will automatically populate. You can use their controls to pan through the data, zoom in on specific time frames, or even download the graphs as PNG images. Hover over a given datapoint to view the details. 

## Screenshots

![Introduction and upload text](https://github.com/wflambeth/fibivi_361/blob/main/fibivi_screenshot_01.jpeg)


![Bar graph view](https://github.com/wflambeth/fibivi_361/blob/main/fibivi_screenshot_02.jpeg)


![Deep sleep graph view](https://github.com/wflambeth/fibivi_361/blob/main/fibivi_screenshot_03.jpeg)

