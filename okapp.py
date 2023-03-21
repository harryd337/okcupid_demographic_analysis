# OKCupid demographic analysis streamlit application.
#
# This local app is run in the browser.  It is used to provide an easy-to-use
# GUI to help the user filter the demographic of the OKCupid dataset, and 
# observe this demographic's probabilities of giving particular answers to a 
# selected question, in comparison to the full population.
#
# The filtered demographic may be written to "okcupid_demographic.pkl".
#
# Author: Harry Durnberger

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import pickle

@st.cache_resource  # Cache outputs
def load_dataset():
    """Loads the dataset and list of features.

    Returns:
        ok (pandas.DataFrame): cleaned OkCupid dataset.
        features (list): list of all features.
    """
    ok = pd.read_pickle("ok.pkl")
    with open('features.txt', 'r') as f:
        lines = f.readlines()
        features = []
        for l in lines:
            features.append(l.replace("\n",""))
    return ok, features

@st.cache_resource
def load_qs_and_traits(features):
    """Loads questions and traits information.
    
    Divides information into separate dataframes. The questions information is
    the question, options and keywords associated with each question index. The
    traits information is the name of each trait associated with each trait
    index.

    Args:
        features (list): list of all features.

    Returns:
        qs_and_traits (pandas.DataFrame): dataframe containing information
        associated with all questions and traits.
        qs (pandas.DataFrame): dataframe containing information associated with
        all questions.
        total_questions (int): original total number of questions.
        traits (pandas.DataFrame): dataframe containing information associated
        with all traits.
    """
    qs_and_traits = pd.read_csv("question_data.csv", sep=';')
    qs = qs_and_traits[:-79]  # Keep only questions
    qs.Keywords = qs.Keywords.fillna('Other')
    total_questions = len(qs)
    traits = qs_and_traits[qs_and_traits.iloc[:, 0].isin(features)]
    return qs_and_traits, qs, total_questions, traits

@st.cache_resource
def load_new_features():
    """Loads list of new features created in 'clean_dataset.py'.

    Returns:
        new_features (list): list of lists of newly created features sorted
        by group.
    """
    with open("new_features.txt", "rb") as f:
        new_features = pickle.load(f)
    return new_features

@st.cache_resource
def create_traits_dictionary(traits):
    """Creates dictionary for traits and other continuous variables.
    
    The labels are the names of each trait or continuous variable. The values
    are the indexes associated with each label.

    Args:
        traits (pandas.DataFrame): dataframe containing information associated
        with all traits.

    Returns:
        traits (dict): traits dictionary.
    """
    traits = traits.set_index('text').to_dict()['Unnamed: 0']
    return traits

def filter_by_keywords(qs):
    """Sets up the keyword multi-selection tool in the sidebar.
    
    Filters the questions by the selected keywords.

    Args:
        qs (pandas.DataFrame): dataframe containing information associated with
        all questions.

    Returns:
        qs (pandas.DataFrame): dataframe containing information associated with
        filtered questions.
    """
    st.sidebar.subheader("Please filter and select a question:")
    list_keywords = ['descriptive', 'preference', 'opinion', 'sex', 'intimacy',
                    'politics','religion', 'superstition', 'cognitive',
                    'technology', 'BDSM']
    keywords = st.sidebar.multiselect("Select keywords:",
                                    options=list_keywords, default=None)
    for keyword in keywords:
        qs = qs[qs['Keywords'].str.contains(keyword)]
    return qs

def initialise_question_selection(qs):
    """Sets up the question number selection tool in the sidebar.
    
    Cleans the questions dataframe so it only contains questions with their
    corresponding options.

    Args:
        qs (pandas.DataFrame): dataframe containing information associated with
        all/filtered questions.

    Returns:
        chosen_q_num (str): chosen question number.
        qs (pandas.DataFrame): cleaned questions dataframe.
        indexes (numpy.ndarray): original indexes of the unfiltered questions
        dataframe (used to recover chosen question ID).
        num_questions (int): number of questions associated with selected
        keyword(s).
    """
    num_questions = len(qs)
    q_num_range = [*(np.arange(1, num_questions + 1))]
    q_nums_str = [str(x) for x in q_num_range]
    q_nums = [('')]
    q_nums.extend(q_nums_str)
    chosen_q_num = st.sidebar.selectbox("Select question number:",
                                        options=q_nums)
    indexes = qs.index.values
    qs = qs.reset_index()
    qs = qs.drop(columns=['Unnamed: 0', 'N', 'Type', 'Order', 'Keywords',
                          'index'])
    return chosen_q_num, qs, indexes, num_questions

