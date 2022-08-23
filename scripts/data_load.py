import sqlite3
from fastparquet import write
import zipfile
import numpy as np
import pandas as pd
import csv
from sklearn.ensemble import AdaBoostClassifier
import pickle
import datetime


## main dataset
try:
    dataset = pd.read_parquet('data\dataset.parq')
    print("Dataset Loaded...")
except:
    try:
        with zipfile.ZipFile('data\dataset.zip', 'r') as zip_ref:
            zip_ref.extractall('data')
        dataset = pd.read_parquet('data\dataset.parq')
        print("Dataset Loaded...")
    except:
        try:
            print("Error 404: Dataset not found...")
            print("Creating Dataset from Database...")
            open("data\FPA_FOD_20170508.sqlite", "r")
            conn = sqlite3.connect("data\FPA_FOD_20170508.sqlite")
            print("Connected to Database...")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM 'Fires';")
            temp_db = cursor.fetchall()
            row = len(temp_db)
            col = 9
            data = [[0 for j in range(col)] for i in range(row)]
            for i in range(row):
                data[i][0] = temp_db[i][7]  ## name of forest
                data[i][1] = temp_db[i][19]  ## year of fire
                data[i][2] = temp_db[i][21]  ## DOY of fire
                data[i][3] = temp_db[i][30]  ## latitude
                data[i][4] = temp_db[i][31]  ## longitude
                data[i][5] = temp_db[i][28]  ## size
                data[i][6] = temp_db[i][34]  ## state of forest
                data[i][7] = temp_db[i][35]  ## county of forest
                data[i][8] = temp_db[i][24]  ## cause of fire
            del temp_db
            check = False
            for i in data:
                for j in range(col):
                    if i[j] == 0: check = True
            if check: print('There are missing values')
            data = pd.DataFrame(data)
            data.columns = ['Forest_name', 'Year', 'DOY', 'Latitude', 'Longitude', 'Fire_Size', 'State', 'County', 'Fire_Cause']
            write('data\dataset.parq', data)
            print("Dataset Saved...")
            dataset = data
            print("Dataset Loaded...")
        except:
            print("Error 404: Dataset not found...")
            print("Error 404: Database not found...")
            print("The app might not work properly...")

## support models
try:
    years = np.sort(pd.unique(dataset['Year']))
    states = np.sort(pd.unique(dataset['State']))
    counties = pd.unique(dataset['County'])
    with open('data/states_freq.csv', newline='') as f:
        states_freq = csv.reader(f)
        states_freq = list(states_freq)
    for i in range(len(states)+1):
        for j in range(len(years)):
            states_freq[i][j] = (states_freq[i][j]).strip('][').split(', ')
            states_freq[i][j] = [int(x) for x in states_freq[i][j]]
    with open('data/counties_freq.csv', newline='') as f:
        counties_freq = csv.reader(f)
        counties_freq = list(counties_freq)
    for i in range(len(counties)):
        for j in range(len(years)):
            counties_freq[i][j] = (counties_freq[i][j]).strip('][').split(', ')
            counties_freq[i][j] = [int(x) for x in counties_freq[i][j]]
    print("Support Tables loaded...")
except:
    try:
        print("Error 404: Support Tables not found...")
        print("Calculating Support Tables...")
        years = np.sort(pd.unique(dataset['Year']))
        states = np.sort(pd.unique(dataset['State']))
        counties = pd.unique(dataset['County'])
        row = len(states) + 1
        col = len(years)
        states_freq = [[0 for j in range(col)] for i in range(row)]
        ind_i = 0
        for i in states:
            ind_j = 0
            for j in years:
                temp = dataset.loc[dataset['Year'] == j]
                temp = temp.loc[temp['State'] == i]
                states_freq[ind_i][ind_j] = [j, temp.shape[0]]
                ind_j = ind_j + 1
            ind_i = ind_i + 1
        ind_j = 0
        for j in years:
            temp = dataset.loc[dataset['Year'] == j]
            states_freq[ind_i][ind_j] = [j, temp.shape[0]]
            ind_j = ind_j + 1
        pd.DataFrame(states_freq).to_csv('data\states_freq.csv', index=False, header=False)
        row = len(counties)
        col = len(years)
        counties_freq = [[0 for j in range(col)] for i in range(row)]
        ind_i = 0
        for i in counties:
            ind_j = 0
            for j in years:
                temp = dataset.loc[dataset['Year'] == j]
                temp = temp.loc[temp['County'] == i]
                counties_freq[ind_i][ind_j] = [j, temp.shape[0]]
                ind_j = ind_j + 1
            ind_i = ind_i + 1
        pd.DataFrame(counties_freq).to_csv('data\counties_freq.csv', index=False, header=False)
        print("Support Tables Saved...")
        states_freq=pd.DataFrame(states_freq)
        counties_freq=pd.DataFrame(counties_freq)
        print("Support Tables loaded...")
    except:
        print("Support Tables could not been calculated...")
        print("The app might not work properly...")

