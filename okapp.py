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
st.set_page_config(page_title="OKCupid Data Analysis",
                   page_icon=":mag:", layout="wide")
#singleton functions run once and then do nothing if called again:
@st.experimental_singleton
def load_dataset(): #function to load the dataset and list of features
    ok = pd.read_csv("ok.csv")
    with open('features.txt', 'r') as f: #read list of features from text file
        lines = f.readlines()
        features =[]
        for l in lines:
            features.append(l.replace("\n",""))
    return ok,features
#this function runs only once to avoid loading the dataset each update:
ok,features = load_dataset()
@st.experimental_singleton
def load_qs(): #function to load questions + traits info
    qs_and_traits = pd.read_csv("question_data.csv",';')
    qs = qs_and_traits[:-79] #remove personality traits
    qs.Keywords = qs.Keywords.fillna('Other') #fills NaNs
    qs_total = qs
    return qs_and_traits,qs_total,qs
#this function runs only once:
qs_and_traits,qs_total,qs = load_qs()

# ---- INITIAL SIDEBAR ----

st.sidebar.header("Please filter and select a question:")
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
list1 = [('')]
list2 = [*(np.arange(1,len(qs)+1))] 
list3 = [str(x) for x in list2]
list1.extend(list3)
#question number selection tool in the sidebar with blank initial value:
chosen_q_num = st.sidebar.selectbox("Select question number:",
                                    options=list1, index=0)

# ---- MAINPAGE ----

#stores an array of the indexes for the set of filtered questions:
indexes = qs.index.values
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
    else: #if the user has not yet selected a keyword
        st.text('To display questions, please select a keyword.')

elif chosen_q_num != '': #if the user has selected a question
    chosen_q_int = int(chosen_q_num)
    chosen_q = qs.iloc[[chosen_q_int-1]] #selects the chosen question
    st.subheader("Chosen question:")
    #displays the chosen question and options to the user:
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
    q_index = indexes[chosen_q_int-1] #finds the index of the chosen question
    indexes_of_qs_and_traits = qs_and_traits['Unnamed: 0']
    #finds the question number associated with the index:
    q_number = (indexes_of_qs_and_traits[[q_index]]).iloc[0]
    cols = features + [q_number] #add chosen question to list of features
    ok1 = ok.copy()
    #cleaned dataset with all features + single 'ouput' question column:
    ok1 = ok1[cols]
    #(makes dataset easier to work with initially, remove line later):
    ok1 = ok1.drop(ok1.index[1000:])
    #removes rows where the question column has no data:
    ok1 = ok1.dropna(subset=[q_number])
    #multi-selection tool in the sidebar for options the user wishes to remove:
    options_remove = st.sidebar.multiselect("Select categories to remove:",
                                            options=options, default=None)
    for option in options_remove: #loop over options to remove
        #remove all rows in dataset with values equal to the option to remove
        ok1 = ok1[ok1[q_number] != option]
    st.dataframe(ok1)
    #plot a histogram displaying the counts of each remaining option:
    count = px.histogram(ok1, x=q_number, text_auto=True)
    st.plotly_chart(count,theme="streamlit")
    #plot a correlation matrix of all the features:
    corr_mat = ok1.corr().round(3)
    st.write(corr_mat)
    fig = plt.figure(figsize = (100,50))
    heat_map = sns.heatmap(corr_mat, annot = True)
    st.pyplot(fig)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)