#Clean OKCupid dataset.

#Created on Mon Nov 21 17:42:21 2022
#@author: Harry Durnberger

#This program cleans the OKCupid dataset.
#i.e. removes irrelevant and useless features;
#binarises categorical features;
#merges minority categories.

#Due to the messy nature of the dataset, most of these processes must be
# carried out manually, but are automated when possible.

#Cleaned dataset is written to "ok.pkl".
#List of total features is written to "features.txt".
#List of newly created features is written to "new_features.txt"
import numpy as np
import pandas as pd
import pickle

def load_dataset():
    """
    Loads the raw OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): original OkCupid dataset.
    """
    ok = pd.read_csv("user_data_public.csv", low_memory=False)
    return ok

def initial_clean(ok):
    """
    Perform an initial clean on the dataset. Drop likely irrelevant/
    non-interesting features.

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset after initial clean.
    """
    ok = ok.drop(columns=['lf_single', 'd_religion_seriosity', 'CA', 'gender2',
                          'CA_items', 'gender2_num', 'd_astrology_seriosity',
                          'gender', 'd_astrology_sign', 'd_country', 
                          'd_ethnicity', 'lf_want', 'lf_for', 'd_job',
                          'd_languages','d_relationship', 'lf_location',
                          'd_education_type', 'gender_orientation', 'd_income',
                          'd_bodytype', 'd_offspring_desires'])
    return ok

def binarise_categoricals_str(ok):
    """
    Binarise categorical features that have 'string' type categories, e.g.,
    ‘d_religion_type’, with categories: 'Christianity', 'Buddhism', 'Atheism',
    etc. A new column is created for each category. This new column contains
    either a 1 or a 0 for each row, depending on whether that individual
    belongs to that category.

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset with new binary features.
        new_features (list): a list of lists of newly created features sorted
        by group.
    """
    new_features = []
    list_categorical = ['d_education_phase', 'd_religion_type', 'race']
    for feature in list_categorical:
        unique_categories = [*(ok[feature].unique())]
        unique_categories = [x for x in unique_categories 
                             if str(x) not in ['nan', '-', 'Other']]
        group = []
        for category in unique_categories:
            ok[category] = np.where(ok[feature].isin([category]), 1, 0)
            group.append(category)
        new_features.append(group)
    return ok, new_features

def binarise_categoricals_yesno(ok):
    """
    Binarise categorical features that have 'yes/no' categories. A new column
    is created for each category. This new column contains either a 1 if the
    individual belongs to the positive (yes) category, or a 0 otherwise (no).

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset with new binary features.
    """
    ok['Has kids'] = np.where(ok['d_offspring_current'].isin(['kids']), 1, 0)
    ok['Drugs often'] = np.where(ok['d_drugs'].isin(['Often']), 1, 0)
    ok['Smokes'] = np.where(ok['d_smokes'].isin(['Yes', 'Trying to quit']),
                            1, 0)
    ok['Drinks often'] = np.where(ok['d_drinks'].isin(['Very often', 'Often']),
                                  1, 0)
    return ok
    
def clean_orientation(ok):
    """
    Clean 'd_orientation' feature. This is a feature that contains 160 unique
    categories. Just three of these categories, 'Straight', 'Gay' and
    'Bisexual', are attributed to ~96% of the samples. This functon merges the
    remaining 158 minority orientations into a single binary column,
    ‘Other orientation’.

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset after cleaning 'd_orientation'.
    """
    ok['Straight'] = np.where(ok['d_orientation'].isin(['Straight']), 1, 0)
    ok['Gay'] = np.where(ok['d_orientation'].isin(['Gay']), 1, 0)
    ok['Bisexual'] = np.where(ok['d_orientation'].isin(['Bisexual']), 1, 0)
    ok['Other orientation'] = np.where(~ok['d_orientation'].isin(['Straight',
                                                                  'Gay',
                                                                  'Bisexual'])
                                       , 1, 0)
    return ok

def clean_gender(ok):
    """
    Clean 'd_gender' feature. This is a feature that contains 107 unique
    categories. Just two of these categories, ‘Man’ and ‘Woman’, are attributed
    to ~97% of the samples. This functon merges the remaining 105 minority
    genders into a single binary column, ‘Other gender’.

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset after cleaning 'd_gender'.
    """
    ok['Male'] = np.where(ok['d_gender'].isin(['Man']), 1, 0)
    ok['Female'] = np.where(ok['d_gender'].isin(['Woman']), 1, 0)
    ok['Other gender'] = np.where(~ok['d_gender'].isin(['Man', 'Woman']), 1, 0)
    return ok

def create_binary_features(ok):
    """
    Create new binary features by binarising categorical features and cleaning
    'd_orientation' and 'd_gender'.

    Args:
        ok (pandas.DataFrame): OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): OkCupid dataset with new binary features.
        new_features (list): a list of lists of newly created features sorted
        by group.
    """
    ok, new_features = binarise_categoricals_str(ok)
    ok = binarise_categoricals_yesno(ok)
    ok = clean_orientation(ok)
    ok = clean_gender(ok)
    ok = ok.drop(columns=['d_education_phase','d_religion_type',
                        'd_offspring_current','race',
                        'd_drugs','d_smokes','d_drinks','d_orientation',
                        'd_gender']) #drop columns we just processed
    return ok, new_features

def clean_dataset():
    """
    Load and clean the OkCupid dataset.

    Returns:
        ok (pandas.DataFrame): cleaned OkCupid dataset.
        new_features (list): a list of lists of newly created features sorted
        by group.
    """
    ok = load_dataset()
    ok = initial_clean(ok)
    ok, new_features = create_binary_features(ok)
    return ok, new_features

def save_cleaned_dataset(ok):
    """
    Write the cleaned OkCupid dataset to a .pkl file.

    Args:
        ok (pandas.DataFrame): cleaned OkCupid dataset.
    """
    ok.to_pickle("ok.pkl")

def save_new_features(new_features):
    """
    Add additional groups to 'new_features'. Write this list to a .txt file.

    Args:
        new_features (list): a list of lists of newly created features sorted
        by group.
    """
    substances = ['Drugs often', 'Smokes', 'Drinks often']
    orientation = ['Straight', 'Gay', 'Bisexual', 'Other orientation']
    gender = ['Male', 'Female', 'Other gender']
    new_features = new_features + [substances] + [orientation] + [gender]
    for group in new_features:
        group.insert(0, '')
    with open('new_features.txt', "wb") as f:
        pickle.dump(new_features, f)
        
def save_all_features(ok):
    """
    Write a list of all the features of the dataset to a .txt file.

    Args:
        ok (pandas.DataFrame): cleaned OkCupid dataset.
    """
    ok_no_qs = ok[ok.columns.drop(list(ok.filter(regex='q')))] #remove qs
    features = ok_no_qs.columns.tolist()
    with open('features.txt', 'w') as f:
        for line in features:
            f.write(f"{line}\n")
            
def main():
    """
    Processes to be executed when 'clean_dataset.py' is called.
    """
    ok, new_features = clean_dataset()
    save_cleaned_dataset(ok)
    save_new_features(new_features)
    save_all_features(ok)
    print('Dataset cleaned')
    
if __name__ == "__main__":
    main()