# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Age
# TITLE: Australian Tax Return Income Breakdown by Age Group
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


def ATO_AG_6(df):

    ignore_list = ATO_helper.ignore_list
    filtered_list = ATO_helper.filter_ignore_list(ATO_helper.income_list, ignore_list) + ["age_range"]  #include age_range data
    filtered_list_without_age_range = filtered_list[:]
    filtered_list_without_age_range.remove("age_range")
    # dataframe of all ages, with filtered column
    df_inc_all = pd.DataFrame(df)[filtered_list]

    def generate_list(df):
        # X_income_all_age = [  [ [sw1 of age0, sw2 of age0 ...], [sw1 of age1, sw2 of age2 ...] ...],
        # [ [alow_ben_amt1 of age0, alow_ben_amt2 of age0 ...], [ [alow_ben_amt1 of age1, alow_ben_amt2 of age1 ...] ...] ... ]
        # list_inc_all or X_mean_income_all_age = [  [mean sw of age0, mean sw of age1 ...], [mean alow_ben_amt of age0, mean alow_ben_amt of age1 ...] ... ]
        list_inc_all = []
        for cols in filtered_list_without_age_range:
            list_all_age = []
            for i in range(len(ATO_helper.age_group) -1, -1, -1):       #reverse, young to old, left to right
                temp_float = df.query("age_range == {}".format(i))[cols].mean()     #why query first then filter column? because you can't query series, so if you query first it is still a dataframe, then you filter by column
                #debug
                #print("Looking at {}, getting value of {}".format(list(df.query("age_range == {}".format(i))[cols]), temp_float))
                print("Looking at {}, getting value of {}".format(cols, temp_float))
                list_all_age.append(temp_float)         #why this? you find the index of the value from the list and then shove it into the array


            list_inc_all.append(list_all_age)           #note: you are building it as per filtered_list_without_age_range - make sure it is in correct order

        return list_inc_all
    #regular data - can be removed
    #list_inc_all = generate_list(df_inc_all)

    # normalising for percentages
    # normalise the dataframe first
    df_age_range = pd.DataFrame(df_inc_all["age_range"])
    df_sum_across_col = abs(df_inc_all[filtered_list_without_age_range]).sum(axis=1)      #absolute because you have negative numbers, no need to include age_range
    df_inc_all_norm = 100*df_inc_all[filtered_list_without_age_range].div(df_sum_across_col, axis=0)     #1.all the columns without age_range is divided by a series array, then convert to percentages
    df_inc_all_norm = df_inc_all_norm.fillna(0)         #make sure there's no NA in dataframe, can't process maths
    df_inc_all_norm = pd.concat([df_inc_all_norm, df_age_range], axis=1)         #combine back the original age_range values

    list_inc_all_norm = generate_list(df_inc_all_norm)

    # debug
    df_inc_all_norm.to_csv("norm.csv")
    df_inc_all.to_csv("test.csv")


    # age group
    age_group_list = [ATO_helper.age_group[i] for i in ATO_helper.age_group][::-1]

    # category
    income_category_list = ATO_helper.translate_to_full(filtered_list_without_age_range)


    # creating traces for percentages
    traces = [0]*len(income_category_list)
    for i in range(0, len(income_category_list)):
        trace_instance = go.Bar(
            x=age_group_list,
            y=list_inc_all_norm[i],      #the data for one specific age group, with many income columns
            name=income_category_list[i],
            opacity=0.75,
        )
        traces[i] = trace_instance

    data = traces
    layout = go.Layout(
        title="Breakdown of Australians' Incomes by Age Group (Percentage)",
        barmode='relative',  # stacked histogram
        yaxis=dict(title="Percentage of Salary"),
        xaxis=dict(title="Age Group"),
        legend=dict(orientation="h", font=dict(size=0.7)),
        autosize=False,
        height = 1000,
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))
    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    return 0

ATO_AG_6(df)