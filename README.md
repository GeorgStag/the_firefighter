# the_firefighter
WebApp for the analysis of fires in US

-- Assessment for Canonical's hiring procedure --

To run the app:
- You can download the repository and run the "run.py" script through python
- You can visit https://georgstagtest.shinyapps.io/the_firefighter

App Architecture:
The app is placed in "app.py". 
The UI and server of the app are called through the respective scripts, in "scripts" file.
There is also the "data_load.py" script that loads the appropriate metadata, calculated from kaggle's database.
https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires
https://www.kaggle.com/code/adheep/us-wildfires

Metadata:
For the needs of the app, the columns ['Forest_name', 'Year', 'DOY', 'Latitude', 'Longitude', 'Fire_Size', 'State', 'County', 'Fire_Cause'] were used from the "Fires" table in kaggle's database.
From these columns, product tables were calculated in "data" and "tokens" files, associated with the frequency of fires per US county and state.
As long as, there is connection to the database or access to "dataset.parq" every product table can be calculated and saved again before the app runs, even if missing or being corrupted. Yet, it might need a significant amount of time for the tables to be calculated again from scratch.

Assessment needs:

Q1: Have wildfires become more or less frequent over time?
In the Second tab "Fire Occurancies per Time" there is plot for the fires per year. There are also results for testing the stationarity of the time series.
The user can check through the test's p-value if the time series is sationary, or else if the fires are ascending or descnding through years, and if this is a case can confirm it visually in the plot above.
The plot can be can be saved through right click and the test results can be copied-pasted.
The plot and test appear for any state and for any time gap between 1992-2015.
The available state codes appear in the last tab "State Codes".

Q2: What counties are the most and least fire-prone?
In the Third tab "Counties prone to fire"

Q3: Given the size, location and date, can you predict the cause of a wildfire?
nb:0.37971 ada:0.35832 random:0.32783 log:0.23 perceptron:0.108279

