#OKCupid data analysis streamlit application.

#Created on Mon Nov 21 10:13:23 2022
#@author: Harry Durnberger

#This local app is run in the browser. It is used to provide an easy-to-use
# GUI to help the user process the OKCupid dataset, with the aim of generating
# an accurate ML model trained to predict answers given to a selected question.

#The user can select keywords to filter the 2541 questions. The filtered
# questions are displayed. The user may then choose their desired question.

#A countplot is displayed for the chosen question's data. The user may choose
# to remove one or many categories (options) associated with the question. The
# countplot and dataset will update accordingly.
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from collections import defaultdict
from collections import Counter
st.set_page_config(page_title="OKCupid Data Analysis",
                   page_icon=":mag:", layout="wide")
#singleton functions run once and then do nothing if called again:
@st.experimental_singleton
def load_dataset():
    #function to load the dataset and list of features.
    ok = pd.read_csv("ok.csv")
    with open('features.txt', 'r') as f: #read list of features from text file
        lines = f.readlines()
        features =[]
        for l in lines:
            features.append(l.replace("\n",""))
    return ok, features
#this function runs only once to avoid loading the dataset each update:
ok,features = load_dataset()
@st.experimental_singleton
def load_qs_and_traits(features):
    #function to load questions + traits information.
    qs_and_traits = pd.read_csv("question_data.csv",';')
    #keep only the questions:
    qs = qs_and_traits[:-79] #remove traits
    qs.Keywords = qs.Keywords.fillna('Other') #fills NaNs
    qs_total = qs
    #now use list of features to keep only the traits:
    traits = qs_and_traits[qs_and_traits.iloc[:,0].isin(features)] #remove qs
    return qs_and_traits, qs_total, qs, traits
#this function runs only once:
qs_and_traits, qs_total, qs, traits = load_qs_and_traits(features)
@st.experimental_singleton
def load_new_features():
    #function to load list of new features created in 'clean_dataset.py'.
    #returns lists of features sorted into appropriate groups.
    with open("new_features.txt", "rb") as f:
        new_features = pickle.load(f)
    #create lists for each group of newly created features:
    uni = new_features[0]
    uni.insert(0, '') #insert a blank initial value to the category list
    religion = new_features[1]
    religion.insert(0, '')
    ethnicity = new_features[2]
    ethnicity.insert(0, '')
    substances = new_features[4]
    substances.insert(0, '')
    orientation = new_features[5]
    orientation.insert(0, '')
    gender = new_features[6]
    gender.insert(0, '')
    return uni, religion, ethnicity, substances, orientation, gender
(uni, religion, ethnicity,
 substances, orientation, gender) = load_new_features()
@st.experimental_singleton
def traits_dictionary(traits):
    #function to create dictionary for personality traits
    traits = traits.set_index('text').to_dict()['Unnamed: 0']
    return traits
traits = traits_dictionary(traits) #this function runs only once
#reuseable functions:
def display_questions(qs):
    #loops over questions, show the question and possible answers for each:
    for index, row in qs.iterrows():
        st.text(f"Q{index+1}: {row['text']}")
        st.text("")
        st.text(f"Option 1: {row['option_1']}")
        st.text(f"Option 2: {row['option_2']}")
        #some questions have more than two options:
        if pd.isna(row['option_3']) == False:
            st.text(f"Option 3: {row['option_3']}")
        if pd.isna(row['option_4']) == False:
            st.text(f"Option 4: {row['option_4']}")
        st.markdown("""---""")
def display_chosen_question(chosen_q):
    #displays the chosen question and options to the user.
    #returns list of associated options.
    st.subheader("Chosen question:")
    st.text(f"{chosen_q.iloc[0]['text']}")
    st.text("")
    options = [] #list to contain all options associated with chosen question
    option1 = chosen_q.iloc[0]['option_1']
    options.append(option1)
    st.text(f"Option 1: {option1}")
    option2 = chosen_q.iloc[0]['option_2']
    options.append(option2)
    st.text(f"Option 2: {option2}")
    if pd.isna(chosen_q.iloc[0]['option_3']) == False:
        option3 = chosen_q.iloc[0]['option_3']
        options.append(option3)
        st.text(f"Option 3: {option3}")
    if pd.isna(chosen_q.iloc[0]['option_4']) == False:
        option4 = chosen_q.iloc[0]['option_4']
        options.append(option4)
        st.text(f"Option 4: {option4}")
    return options