def display_questions(qs):
    """Displays the filtered questions and their corresponding options.
    
    Args:
        qs (pandas.DataFrame): dataframe containing information associated with
        filtered questions.
    """
    for index, row in qs.iterrows():
        st.text(f"Q{index+1}: {row['text']}")
        st.text("")
        st.text(f"Option 1: {row['option_1']}")
        st.text(f"Option 2: {row['option_2']}")
        if pd.isna(row['option_3']) == False:
            st.text(f"Option 3: {row['option_3']}")
        if pd.isna(row['option_4']) == False:
            st.text(f"Option 4: {row['option_4']}")
        st.markdown("""---""")

def initial_main_page(qs, total_questions, num_questions):
    """Sets up initial main page before selection of a question.

    Args:
        qs (pandas.DataFrame): cleaned questions dataframe containing all/filtered questions.
        total_questions (int): original total number of questions.
        num_questions (int): number of questions associated with selected
        keyword(s).
    """
    st.text("Number of questions associated with selected keyword(s):")
    st.text(f"{num_questions}")
    st.text("")
    if num_questions < total_questions:
        if num_questions != 0:
            st.subheader("Questions associated with keyword(s):")
            st.markdown("##")
            display_questions(qs)
        else:
            st.text("Please remove keyword(s).")
    else:
        st.text('To display questions, please select a keyword.')
        
def display_chosen_question(qs, chosen_q_num):
    """Displays the chosen question and associated options to the user.

    Args:
        qs (pandas.DataFrame): dataframe containing information associated with
        filtered questions.
        chosen_q_num (str): chosen question number.

    Returns:
        chosen_q_int (int): chosen question number.
        options (list): list of options corresponding with chosen question.
    """
    chosen_q_int = int(chosen_q_num)
    chosen_q = qs.iloc[[chosen_q_int-1]]
    st.subheader("Chosen question:")
    st.text(f"{chosen_q.iloc[0]['text']}")
    options = []
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
    return chosen_q_int, options

def filter_chosen_question(ok, chosen_q_int, qs_and_traits, features, indexes):
    """Remove all question data except for the chosen question.
    
    Filters out all question data in the OkCupid dataset except for that of
    the chosen question. Finds the ID associated with the chosen question.

    Args:
        ok (pandas.DataFrame): cleaned OkCupid dataset.
        chosen_q_int (int): chosen question number.
        qs_and_traits (pandas.DataFrame): dataframe containing information 
        associated with all questions and traits.
        features (list): list of all features.
        indexes (numpy.ndarray): original indexes of the unfiltered questions
        dataframe.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
        q_number (str): ID of chosen question.
    """
    q_index = indexes[chosen_q_int - 1]
    indexes_of_qs_and_traits = qs_and_traits['Unnamed: 0']
    q_number = (indexes_of_qs_and_traits[[q_index]]).iloc[0]
    columns = features + [q_number]
    ok1 = ok.copy()
    ok1 = ok1[columns].dropna(subset=[q_number])
    return ok1, q_number

def remove_options(ok1, q_number, options):
    """Creates tool allowing the user to select options they wish to remove.
    
    Sets up multi-selection tool in the sidebar allowing the user to select
    options they wish to remove from the chosen question. Filters OkCupid
    dataset by removing individuals that selected the chosen option(s).

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        q_number (str): ID of chosen question.
        options (list): list of options associated with chosen question.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
    """
    options_remove = st.sidebar.multiselect("Select categories to remove:",
                                            options=options, default=None)
    for option in options_remove:
        ok1 = ok1[ok1[q_number] != option]
    return ok1

