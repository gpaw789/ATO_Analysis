# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Social
# TITLE: Australian Tax Return Taxable Income by Gender and Partner Status
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

def ATO_SO_2(df):

    inc_all_male = [0]*len(ATO_helper.age_group)
    for i in range(0, len(inc_all_male)):
        inc_all_male[i] = pd.DataFrame(df).query("age_range == {} & Gender == 0".format(i))["Taxable_Income"].median()

    inc_all_fem = [0]*len(ATO_helper.age_group)
    for i in range(0, len(inc_all_fem)):
        inc_all_fem[i] = pd.DataFrame(df).query("age_range == {} & Gender == 1".format(i))["Taxable_Income"].median()

    # reverse the list to produce age group from youngest to oldest
    inc_all_male = inc_all_male[::-1]
    inc_all_fem = inc_all_fem[::-1]
    age_groups = list(ATO_helper.age_group.values())[::-1]

    trace_male = go.Bar(
        x = age_groups,
        y = inc_all_male,
        name = "Male",
        hoverinfo="x+y",
        showlegend=True,
    )
    trace_female = go.Bar(
        x = age_groups,
        y = inc_all_fem,
        name = "Female",
        hoverinfo="x+y",
        showlegend=True,
    )

    data = [trace_male, trace_female]
    layout = go.Layout(
        title="Australian Median Incomes by Gender & Age Group",
        barmode='group',  # grouped bar
        yaxis=dict(title="Australian Dollar"),
        xaxis=dict(title="Age Group"),
        legend=dict(orientation="h"),
    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_SO_2(df)