def filter_chosen_question():
    #function to filter all question data in the dataset except for the chosen
    # question.
    #returns filtered dataset and chosen question id.
    q_index = indexes[chosen_q_int-1] #finds the index of the chosen question
    indexes_of_qs_and_traits = qs_and_traits['Unnamed: 0']
    #finds the question number associated with the index:
    q_number = (indexes_of_qs_and_traits[[q_index]]).iloc[0]
    cols = features + [q_number] #add chosen question to list of features
    ok1 = ok.copy() #ensures original loaded dataset is not changed
    #cleaned dataset with all features + single 'ouput' question column:
    ok1 = ok1[cols]
    #removes rows where the question column has no data:
    ok1 = ok1.dropna(subset=[q_number])
    return ok1, q_number
def percentile_range():
    #function to provide percentile range sliders to allow the user to choose
    # the percentile range over which to filter the traits.
    #returns matrix of percentile range boundary values and associated trait
    # identifiers.
    num_chosen_traits = len(chosen_traits)
    feature_range = np.zeros(shape=(num_chosen_traits,2)) #define empty matrix
    lower = 0
    upper = 0
    chosen_trait_ids = []
    for t in range(num_chosen_traits): #loop over number of chosen traits
        chosen_trait = chosen_traits[t] #select a particular trait
        #use traits dictionary to find trait ID and add this to the list:
        chosen_trait_ids.append(traits[chosen_trait])
        st.text(f"'{chosen_trait}'")
        #slider on mainpage to allow the user to select the lower percentile
        # range boundary for the trait:
        lower = st.slider('Choose lower percentile range boundary:', 
                                min_value=0, max_value=100,
                                key=(f"{chosen_trait}.low"))
        #slider for the upper boundary:
        upper = st.slider('Choose upper percentile range boundary:', 
                                min_value=0, max_value=100,
                                key=(f"{chosen_trait}.high"))
        #add the selected percentile range boundaries to the matrix of ranges:
        feature_range[t,0] = lower
        feature_range[t,1] = upper
        #display the chosen range to the user:
        if lower == 0 and upper != 0: #lower boundary
            st.text("Chosen percentile range:")
            st.text(f"{lower}-{upper} (bottom {upper}%)")
        elif lower != 0 and upper == 100: #upper boundary
            st.text("Chosen percentile range:")
            st.text(f"{lower}-{upper} (top {upper-lower}%)")
        elif lower > upper:
            st.text('Invalid percentile range.')
        else: #middle boundary
            st.text("Chosen percentile range:")
            st.text(f"{lower}-{upper}")
        st.markdown("""---""")
    return feature_range, chosen_trait_ids
def filter_traits(ok1):
    #function to filter dataset by selected traits and their associated
    # selected percentile range.
    trait_ids = list(traits.values()) #list of trait ids from traits dictionary
    #subtract list of chosen trait ids from list of all trait ids:
    trait_ids_to_remove = list((Counter(trait_ids) - 
                                Counter(chosen_trait_ids)).elements())
    #drop traits the user has not selected:
    ok1 = ok1.drop(columns=[*trait_ids_to_remove])
    for i, trait in enumerate(chosen_trait_ids): #loop over chosen traits
        #lower and upper bounds are defined by the chosen percentile range
        # boundary values, contained in the 'feature_range' matrix, scaled to
        # the range of trait values (-100-100)
        lowerbound = feature_range[i,0]*0.01*200-100
        upperbound = feature_range[i,1]*0.01*200-100
        #use lower and upper bounds to filter the dataset accordingly:
        ok1 = ok1[(ok1[trait] > lowerbound) & (ok1[trait] < upperbound)]
    return ok1
def filter_categoricals(ok1):
    ok_list = [] #list of datasets
    for category in chosen_all: #loop over each chosen category
        #create new dataset that only contains 1s in the chosen category,
        # and append this to the list of datasets:
        ok2 = ok1.copy()
        ok_list.append(ok2[ok2[category] == 1])
    #redefine original dataset as concatenation of list of datasets with
    # duplicates dropped:
    ok1 = pd.concat(ok_list).drop_duplicates().reset_index(drop=True)
    for category in chosen_all: #loop over each chosen category once more
        #keep only rows containing a 1 for every chosen category:
        ok1 = ok1[ok1[category] == 1]
    return ok1
st.sidebar.subheader("Please filter and select a question:")
#list of keywords to help the user filter the (2541) questions:
list_keywords = ['descriptive', 'preference', 'opinion', 'sex', 'intimacy',
                 'politics','religion', 'superstition', 'cognitive',
                 'technology', 'BDSM']
#keyword multi-selection tool in the sidebar:
keywords = st.sidebar.multiselect("Select keywords:",
                                  options=list_keywords, default=None)
#filters questions dataset by chosen keywords:
for keyword in keywords:
    qs = qs[qs['Keywords'].str.contains(keyword)]