def categorical_selectboxes(new_features):
    """Creates selectboxes allowing selection of categorical variables.
    
    Sets up selectboxes in the sidebar allowing the user to select categorical
    variables to filter the OkCupid dataset with.

    Args:
        new_features (list): list of lists of newly created features sorted
        by group.

    Returns:
        chosen_all (list): list of all selected categorical variables.
    """
    uni = new_features[0]  # Options of each group
    religion = new_features[1]
    ethnicity = new_features[2]
    substances = new_features[3]
    orientation = new_features[4]
    gender = new_features[5]
    chosen_gender = st.sidebar.selectbox("Gender:", options=gender)
    chosen_orientation = st.sidebar.selectbox("Orientation:",
                                              options=orientation)
    chosen_ethnicity = st.sidebar.selectbox("Ethnicity:", options=ethnicity)
    chosen_religion = st.sidebar.selectbox("Religion:", options=religion)
    chosen_uni = st.sidebar.selectbox("University status:", options=uni)
    chosen_substances = st.sidebar.selectbox("Substances:", options=substances)
    chosen_all = ([chosen_gender] + [chosen_orientation] + [chosen_ethnicity]
                  + [chosen_religion] + [chosen_uni] + [chosen_substances])
    chosen_all = list(filter(None, chosen_all))
    return chosen_all

def categorical_checkboxes():
    """Creates checkboxes in the sidebar for the yes/no categorical variable.

    Returns:
        have_kids (bool): True if the user checks 'Have kids', False otherwise.
        no_kids (bool): True if the user checks 'Don't have kids', False
        otherwise.
    """
    have_kids = st.sidebar.checkbox('Have kids', value=False)
    no_kids = st.sidebar.checkbox("Don't have kids", value=False)
    return have_kids, no_kids

def filter_categoricals(ok1, chosen_all):
    """Filters OkCupid dataset by selected categorical variables.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        chosen_all (list): list of all chosen categoricals.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
    """
    ok_list = []
    for category in chosen_all:
        ok2 = ok1.copy()
        ok_list.append(ok2[ok2[category] == 1])
    ok1 = pd.concat(ok_list).drop_duplicates().reset_index(drop=True)
    for category in chosen_all:
        ok1 = ok1[ok1[category] == 1]
    return ok1

def categorical_selection(ok1, new_features):
    """Creates categorical selectboxes and checkboxes in the sidebar.
    
    Filters the OkCupid dataset according to the user's selections.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        new_features (list): list of lists of newly created features sorted
        by group.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
        made_selection (bool): True if the user has made a selection, False
        otherwise.
    """
    st.sidebar.subheader("Please filter the demographic:")
    chosen_all = categorical_selectboxes(new_features)
    made_selection = False
    if len(chosen_all) > 0:
        made_selection = True
        ok1 = filter_categoricals(ok1, chosen_all)
    have_kids, no_kids = categorical_checkboxes()
    if have_kids:
        made_selection = True
        ok1 = ok1[ok1['Has kids'] == 1]
    if no_kids:
        made_selection = True
        ok1 = ok1[ok1['Has kids'] == 0]
    return ok1, made_selection

def continuous_multiselect(traits):
    """Creates tools for selecting traits and other continuous variables.
    
    Sets up multi-select tools in the sidebar allowing the user to select
    traits and other continuous variables to filter the OkCupid dataset with.

    Args:
        traits (dict): traits dictionary.

    Returns:
        chosen_traits (list): list of chosen traits and other continuous
        variables.
    """
    keys = list(traits.keys())
    keys_traits = sorted(keys[0:50])
    keys_other = keys[50:53]
    chosen_traits = st.sidebar.multiselect("Traits:", 
                                           options=keys_traits, default=None)
    chosen_other = st.sidebar.multiselect("Other:", 
                                          options=keys_other, default=None)
    chosen_traits = [*chosen_traits] + [*chosen_other]  # Lump together
    return chosen_traits

