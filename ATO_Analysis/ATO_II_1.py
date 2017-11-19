# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Average Australian
# TITLE: Average Australian Tax Return Deductions/Losses Breakdown 1% vs 99%
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

def ATO_II_1(df):

    # finding the top 1% of taxable income
    top1pc = df["Taxable_Income"].quantile(0.99)

    # split dataframe into two, 1: top 1%%, 2: bottom 99%
    df1 = df.query("Taxable_Income >= {}".format(df["Taxable_Income"].quantile(0.99)))
    df99 = df.query("Taxable_Income < {}".format(df["Taxable_Income"].quantile(0.99)))

    # getting values
    income_values1, income_labels1 = ATO_helper.breakdown_income(df1)
    income_values99, income_labels99 = ATO_helper.breakdown_income(df99)

    # truncate the labels a bit so it fits nicely in graph
    income_labels1 = [i[:55] for i in income_labels1]
    income_labels99 = [i[:55] for i in income_labels99]


    # Drawing Figure
    
    trace1 = go.Pie(
        values=income_values1,
        labels=income_labels1,
        domain=dict(x=[0,0.49], y=[0.1, 1]),      #changing the x,y position
        name="Income",
        textinfo="percent",
        textposition="inside",
        hoverinfo="label+value+percent",
        hole=0.6,
    )
    trace99 = go.Pie(
        values=income_values99,
        labels=income_labels99,
        domain=dict(x=[0.51,1], y=[0.1, 1]),      #changing the x,y position
        name="Income",
        textinfo="percent",
        textposition="inside",
        hoverinfo="label+value+percent",
        hole=0.6,
    )


    data = [trace1, trace99]

    layout = go.Layout(
        title="Average Australian Tax Return<br>Income Breakdown 2013-2014",
        autosize=True,
        legend=dict(x=1,y=0,orientation="h",font=dict(size=8)), showlegend=True,
        annotations=[dict(text="Income <br>for Top 1%",font=dict(size=16),showarrow=False, x=0.17,y=0.58),
                     dict(text="Income <br>for Bottom 99%", font=dict(size=16), showarrow=False, x=0.86, y=0.58)],
        height=667, width=800,
    )

    fig = go.Figure(
        data=data, layout=layout
    )

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    
    

    return 0

ATO_II_1(df)