#generates a list the length of the num. of questions of the filtered dataset
# + a blank initial value:
q_nums = [('')]
q_num_range = [*(np.arange(1,len(qs)+1))] #integer number range for num. of qs
q_nums_str = [str(x) for x in q_num_range]
q_nums.extend(q_nums_str)
#question number selection tool in the sidebar with blank initial value:
chosen_q_num = st.sidebar.selectbox("Select question number:", options=q_nums)
#stores an array of the indexes for the set of filtered questions:
indexes = qs.index.values #used to recover chosen question id
qs = qs.reset_index()
#drop unnecessary columns:
qs=qs.drop(columns=['Unnamed: 0', 'N', 'Type', 'Order', 'Keywords', 'index'])
if chosen_q_num == '': #initial layout before selection of a question
    st.text("Number of questions associated with selected keyword(s):")
    st.text(f"{len(qs)}")
    st.text("")
    if len(qs) < len(qs_total): #if the user has selected a keyword
        if len(qs) != 0:
            st.subheader("Questions associated with keyword(s):")
            st.markdown("##")
        else: #if there are no questions associated with selected keywords
            st.text("Please remove keyword(s).")
        display_questions(qs)
    else: #if the user has not yet selected a keyword
        st.text('To display questions, please select a keyword.')
elif chosen_q_num != '': #if the user has selected a question
    chosen_q_int = int(chosen_q_num)
    chosen_q = qs.iloc[[chosen_q_int-1]] #selects the chosen question
    #displays chosen question and associated options to the user:
    options = display_chosen_question(chosen_q)
    #filter dataset by chosen question:
    ok1, q_number = filter_chosen_question()
    #multi-selection tool in the sidebar for options the user wishes to remove:
    options_remove = st.sidebar.multiselect("Select categories to remove:",
                                            options=options, default=None)
    for option in options_remove: #loop over options to remove
        #keep only rows with values not equal to the option to remove
        ok1 = ok1[ok1[q_number] != option]
    #plot a histogram displaying the counts of each remaining option:
    count = px.histogram(ok1, x=q_number, title='Population countplot:',
                         text_auto=True)
    st.plotly_chart(count,theme="streamlit")
    st.markdown("""---""")
    st.sidebar.subheader("Please filter the demographic:")
    keys_traits = list(traits.keys()) #the keys of the traits dictionary
    #multi-selection tool in the sidebar to select traits:
    chosen_traits = st.sidebar.multiselect("Traits:", 
                                   options=keys_traits, default=None)
    made_selection = False
    if len(chosen_traits) > 0: #if the user has chosen at least one trait
        made_selection = True
        st.subheader("Chosen traits:")
        #percentile range sliders for the chosen traits:
        feature_range, chosen_trait_ids = percentile_range()
        ok1 = filter_traits(ok1) #filter the dataset accordingly
    #selectboxes in the sidebar for the user to choose a category to filter by:
    chosen_gender = st.sidebar.selectbox("Gender:", options=gender)
    chosen_orientation = st.sidebar.selectbox("Orientation:",
                                              options=orientation)
    chosen_ethnicity = st.sidebar.selectbox("Ethnicity:", options=ethnicity)
    chosen_religion = st.sidebar.selectbox("Religion:", options=religion)
    chosen_uni = st.sidebar.selectbox("University status:", options=uni)
    chosen_substances = st.sidebar.selectbox("Substances:", options=substances)
    #list of all chosen categories:
    chosen_all = ([chosen_gender] + [chosen_orientation] + [chosen_ethnicity]
                  + [chosen_religion] + [chosen_uni] + [chosen_substances])
    chosen_all = list(filter(None, chosen_all)) #remove blank values
    if len(chosen_all) > 0: #if the user has chosen at least one category
        made_selection = True
        ok1 = filter_categoricals(ok1)
    #checkboxes in the sidebar for yes/no categorical:
    have_kids = st.sidebar.checkbox('Have kids', value=False)
    no_kids = st.sidebar.checkbox("Don't have kids", value=False)
    if have_kids:
        made_selection = True
        ok1 = ok1[ok1['kids'] == 1] #only include people with kids
    elif no_kids:
        made_selection = True
        ok1 = ok1[ok1['kids'] == 0] #only include people with no kids
    if made_selection: #if the user has filtered the demographic in some way
        #plot a histogram displaying the counts of each option of the selected
        # demographic:
        count = px.histogram(ok1, x=q_number, text_auto=True,
                            title='Selected demographic countplot:')
        st.plotly_chart(count,theme="streamlit")
        #option to display filtered dataframe:
        df_check = st.checkbox('Display dataframe', value=False)
        if df_check:
            st.dataframe(ok1)
    else: #if the user has not filtered the demographic in some way
        st.text('Please filter the demographic.')
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)