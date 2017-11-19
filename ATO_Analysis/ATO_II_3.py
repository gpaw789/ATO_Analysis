# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Income Inequality
# TITLE: Australian Tax Return Income by Income Percentile
# AUTHOR: George Paw
# DATE: November 2017

import sys
import os
import pandas as pd
import plotly.graph_objs as go
import plotly

# custom imports
import ATO_helper

# getting path
target_path = os.getcwd() + "/Sample_file_1314/2014_sample_file.csv"
df = pd.read_csv(target_path)

#creating custom ignore list to include total income
ignore_list = ["Gross_rent_amt", "Other_rent_ded_amt", "Rent_int_ded_amt", "Rent_cap_wks_amt",
               "Total_PP_BI_amt", "Total_NPP_BI_amt", "Total_PP_BE_amt", "Total_NPP_BE_amt",
               "Tot_CY_CG_amt"]


def ATO_II_3(df):

    # determine the percentile rank, from 10% to 99%, increment by 10%, and then round them
    rank = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999]
    rank_text = ["10th<br>${}".format(round(df["Taxable_Income"].quantile(0.1)), 0), "20th<br>${}".format(round(df["Taxable_Income"].quantile(0.2)), 0),
                 "30th<br>${}".format(round(df["Taxable_Income"].quantile(0.3)), 0), "40th<br>${}".format(round(df["Taxable_Income"].quantile(0.4)), 0),
                 "50th<br>${}".format(round(df["Taxable_Income"].quantile(0.5)), 0), "60th<br>${}".format(round(df["Taxable_Income"].quantile(0.6)), 0),
                 "70th<br>${}".format(round(df["Taxable_Income"].quantile(0.7)), 0), "80th<br>${}".format(round(df["Taxable_Income"].quantile(0.8)), 0),
                 "90th<br>${}".format(round(df["Taxable_Income"].quantile(0.9)), 0), "99th (top 1%)<br>${}".format(round(df["Taxable_Income"].quantile(0.99)), 0),
                 "99.9th (top 0.1%)<br>${}".format(round(df["Taxable_Income"].quantile(0.999)), 0)]
    # get income_values and build traces
    income_pc_array = [0] * len(rank)
    for i in range(0, len(rank)):
        income_values, income_labels = ATO_helper.breakdown_income(df.query("Taxable_Income >= {}".format(df["Taxable_Income"].quantile(rank[i]))))
        income_pc = [round(100*income_values[i]/sum(income_values),2) for i in range(0, len(income_values))]   #all incomes divided by total income to get percentage, round to 2 decimal places
        income_pc_array[i] = income_pc       # making sure that the labels and values line up

    # source the labels
    full_income_labels =  income_labels

    # transpose list, from [  [a, b, c], [A, B, C], [aa, bb, cc]  ]  to  [  [a, A, aa], [b, B, bb], [c, C, cc]  ]

    income_pc_array = list(map(list, zip(*income_pc_array)))


    # build traces
    traces = [0] * len(full_income_labels)     # based off income_labels, picked the first one
    for label in range(0, len(full_income_labels)):
        trace_instance = go.Bar(
            x=rank_text,
            y=income_pc_array[label],      #the data for one specific rank group, with many income columns
            name=full_income_labels[label],
            opacity=0.75,
        )
        traces[label] = trace_instance

    data = traces
    layout = go.Layout(
        title="Australian Tax Return Income by Income Percentile",
        barmode='relative',  # stacked histogram
        yaxis=dict(title="Percentage of Taxable Income"),
        xaxis=dict(title="Percentile Rank"),
        legend=dict(orientation="v", font=dict(size=0.7)), showlegend=False,
        autosize=True,
        height=667,
    )
    # creating plot
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_II_3(df)