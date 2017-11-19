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

def ATO_SO_3(df):

    # get median taxable income for male
    median_male = df[(df["Gender"] == 0)]["Taxable_Income"].median()

    # get median taxable income for single male
    median_male_single = df[(df["Gender"] == 0) & (df["Partner_status"] == 0)]["Taxable_Income"].median()

    # get median taxable income for male with partner
    median_male_partner = df[(df["Gender"] == 0) & (df["Partner_status"] == 1)]["Taxable_Income"].median()

    # get median taxable income for female
    median_female = df[(df["Gender"] == 1)]["Taxable_Income"].median()

    # get median taxable income for single female
    median_female_single = df[(df["Gender"] == 1) & (df["Partner_status"] == 0)]["Taxable_Income"].median()

    # get median taxable income for female with partner
    median_female_partner = df[(df["Gender"] == 1) & (df["Partner_status"] == 1)]["Taxable_Income"].median()



    # build traces
    trace_male = go.Bar(
        x = ["All", "Single", "With Partner"],
        y = [median_male, median_male_single, median_male_partner],
        name = "Male",
        text = [median_male, median_male_single, median_male_partner],
        textposition = "outside"
    )
    trace_female = go.Bar(
        x = ["All", "Single", "With Partner"],
        y = [median_female, median_female_single, median_female_partner],
        name = "Female",
        text = [median_female, median_female_single, median_female_partner],
        textposition = "outside"
    )

    data = [trace_male, trace_female]
    layout = go.Layout(
        title="Australian Median Incomes by Gender & Partner Status",
        barmode='group',  # grouped bar
        yaxis=dict(title="Australian Dollars"),
        xaxis=dict(title="Gender"),
        legend=dict(orientation="h")
    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_SO_3(df)