def percentile_range(chosen_traits, traits):
    """Provides percentile range sliders for each chosen trait.
    
    Provides percentile range sliders to allow the user to choose
    the percentile range over which to filter the chosen traits. Displays the
    chosen range to the user.
    
    Args:
        chosen_traits (list): list of names of chosen traits.
        traits (dict): traits dictionary.

    Returns:
        selected_range (numpy.ndarray): matrix of chosen percentile range
        boundary values.
        chosen_trait_ids (list): list of IDs corresponding to chosen traits.
    """
    selected_range = np.zeros(shape=(len(chosen_traits), 2))
    lower = 0
    upper = 0
    chosen_trait_ids = []
    for t, chosen_trait in enumerate(chosen_traits):
        chosen_trait_ids.append(traits[chosen_trait])
        st.text(f"'{chosen_trait}'")
        lower = st.slider('Choose lower percentile range boundary:', 
                                min_value=0, max_value=100,
                                key=(f"{chosen_trait}.low"))
        upper = st.slider('Choose upper percentile range boundary:', 
                                min_value=0, max_value=100, value=100,
                                key=(f"{chosen_trait}.high"))
        selected_range[t, 0] = lower
        selected_range[t, 1] = upper
        if lower == 0 and upper != 0:
            if upper == 100:
                st.text("Chosen percentile range:")
                st.text("Entire range (100%)")
            else:
                st.text("Chosen percentile range:")
                st.text(f"{lower}-{upper} (bottom {upper}%)")
        elif lower != 0 and upper == 100:
            st.text("Chosen percentile range:")
            st.text(f"{lower}-{upper} (top {upper - lower}%)")
        elif lower > upper:
            st.text('Invalid percentile range.')
        else:
            st.text("Chosen percentile range:")
            st.text(f"{lower}-{upper}")
        st.markdown("""---""")
    return selected_range, chosen_trait_ids

def filter_traits(ok1, selected_range, chosen_trait_ids):
    """Filters the OkCupid dataset by selected continuous variables.
    
    Filters each trait by the corresponding selected percentile range. The
    lower and upper percentile bounds of each continuous variable are scaled to
    the range of values in 'ok1'.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        selected_range (numpy.ndarray): matrix of chosen percentile range
        boundary values.
        chosen_trait_ids (list): list of IDs corresponding to chosen traits.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
    """
    for i, trait in enumerate(chosen_trait_ids):
        total_range = ok1[trait].max() - ok1[trait].min()
        lowerbound = selected_range[i, 0]*0.01*total_range + ok1[trait].min()
        upperbound = selected_range[i, 1]*0.01*total_range + ok1[trait].min()
        ok1 = ok1[(ok1[trait] >= lowerbound) & (ok1[trait] <= upperbound)]
    return ok1

def continuous_selection(ok1, made_selection, traits):
    """Creates tools to allow selection of continuous variables.
    
    Creates multi-select tools in the sidebar to allow selection of continuous
    variables. Provides percentile range sliders to allow the user to choose
    the percentile range over which to filter the traits. Filters the OkCupid
    dataset according to the user's selections.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        made_selection (bool): True if the user has previously made a
        selection, False otherwise.
        traits (dict): traits dictionary.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
        made_selection (bool): True if the user has made a selection, False
        otherwise.
    """
    chosen_traits = continuous_multiselect(traits)
    if len(chosen_traits) > 0:
        made_selection = True
        st.subheader("Chosen traits:")
        selected_range, chosen_trait_ids = percentile_range(chosen_traits,
                                                            traits)
        ok1 = filter_traits(ok1, selected_range, chosen_trait_ids)
    return ok1, made_selection

def selection(ok1, new_features, traits):
    """Creates tools allowing the selection of variables. Filters the dataset.
    
    Creates tools in the sidebar allowing the user to select variables they
    wish to filter the OkCupid dataset with. Filters the OkCupid dataset
    according to the user's selections.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        new_features (list): list of lists of newly created features sorted
        by group.
        traits (dict): traits dictionary.

    Returns:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
        made_selection (bool): True if the user has made a selection, False
        otherwise.
    """
    ok1, made_selection = categorical_selection(ok1, new_features)
    ok1, made_selection = continuous_selection(ok1, made_selection, traits)
    return ok1, made_selection

def plot_histogram(ok1, q_number, demographic):
    """Plots a histogram for the population or the chosen demographic.
    
    Plots a histogram showing the counts of each option of the
    chosen question for either the population or the chosen demographic.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        q_number (str): ID of chosen question.
        demographic (str): name of particular demographic.
    """
    count = px.histogram(ok1, x=q_number, title=(f'{demographic} countplot:'),
                         text_auto=True)
    count.update_xaxes(categoryorder='category ascending')
    st.plotly_chart(count,theme="streamlit")
    
