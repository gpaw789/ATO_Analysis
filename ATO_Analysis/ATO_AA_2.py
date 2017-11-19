# TOPIC: Australian Tax Office - Tax Return Sample for Year 2013-14
# CATEGORY: Average Australian
# TITLE: Average Australian Tax Return Income
# AUTHOR: George Paw
# DATE: November 2017


import os
import pandas as pd

#getting path
target_path = os.getcwd() + "/Sample_file_1314/2014_sample_file.csv"
df = pd.read_csv(target_path)



def ATO_AA_2(df):

    #get the average of income for salary, total income and taxable income
    df_sw = pd.DataFrame(df["Sw_amt"])
    df_tot = pd.DataFrame(df["Tot_inc_amt"])
    df_tax = pd.DataFrame(df["Taxable_Income"])

    print(df_sw["Sw_amt"].mean())
    print(df_tot["Tot_inc_amt"].mean())
    print(df_tax["Taxable_Income"].mean())

ATO_AA_2(df)