# Scientific Programming in Python – submission 2

### Project title: GUI for filtering demographic of OkCupid dataset based on personality scales and profile information to observe corresponding probabilities of answers to personal questions

### Student name: Harry Durnberger

This project attempts to handle a very large dataset (N=68371, 2620 variables) from the online dating site OkCupid. The dataset consists of a total of 83 features, including basic profile information (gender, age, sexuality, etc.) and 50 continuous personality scales (confidence, creativity, honesty, etc.) that OkCupid calculates automatically for its users. In addition, there are categorical answers given to the top 2541 questions on the site. The questions are extremely varied and many are personal, the user is incentivised to answer the questions so that the OkCupid algorithm can match them to someone with similar answers.

[Paper on dataset: https://openpsych.net/files/papers/Kirkegaard_2016g.pdf]

The program 'clean_dataset.py' is used to clean the the dataset, i.e. removing irrelevant and useless features; binarising categorical features; merging minority features. The cleaned dataset is written to 'ok.csv'. The list of surviving and newly created features is written to 'features.txt'. A list of only the newly created features is written to 'new_features.txt'.

These files are then loaded by the program 'okapp.py'. This is a streamlit application that is run locally and interacted with via the browser. It is used to provide an easy-to-use GUI to help the user filter the demographic of the OkCupid dataset, and observe this demographic's probabilities of giving particular answers to a selected question, in comparison to that of the full population.

## Use of 'okapp.py':

If you'd like to run the app with the cleaned dataset, download 'okapp.py', 'ok.csv' (650MB), 'question_data.csv', 'features.txt' and 'new_features.txt' into the same directory.

To run the app as a streamlit application in the browser, go to Anaconda prompt and execute:

```
streamlit run okapp.py
```

The app will launch in the browser.

From the sidebar, the user may select keywords to filter the 2541 questions using a multi-selection widget. The filtered questions are displayed. The user may then choose from one of these questions via a drop-down widget in the sidebar. The user has the ability to change their mind on these selections at any point, the app will display the updated information.

A countplot is displayed for the chosen question's data. The user may then choose to remove one or many categories (options) associated with the question using another multi-selection widget in the sidebar. The countplot and dataset will update accordingly.

Probabilities of the population giving any one of the options of the chosen question are then displayed, with the most likey and least likely options highlighted.

The user is then able to filter the demographic via drop-downs in the sidebar. The demographic may be filtered by categorical background information, or by continuous personality trait percentile ranges, or by a combination of an arbitrary number of both.

Upon selecting a personality trait, sliders for the lower and upper bounds of the chosen trait appear to the user. The user may use these to select the percentile range of the trait by which the dataset will be filtered.

After the user has selected the demographic, a new corresponding countplot is displayed for the chosen question's data, specific to the chosen demographic. Probabilities of the chosen demographic giving any one of the options of the chosen question are then displayed, with the most likey and least likley options highlighted.

The user also has the option to tick a box to display the dataframe containing the filtered data.
