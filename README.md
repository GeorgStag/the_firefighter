# the_firefighter
WebApp for the analysis of fires in US

-- Assessment for Canonical's hiring procedure --

To run the app:
- You can download the repository and run the "run.py" script through python
- You can visit \n
-- https://georgstagtest.shinyapps.io/the_firefighter  \n
-- https://georgstagtest.shinyapps.io/the_firefighter1

App Architecture:
The app is placed in "app.py". 
The UI and server of the app are called through the respective scripts, in "scripts" file.
There is also the "data_load.py" script that loads the appropriate metadata, calculated from kaggle's database. \n
-- https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires \n
-- https://www.kaggle.com/code/adheep/us-wildfires

Metadata:
For the needs of the app, the columns ['Forest_name', 'Year', 'DOY', 'Latitude', 'Longitude', 'Fire_Size', 'State', 'County', 'Fire_Cause'] were used from the "Fires" table in kaggle's database.
From these columns, product tables were calculated in "data" and "tokens" files, associated with the frequency of fires per US county and state.
As long as, there is connection to the database or access to "dataset.parq" every product table can be calculated and saved again before the app runs, even if missing or being corrupted. Yet, it might need a significant amount of time for the tables to be calculated again from scratch.

Assessment needs:

Q1: Have wildfires become more or less frequent over time?
In the Second tab "Fire Occurencies per Time", there is plot for the fires per year. There are also results for testing the stationarity of the time series.
The user can check through the test's p-value if the time series is stationary, or else if the fires are ascending or descending through years, and if this is a case can confirm it visually in the plot above.
The plot can be can be saved through right click and the test results can be copied-pasted.
The plot and test appear for any state and for any time gap between 1992-2015.
The available state codes appear in the last tab "State Codes".

Q2: What counties are the most and least fire-prone?
In the Third tab "Counties prone to fire", the user can print the most or least prone counties to fire in specific time gaps. The results are called through the respective token files. The tokens are calculated through the amount of fires per county in specific time gaps.

Q3: Given the size, location and date, can you predict the cause of a wildfire? 
In the Third tab "Fire Cause Prediction", the cause of fire is predicted given data. The output is the causes sorted based on the probability of happening. For the estimation of probability the AdaBoost algorithm is used from Sci-Kit library. The input is rescaled appropriately to raise the algorithm's adaptability to the data.

Different algorithms' scores, tested for Q3:
- Categorical Naive Bayes:  0.37971 
- AdaBoost:                 0.35832 
- Random Decision Forest:   0.32783 
- Logistic Regression:      0.23012 
- Perceptron:               0.10828

Despite Categorical Naive Bayes having the highest score, it is quite unstable, failing often to predict for non observed cases, so AdaBoost was finally chosen.

Futre work:
- Give more plotting and cross-plotting options
- Add testing and algorithm choices
- The prediction to happen through model selection and more insight to the data.
- More utilities in County ordering or model predictions given time gap and other information
