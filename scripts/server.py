from shiny import render
from shiny.types import ImgData
import numpy as np
import pandas as pd
from arch.unitroot import ADF
from sklearn.ensemble import AdaBoostClassifier
import pickle
import seaborn as sns
sns.set_theme(style="darkgrid")
from scripts import data_load
import asyncio



states_freq = data_load.states_freq
counties_freq = data_load.counties_freq
years = data_load.years
states = data_load.states
counties = data_load.counties
clf = data_load.clf

top_c = data_load.top_c
top_c0 = data_load.top_c0
top_c1 = data_load.top_c1
top_c2 = data_load.top_c2

bott_c = data_load.bott_c
bott_c0 = data_load.bott_c0
bott_c1 = data_load.bott_c1
bott_c2 = data_load.bott_c2



def server(input, output, session):
    @output
    @render.text
    def state_codes():
        temp = ''
        for i in states:
            temp = temp + i + '\n'
        return temp

    @output
    @render.plot
    def fotp():
        state_ind = input.state_txt()
        start = input.time_period_sl()[0] - 1992
        end = input.time_period_sl()[1] - 1992 + 1
        if np.isin(state_ind, states):
            ind = np.where(states == state_ind)[0]
            temp = pd.DataFrame(states_freq[int(ind)][start:end])
        else:
            state_ind = "All States"
            temp = pd.DataFrame(states_freq[len(states)][start:end])
        fvy_plot = sns.lineplot(x=0, y=1, data=temp)
        fvy_plot.set_xlabel("Year")
        fvy_plot.set_ylabel("Cumulative Fires")
        fvy_plot.set(title= 'Fires in ' + state_ind + ' per year')
        return fvy_plot

    @output
    @render.text
    def fot():
        state_ind = input.state_txt()
        start = input.time_period_sl()[0] - 1992
        end = input.time_period_sl()[1] - 1992 + 1
        if np.isin(state_ind,states):
            ind = np.where(states == state_ind)[0]
            temp = pd.DataFrame(states_freq[int(ind)][start:end])
        else:
            state_ind = "All States"
            temp = pd.DataFrame(states_freq[len(states)][start:end])
        adf = ADF(temp.loc[:, 1])
        if adf.pvalue < 0.05:
            conc = ' (Reject H0, Fires stable in time)'
        else:
            conc = ' (Cannot reject H0, Possible addition or reduction of Fires in time)'
        return state_ind + ", Test's P-value:      " + str(adf.pvalue) + conc

    @output
    @render.text
    def counties_tb():
        if input.year_rb() == 'All':
            if input.county_rb() == 't' :
                temp = top_c[:input.county_n()]
                message = 'The most prone counties in descending order:        '
            else:
                temp = bott_c[:input.county_n()]
                message = 'The least prone counties in ascending order:        '
            period = ' 1992-2015'
        elif input.year_rb() == 'ni':
            if input.county_rb() == 't' :
                temp = top_c0[:input.county_n()]
                message = 'The most prone counties in descending order:        '
            else:
                temp = bott_c0[:input.county_n()]
                message = 'The least prone counties in ascending order:        '
            period = ' 1992-2000'
        elif input.year_rb() == 'tw':
            if input.county_rb() == 't' :
                temp = top_c1[:input.county_n()]
                message = 'The most prone counties in descending order:        '
            else:
                temp = bott_c1[:input.county_n()]
                message = 'The least prone counties in ascending order:        '
            period = ' 2000-2010'
        else :
            if input.county_rb() == 't' :
                temp = top_c2[:input.county_n()]
                message = 'The most prone counties in descending order:        '
            else:
                temp = bott_c2[:input.county_n()]
                message = 'The least prone counties in ascending order:        '
            period = ' 2000-2015'
        txt_re = 'For the period' + period + '... ' + message
        for i in range(len(temp)):
            txt_re = txt_re + ' ' + (temp[i])[0] + ','
        return txt_re + '...'

    @output
    @render.text
    def pred():
        x = [[ int(input.date().year)-1992, input.date().weekday(), input.date().month, (input.pred_coor_la() + 90) / 10, (input.pred_coor_la() + 180) / 20, input.fire_size() ], [ int(input.date().year)-1992,  input.date().weekday(), int(input.date().month), (input.pred_coor_la() + 90) / 10, (input.pred_coor_la() + 180) / 20, input.fire_size() ]]
        if x[0][0] < 0 : x[0][0] = 0
        if x[0][0] > 23 : x[0][0] = 23
        x = np.array(x)
        result = clf.classes_[ np.argsort( (-1)*clf.predict_log_proba(x) ) ][0]
        txt_re = 'The Fire Causes for data x=' + str([ input.date().strftime("%d/%m/%Y"), input.pred_coor_lo(), input.pred_coor_la(), input.fire_size() ]) + ',\n    are sorted from highest to lowest probability:   \n'
        for i in result:
            txt_re = txt_re + i + ', '
        return  txt_re

    @output
    @render.image
    def image():
        img: ImgData = {"src": "logo.png", "width": "500px"}
        return img

    @session.download(
        filename = lambda: f"Counties_{input.year_rb()}_{input.county_rb()}.csv"
    )
    async def down_b():
        if input.year_rb() == 'All':
            if input.county_rb() == 't' :
                temp = top_c[:input.county_n()]
            else:
                temp = bott_c[:input.county_n()]
        elif input.year_rb() == 'ni':
            if input.county_rb() == 't' :
                temp = top_c0[:input.county_n()]
            else:
                temp = bott_c0[:input.county_n()]
        elif input.year_rb() == 'tw':
            if input.county_rb() == 't' :
                temp = top_c1[:input.county_n()]
            else:
                temp = bott_c1[:input.county_n()]
        else :
            if input.county_rb() == 't' :
                temp = top_c2[:input.county_n()]
            else:
                temp = bott_c2[:input.county_n()]
        await asyncio.sleep(0.25)
        for i in temp:
            yield i[0]+'\n'



print("Server Loaded...")