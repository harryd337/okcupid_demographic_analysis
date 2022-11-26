# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:42:21 2022

@author: Harry Durnberger

Program for cleaning OKCupid dataset.

i.e. removing irrelevant and useless features;
binarising categorical features;
merging minority features.

Cleaned dataset is written to "ok.csv".
List of features is written to "features.txt".
"""
import numpy as np
import pandas as pd
ok = pd.read_csv("user_data_public.csv")
#drop likely irrelevant features:
ok = ok.drop(columns=['lf_single','d_religion_seriosity','CA','gender2',
                      'CA_items','gender2_num','d_astrology_seriosity',
                      'gender','d_astrology_sign','d_country','d_ethnicity',
                      'lf_want','lf_for','d_job','d_languages',
                      'd_relationship','lf_location','d_education_type',
                      'gender_orientation','d_income','d_bodytype',
                      'd_offspring_desires'])
#string-like categorical features we must binarise:
list_binarise = ['d_education_phase','d_religion_type','d_offspring_current',
                 'race']
for i in range(0,len(list_binarise)): #loop over list of categorical features
    #list of unique categories of each feature:
    unique = [*(ok[list_binarise[i]].unique())]
    unique = [x for x in unique if str(x) != 'nan'] #remove NaNs
    for j in range(0,len(unique)): #loop over unique categories of a feature
        #create new binary column for each category:
        ok[unique[j]] = np.where(ok[list_binarise[i]] == unique[j], 1, 0)
ok = ok.drop(columns=['-', 'Other']) #drop useless newly created columns
#we must binarise boolean-like (yes/no) categorical features
#create new binary columns for positive categories:
ok['Drugs often'] = np.where(ok['d_drugs'] == 'Often', 1, 0)
ok['Smokes'] = np.where((ok['d_smokes'] == 'Yes') |
                        (ok['d_drinks'] == 'Trying to quit'), 1, 0)
ok['Drinks often'] = np.where((ok['d_drinks'] == 'Very often') |
                              (ok['d_drinks'] == 'Often'), 1, 0)
#create new binary columns for majority groups:
ok['Straight'] = np.where(ok['d_orientation'] == 'Straight', 1, 0)
ok['Gay'] = np.where(ok['d_orientation'] == 'Gay', 1, 0)
ok['Bisexual'] = np.where(ok['d_orientation'] == 'Bisexual', 1, 0)
#create new binary column for 50 other minority orientations:
ok['Other orientation'] = np.where(
    (ok['d_orientation'] != 'Straight') &
    (ok['d_orientation'] != 'Gay') &
    (ok['d_orientation'] != 'Bisexual')
    , 1, 0)
#create new binary columns for majority groups:
ok['Male'] = np.where(ok['d_gender'] == 'Man', 1, 0)
ok['Female'] = np.where(ok['d_gender'] == 'Woman', 1, 0)
#create new binary column for 36 other minority genders:
ok['Other gender'] = np.where(
    (ok['d_gender'] != 'Man') &
    (ok['d_gender'] != 'Woman')
    , 1, 0)
ok = ok.drop(columns=['d_education_phase','d_religion_type',
                      'd_offspring_current','race',
                      'd_drugs','d_smokes','d_drinks','d_orientation',
                      'd_gender']) #drop columns we just converted
ok.to_csv("ok.csv") #write cleaned dataset to csv file
#remove all columns containing 'q' (not features):
ok_no_qs = ok[ok.columns.drop(list(ok.filter(regex='q')))]
features = ok_no_qs.columns.tolist() #list of features
with open('features.txt', 'w') as f: #write list of features to text file
    for line in features:
        f.write(f"{line}\n")