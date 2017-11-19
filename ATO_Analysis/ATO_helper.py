import xlrd
import os
import pandas as pd

#getting path
target_path = os.getcwd() + "/Sample_file_1314/2014_sample_file.csv"
df = pd.read_csv(target_path)


#create global lists
ignore_list = ["Gross_rent_amt", "Other_rent_ded_amt", "Rent_int_ded_amt", "Rent_cap_wks_amt",
               "Total_PP_BI_amt", "Total_NPP_BI_amt", "Total_PP_BE_amt", "Total_NPP_BE_amt",
               "Tot_CY_CG_amt", "Tot_inc_amt"]

ID_list = [df.columns[i] for i in range(0,7)]
income_list = [df.columns[i] for i in range(8,37)]
deduction_list = [df.columns[i] for i in range(37,48)]
losses_list = [df.columns[i] for i in range(49,50)]
other_list = [df.columns[i] for i in range(51,66)]

#age group
age_group = {
    0: "70 and over", 1: "65 to 69", 2: "60 to 64", 3: "55 to 59", 4: "50 to 54", 5: "45 to 49", 6: "40 to 44", 7: "35 to 39",
    8: "30 to 34", 9: "25 to 29", 10: "20 to 24", 11: "under 20"
}



def translate_to_full(column_list):

    #translate column names to full names
    target_path = os.getcwd() + "/Documentation/Variables in 2013-14 sample file.xlsx"
    df = pd.read_excel(target_path)
    df_filtered = df[["File column name", "Description"]].dropna()

    #create a new list, populate it by looking up the value of the column names and return full name
    new_list = []
    for i in column_list:
        row_pos = df_filtered.loc[df_filtered["File column name"] == i].index[0]
        new_element = df_filtered.get_value(row_pos, "Description")
        new_list.append(new_element)

    return new_list


def filter_ignore_list(input_list, ignore_list):
    for i in ignore_list:
        try:
            input_list.remove(i)
        except:
            pass
    return input_list

def save_div_text(div, name):
    with open(name, "w") as sfile:
        sfile.write(div)
    print("File {} saved successfully".format(name))

#function for breaking down income
def breakdown_income(df, ignore_list=ignore_list):      # allow custom ignore list
    ###breakdown of income
    filtered_list = filter_ignore_list(income_list, ignore_list)
    df_break = pd.DataFrame(df[filtered_list])          #get dataframe for income breakdown
    df_break_mean = df_break.mean()                #get dataframe of mean, reduce to 1xmany dataframe

    '''
    # do not do negative income list, just call a spade a spade, use barmode relative so show negative values
    # why not do negative income list? because the income_labels will have different values every time, and its hard to keep track
    negative_income_list = []; negative_income_value = []
    for i in filtered_list:                           #filter out all the negative column and values
        if df_break_mean[i] < 0:
            negative_income_list.append(i)
            negative_income_value.append(df_break_mean[i])
            df_break_mean = df_break_mean.drop([i])
    '''

    #filter out income list  - push the negative values into deduction/loss category
    income_list_filtered = filtered_list

    #setup the values
    income_labels = translate_to_full(income_list_filtered)
    income_values = [i for i in list(df_break_mean)]
    return income_values, income_labels

# function for breaking down loss
def breakdown_loss(df):         # allow custom ignore list
    ###breakdown of income
    filtered_list = filter_ignore_list(income_list, ignore_list)
    df_break = pd.DataFrame(df[filtered_list])  # get dataframe for income breakdown
    df_break_mean = df_break.mean()  # get dataframe of mean, reduce to 1xmany dataframe

    '''#do not use negative_income_list
    negative_income_list = [];
    negative_income_value = []
    for i in filtered_list:  # filter out all the negative column and values
        if df_break_mean[i] < 0:
            negative_income_list.append(i)
            negative_income_value.append(df_break_mean[i])
            df_break_mean = df_break_mean.drop([i])

    # filter out income list  - push the negative values into deduction/loss category
    income_list_filtered = filtered_list
    for i in negative_income_list:
        income_list_filtered.remove(i)
    '''
    ###breakdown of deductions/losses
    filtered_list = filter_ignore_list(deduction_list, ["Tot_ded_amt"])
    df_loss = pd.DataFrame(df[filtered_list])
    df_loss_mean = df_loss.mean()

    # setup the values
    loss_labels = translate_to_full(filtered_list)
    loss_values = [round(i, 0) for i in list(df_loss_mean)]

    return loss_values, loss_labels

#translate_to_full(["Ind", "Gender"])
#filtered_list = filter_ignore_list(income_list, ignore_list)