# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Age
# TITLE: Australian Tax Return Income by Age Group
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

def ATO_AG_1(df):

    range_all = [0]*len(ATO_helper.age_group)
    for i in range(0, len(range_all)):
        range_all[i] = pd.DataFrame(df).query("age_range == {}".format(i))["Taxable_Income"]


    trace_all = [0]*len(range_all)
    for i in range(0, len(range_all)):
        trace_all[i] = go.Histogram(
            x=range_all[i],
            xbins=dict(start=0, size=5000, end=df["Taxable_Income"].max()),  # create bin size of 5000
            histnorm="probability",
            opacity=0.4,
            name=ATO_helper.age_group[i]
        )

    data = trace_all
    layout = go.Layout(
        title="Australians Taxable Incomes By Age Group",
        barmode='overlay',
        legend=dict(orientation="h"),
        yaxis=dict(title="Fraction of Age Range Population"),
        xaxis=dict(title="Income (AUD)", range=[0,250000]),            #limit size to under 250,000


    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AG_1(df)