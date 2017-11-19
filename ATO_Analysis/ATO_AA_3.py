# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Average Australian
# TITLE: Average Australian Tax Return Income Breakdown
# AUTHOR: George Paw
# DATE: November 2017

import sys
import os
import pandas as pd
import plotly.graph_objs as go
import plotly


#custom imports
import ATO_helper


#getting path
target_path = os.getcwd() + "/Sample_file_1314/2014_sample_file.csv"
df = pd.read_csv(target_path)

def ATO_AA_3(df):

    ###breakdown of income
    filtered_list = ATO_helper.filter_ignore_list(ATO_helper.income_list, ATO_helper.ignore_list)
    df_break = pd.DataFrame(df[filtered_list])          #get dataframe for income breakdown
    df_break_mean = df_break.mean()                #get dataframe of mean, reduce to 1xmany dataframe
    negative_income_list = []; negative_income_value = []
    for i in filtered_list:                           #filter out all the negative column and values
        if df_break_mean[i] < 0:
            negative_income_list.append(i)
            negative_income_value.append(df_break_mean[i])
            df_break_mean = df_break_mean.drop([i])

    #filter out income list  - push the negative values into deduction/loss category
    income_list_filtered = filtered_list
    for i in negative_income_list:
        income_list_filtered.remove(i)

    #setup the values
    income_labels = ATO_helper.translate_to_full(income_list_filtered)
    income_values = [round(i,0) for i in list(df_break_mean)]

    # Drawing Figure

    trace = go.Pie(
        values=income_values,
        labels=income_labels,
        domain=dict(x=[0, 1], y=[0, 1]),       # taking 100% of x position and 100% of y position
        name="Income",
        textinfo="value",
        hoverinfo="label+value+percent",
        hole=0.6,
    )

    data = [trace]

    layout = go.Layout(
        title="Average Australian Tax Return<br>Income Breakdown 2013-2014",
        autosize=True,
        legend=dict(y=-1, orientation="v",font=dict(size=8)), showlegend=True,
        #annotations=[dict(text="Income (AUD)",font=dict(size=20),showarrow=False,x=0.5,y=0.5)],
        width=375, height=740,              # mobile dimensions
    )

    fig = go.Figure(
        data=data, layout=layout
    )

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AA_3(df)