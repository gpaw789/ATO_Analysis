# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Age
# TITLE: Australian Tax Return Income by Age Group Cumulative
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

def ATO_AG_2(df):

    range_all = [0]*len(ATO_helper.age_group)
    for i in range(0, len(range_all)):
        range_all[i] = pd.DataFrame(df).query("age_range == {}".format(i))["Taxable_Income"]

    trace_all = [0]*len(range_all)
    lines_all = [0]*len(range_all)
    for i in range(0, len(range_all)):
        trace_all[i] = go.Histogram(
            x=range_all[i],
            xbins=dict(start=0, size=1000, end=df["Taxable_Income"].max()),  # create bin size
            opacity=0.4,
            histnorm="percent",
            cumulative=dict(enabled=True, direction="decreasing"),
            name=ATO_helper.age_group[i]
        )

        lines_all[i] = go.Scatter(
            x=[range_all[i].median()],
            y=[50],
            mode="markers",
            opacity=0.75,
            hovertext=["{} avg income:<br>{}".format(ATO_helper.age_group[i], round(range_all[i].median()),2)],
            name=ATO_helper.age_group[i],
            hoverinfo="text",
            showlegend=False,
        )

    data = trace_all+lines_all
    layout = go.Layout(
        title="Australians Taxable Incomes<br>Percentile Rank By Age Group",
        barmode='overlay',
        legend=dict(orientation="h"),
        yaxis=dict(title="Percentile rank of Age Range Population", hoverformat=".2f"),   #show spikes, round values
        xaxis=dict(title="Income (AUD)", range=[0,250000], hoverformat=".0f"),            #limit window size, show spikes, round values
        height=667,
    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AG_2(df)