def display_probabilities(ok1, q_number, demographic):
    """Displays the probabilities of each option for a demographic.
    
    Displays the probabilities of an individual in either the population or the
    chosen demographic selecting any one of the options of the chosen question.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset.
        q_number (str): ID of chosen question.
        demographic (str): name of particular demographic.
    """
    counts = ok1[q_number].value_counts()  # Counts in descending order
    st.text("Probability of an individual choosing each option from "
            f"{demographic}:")
    st.text("")
    last_option = len(counts) - 1
    for i, count in enumerate(counts):
        p = count/np.sum(counts)  # Probability of the option
        if i == 0:
            st.text(f"{counts.index[i]} : {int(100*p)}% (most likely)")
        elif i == last_option:
            st.text(f"{counts.index[i]} : {int(100*p)}% (least likely)")
        else:
            st.text(f"{counts.index[i]} : {int(100*p)}%")

def population_analysis(ok1, q_number):
    """Plots a histogram and displays probabilities for the population.
    
    Perform analysis on the total population of the OkCupid dataset that
    answered the chosen question. Plots a histogram and displays the
    probabilities of an individual in the population selecting any one of the
    options of the chosen question.
    
    Args:
        ok1 (pandas.DataFrame): OkCupid dataset before selection.
        q_number (str): ID of chosen question.
    """
    plot_histogram(ok1, q_number, 'Population')
    display_probabilities(ok1, q_number, 'population')
    st.markdown("""---""")

def chosen_demographic_analysis(ok1, q_number):
    """Plots a histogram and displays probabilities for the chosen demographic.
    
    Perform analysis on the chosen demographic of the OkCupid dataset that
    answered the chosen question. Plots a histogram and displays the
    probabilities of an individual in the demographic selecting any one of the
    options of the chosen question. Provides a checkbox that may be used to
    display the filtered dataframe to the user.

    Args:
        ok1 (pandas.DataFrame): OkCupid dataset after selection.
        q_number (str): ID of chosen question.
    """
    if len(ok1[q_number]) == 0:
        st.text('No data for chosen demographic.')
    else:
        st.subheader('Chosen demographic analysis:')
        plot_histogram(ok1, q_number, 'Chosen demographic')
        display_probabilities(ok1, q_number, 'chosen demographic')
        st.markdown("##")
        df_check = st.checkbox('Display dataframe', value=False)
        if df_check:
            st.dataframe(ok1)

def save_demographic(ok1):
    """Creates a button for saving the filtered dataframe to a .pkl file.
    
    Provides a clickable button for the user to press if they desire to save
    the filtered dataframe. If pressed, saves the dataframe to
    'okcupid_demographic.pkl'.

    Args:
        ok1 (pandas.DataFrame): filtered OkCupid dataset.
    """
    if st.button('Save dataframe'):
        ok1.to_pickle('okcupid_demographic.pkl')
    st.text("Click here to save dataframe of chosen demographic to \
'okcupid_demographic.pkl'")

def main():
    """Executes when the app is launched and whenever it is refreshed.
    
    Note that the outputs of the functions used to load the data and create the
    traits dictionary are cached. These functions run once when the app is
    launched and are ignored when it is later refreshed.
    """
    ok, features = load_dataset()
    qs_and_traits, qs, total_questions, traits = load_qs_and_traits(features)
    new_features = load_new_features()
    traits = create_traits_dictionary(traits)
    qs = filter_by_keywords(qs)
    (chosen_q_num, qs, indexes,
     num_questions) = initialise_question_selection(qs)
    if chosen_q_num == '':
        initial_main_page(qs, total_questions, num_questions)
    elif chosen_q_num != '':  # If the user has selected a question
        chosen_q_int, options = display_chosen_question(qs, chosen_q_num)
        ok1, q_number = filter_chosen_question(ok,
                                               chosen_q_int,
                                               qs_and_traits,
                                               features,
                                               indexes)
        ok1 = remove_options(ok1, q_number, options)
        population_analysis(ok1, q_number)
        ok1, made_selection = selection(ok1, new_features, traits)
        if made_selection:
            chosen_demographic_analysis(ok1, q_number)
            save_demographic(ok1)
        else:
            st.text('Please filter the demographic.')


st.set_page_config(page_title="OkCupid Demographic Analysis",
                   page_icon=":mag:", layout="wide")
main()
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)