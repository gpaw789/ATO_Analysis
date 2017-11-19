# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Social
# TITLE: Australian Tax Return Income by Gender Breakdown
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

def gender_breakdown(df):

    ignore_list = ATO_helper.ignore_list
    filtered_list = ATO_helper.filter_ignore_list(ATO_helper.income_list, ignore_list) + ["Gender"]  #include gender data
    filtered_list_without_gender = filtered_list[:]
    filtered_list_without_gender.remove("Gender")
    # dataframe of all gender, with filtered column
    df_inc_all = pd.DataFrame(df)[filtered_list]

    def generate_list(df):
        # X_income_all_genders = [   [  [sw1 of male, sw2 of male ... ], [sw1 of female, sw2 of female ... ] ... ],
        #   [ alow_ben_amt1 of male, alow_ben_amt2 of male ... ] , [ alow_ben_amt1 of female, alow_ben_amt2 of female ... ] ... , ... ]
        # list_inc_all or X_median_income_all_gender =
        # [  [median sw of male, median sw of female ... ], [median alow_ben_amt of male, median sw of female ...] ... ]
        # think of it as a 2 columns (male/female) by len(filtered_list_without_gender) row
        list_inc_all = []
        for cols in filtered_list_without_gender:
            list_all_gender = []
            for i in range(0, 2):       #two types of gender, 0 = male, 1 = female
                temp_val = df.query("Gender == {}".format(i))[cols].mean()     #why query first then filter column? because you can't query series, so if you query first it is still a dataframe, then you filter by column
                #debug
                #print("Looking at {}, getting value of {}".format(list(df.query("Gender == {}".format(i))[cols]), temp_val))
                list_all_gender.append(temp_val)         #why this? you find the index of the value from the list and then shove it into the array

            list_inc_all.append(list_all_gender)           #note: you are building it as per filtered_list_without_gender - make sure it is in correct order

        return list_inc_all
    #regular data
    list_inc_all = generate_list(df_inc_all)

    # print data
    sum_male = 0; sum_fem = 0
    for i in list_inc_all:
        sum_male = i[0] + sum_male
        sum_fem = i[1] + sum_fem

    print(sum_male, sum_fem)

    # age group
    gender_group_list = ["Male", "Female"]

    # category
    income_category_list = ATO_helper.translate_to_full(filtered_list_without_gender)

    # creating traces
    traces = [0]*len(income_category_list)
    for i in range(0, len(income_category_list)):
        trace_instance = go.Bar(
            x=gender_group_list,
            y=list_inc_all[i],      #the data for one specific gender, with many income columns
            name=income_category_list[i],
            opacity=0.75,
            width=0.4
        )
        traces[i] = trace_instance

    data = traces
    layout = go.Layout(
        title="Australian Tax Return Taxable Income<br>by Gender and Partner Status",
        barmode='stack',  # stacked histogram
        yaxis=dict(title="Australian Dollar"),
        xaxis=dict(title="Gender"),
        legend=dict(orientation="v", font=dict(size=8)), showlegend=False,
    )
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename="{}/output/{}.html".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))

    ATO_helper.save_div_text(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'), "{}/output/{}.txt".format(os.getcwd(), os.path.basename(sys.argv[0][:-3])))


    return 0

gender_breakdown(df)