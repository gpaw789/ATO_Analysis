# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Age
# TITLE: Australian Tax Return Income by Age Group (3D, Log)
# AUTHOR: George Paw
# DATE: November 2017

import sys
import os
import pandas as pd
import plotly.graph_objs as go
import plotly
import numpy as np


#custom imports
import ATO_helper


#getting path
target_path = os.getcwd() + "/Sample_file_1314/2014_sample_file.csv"
df = pd.read_csv(target_path)

def ATO_AG_4(df):

    # get the data from df as [ [Taxable_Income_0 for age_0, Taxable_Income_1 for age_0 ... ], [Taxable_Income_0 for age_1, Taxable_Income_1 for age_1 ... ], ... ]
    range_all = [0]*len(ATO_helper.age_group)
    for i in range(0, len(range_all)):
        range_all[i] = list(pd.DataFrame(df).query("age_range == {}".format(i))["Taxable_Income"])

    # convert it to histogram format as [  [# of people in bin_0 for age 0, # of people in bin_1 for age 0, ... ], [# of people in bin_0 for age 1, # of people in bin_0 for age 1, ... ]
    range_hist_all = [0]*len(ATO_helper.age_group)
    for age in range(0, len(range_all)):
        count, division = np.histogram(range_all[age], bins=list(range(0,df["Taxable_Income"].max(),5000)))         #create the bin size, use the max as the end point
        range_hist_all[age] = count

    # convert it to a dataframe, transpose it, the dataframe has index as bins and columns as age_group
    df_new = pd.DataFrame(range_hist_all, columns=list(range(0,df["Taxable_Income"].max(),5000))[:-1], index=ATO_helper.age_group.values())        #reduce the bin list by 1, because bins is always one extra from result, as it is to cover the "remainding" data, since we found the max income in the data, there is no point of having the last bin
    df_new = df_new.transpose()

    # normalise df by age group
    df_sum_across_rows = df_new.sum(axis=0)
    df_new = 100 * df_new.div(df_sum_across_rows, axis=1)


    # reduce data points
    df_new = df_new.iloc[:80]  # show only income between 0 and 200k, max data points is approx 1279

    # Drawing 3D - how it works: each data "line" needs to be drawn twice to produce a 2D plane ribbon
    # so therefore each data point is a tuple of 2 dimension, e.g. z = (10,10), y = (5,5), x = (1,2), x is two lines so it makes a plane
    traces=[0]*len(list(ATO_helper.age_group.values()))
    y_raw = list(range(0, df["Taxable_Income"].max(), 5000))[:-1]
    for age_col in range(0, len(list(ATO_helper.age_group.values()))):
        z_raw = df_new[ATO_helper.age_group[age_col]].tolist()
        x = []; y = []; z = []
        for j in range(0, len(z_raw)):
            z.append([z_raw[j], z_raw[j]])
            y.append([y_raw[j], y_raw[j]])
            x.append([age_col, age_col+0.75])

        traces[age_col] = go.Surface(
            name=ATO_helper.age_group[age_col],
            x=x,
            y=y,
            z=z,
            showscale=False,
            colorscale= [
                [0, 'rgb(255, 0, 0)'],  # 0
                [1. / 10000000, 'rgb(250, 15, 0)'],  # 10
                [1. / 1000000, 'rgb(240, 30, 0)'],  # 10
                [1. / 100000, 'rgb(230, 45, 0)'],  # 10
                [1. / 10000, 'rgb(220, 75, 0)'],  # 10
                [1. / 1000, 'rgb(200, 100, 0)'],  # 100
                [1. / 100, 'rgb(180, 150, 0)'],  # 1000
                [1. / 10, 'rgb(150, 200, 0)'],  # 10000
                [1.0, 'rgb(0, 250, 0)'],  # 100000

            ],

        )


    data = traces
    layout = go.Layout(
        title='Australian Tax Return Income<br>by Age Group (3D, Log)',
        autosize=True,
        scene=dict(
            xaxis=dict(title="Age Group", tickmode="array", tickvals=list(range(0,12)), ticktext=list(ATO_helper.age_group.values())),
            yaxis=dict(title="Income Bracket"),
            zaxis=dict(title="Percentage of Age Group Population", type="log")
        ),
        height = 667, width = 667,
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AG_4(df)