## tokens
try:
    with open('tokens/bott_c.csv', newline='') as f:
        bott_c = csv.reader(f)
        bott_c = list(bott_c)
    with open('tokens/bott_c0.csv', newline='') as f:
        bott_c0 = csv.reader(f)
        bott_c0 = list(bott_c0)
    with open('tokens/bott_c1.csv', newline='') as f:
        bott_c1 = csv.reader(f)
        bott_c1 = list(bott_c1)
    with open('tokens/bott_c2.csv', newline='') as f:
        bott_c2 = csv.reader(f)
        bott_c2 = list(bott_c2)
    with open('tokens/bott_c.csv', newline='') as f:
        top_c = csv.reader(f)
        top_c = list(top_c)
    with open('tokens/top_c0.csv', newline='') as f:
        top_c0 = csv.reader(f)
        top_c0 = list(top_c0)
    with open('tokens/top_c1.csv', newline='') as f:
        top_c1 = csv.reader(f)
        top_c1 = list(top_c1)
    with open('tokens/top_c2.csv', newline='') as f:
        top_c2 = csv.reader(f)
        top_c2 = list(top_c2)
    print("Tokens Loaded...")
except:
    print("Error 404: Tokens not found...")
    print("Calculating Tokens...")
    counties_freq_cum = [0]*len(counties)
    for i in range(len(counties)):
        counties_freq_cum[i] = pd.DataFrame(counties_freq[i][:8]).sum()
    counties_freq_cum = np.array(counties_freq_cum)
    top_c = counties[np.argsort(-counties_freq_cum[:,1])]
    bott_c = counties[np.argsort(counties_freq_cum[:,1])]
    try:
        top_c = np.delete(top_c, np.where(top_c==None))
        bott_c = np.delete(bott_c, np.where(bott_c==None))
    except:
        print(' ')
    pd.DataFrame(top_c).to_csv('tokens/top_c0.csv', index=False, header=False)
    pd.DataFrame(bott_c).to_csv('tokens/bott_c0.csv', index=False, header=False)
    top_c0 = top_c
    bott_c0 = bott_c
    counties_freq_cum = [0]*len(counties)
    for i in range(len(counties)):
        counties_freq_cum[i] = pd.DataFrame(counties_freq[i][8:18]).sum()
    counties_freq_cum = np.array(counties_freq_cum)
    top_c = counties[np.argsort(-counties_freq_cum[:,1])]
    bott_c = counties[np.argsort(counties_freq_cum[:,1])]
    try:
        top_c = np.delete(top_c, np.where(top_c==None))
        bott_c = np.delete(bott_c, np.where(bott_c==None))
    except:
        print(' ')
    pd.DataFrame(top_c).to_csv('tokens/top_c1.csv', index=False, header=False)
    pd.DataFrame(bott_c).to_csv('tokens/bott_c1.csv', index=False, header=False)
    counties_freq_cum = [0]*len(counties)
    top_c1 = top_c
    bott_c1 = bott_c
    for i in range(len(counties)):
        counties_freq_cum[i] = pd.DataFrame(counties_freq[i][18:]).sum()
    counties_freq_cum = np.array(counties_freq_cum)
    top_c = counties[np.argsort(-counties_freq_cum[:,1])]
    bott_c = counties[np.argsort(counties_freq_cum[:,1])]
    try:
        top_c = np.delete(top_c, np.where(top_c==None))
        bott_c = np.delete(bott_c, np.where(bott_c==None))
    except:
        print(' ')
    pd.DataFrame(top_c).to_csv('tokens/top_c2.csv', index=False, header=False)
    pd.DataFrame(bott_c).to_csv('tokens/bott_c2.csv', index=False, header=False)
    top_c2 = top_c
    bott_c2 = bott_c
    counties_freq_cum = [0]*len(counties)
    for i in range(len(counties)):
        counties_freq_cum[i] = pd.DataFrame(counties_freq[i][:]).sum()
    counties_freq_cum = np.array(counties_freq_cum)
    top_c = counties[np.argsort(-counties_freq_cum[:,1])]
    bott_c = counties[np.argsort(counties_freq_cum[:,1])]
    try:
        top_c = np.delete(top_c, np.where(top_c==None))
        bott_c = np.delete(bott_c, np.where(bott_c==None))
    except:
        print(' ')
    pd.DataFrame(top_c).to_csv('tokens/top_c.csv', index=False, header=False)
    pd.DataFrame(bott_c).to_csv('tokens/bott_c.csv', index=False, header=False)
    print("Tokens Saved...")
    print("Tokens Loaded...")

## prediction model
try:
    file = open("model/trained.sav", 'rb')
    clf = pickle.load(file)
    file.close()
    print("Model Loaded...")
except:
    try:
        print("Error 404: Model not Found...")
        print("Training the Model...")
        x_df = dataset[['Year', 'DOY', 'DOY', 'Latitude', 'Longitude', 'Fire_Size']]
        y_df = dataset[['Fire_Cause']]
        x_df = np.array(x_df)
        y_df = np.array(y_df)
        for i in range(len(y_df)):
            temp = datetime.date(int(x_df[i, 0]), 1, 1) + datetime.timedelta(int(x_df[i, 1]) - 1)
            x_df[i, 1] = temp.weekday()
            x_df[i, 2] = temp.month
        x_df[:, 0] = x_df[:, 0] - 1992
        x_df[:, 3] = (x_df[:, 2] + 90) / 10
        x_df[:, 4] = (x_df[:, 3] + 180) / 20
        clf = AdaBoostClassifier(n_estimators=50, random_state=0)
        clf.fit(x_df, y_df.ravel())
        print( clf.score(x_df, y_df) )
        f = open('model/trained.sav', 'wb')
        pickle.dump(clf, f, -1)
        f.close()
        print("Model Saved...")
        print("Model Loaded...")
    except:
        print("Model Can not be trained or loaded...")
        print("The app might not work properly...")



