# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Average Australian
# TITLE: Percentile of Australians Taxable Incomes from ATO dataset 2013-2014
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

def ATO_AA_6(df):
    #get the data for all the taxable income
    range_all = pd.DataFrame(df)["Taxable_Income"]

    median_income = range_all.median()

    #create a histogram trace
    trace = go.Histogram(
        xbins=dict(start=0, size=500, end=range_all.max()),     #create bin sizes of 1000, no end
        x=range_all,
        opacity=0.75,
        hoverinfo="x+y",
        histnorm="probability",
        cumulative=dict(enabled=True, direction="decreasing"),
    )
    line = go.Scatter(
        x=[median_income],
        y=[1],
        text=["Median Income"],
        mode="text",
        opacity=0.75,
        hoverinfo="none"
    )

    data = [trace,line]
    layout = go.Layout(
        title="Percentile of Australians Taxable Incomes from ATO dataset 2013-2014",
        yaxis=dict(title="Fraction of Population", showspikes=True,spikedash="solid",spikecolor="black",spikethickness=1, hoverformat=".3%f"),   #show spikes, round values
        xaxis=dict(title="Taxable Income (AUD)", range=[0,350000], showspikes=True,spikedash="solid",spikecolor="black",spikethickness=1, hoverformat=".0f"),            #limit window size, show spikes, round values
        hovermode="closest",        #need to enable this with show spikes
        shapes=[dict(type="line",x0=median_income,y0=0,x1=median_income,y1=1,line=dict(color="red",width=3))],
        showlegend=False
    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AA_6(df)