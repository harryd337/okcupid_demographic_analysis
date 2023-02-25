# OkCupid Demographic Analysis Tool

### Project title: GUI for filtering demographic of OkCupid dataset based on personality scales and profile information to observe corresponding probabilities of answers to personal questions

### Author: Harry Durnberger

This project attempts to handle a very large dataset (N=68371, 2620 variables) from the online dating site OkCupid. The dataset consists of a total of 83 features, including basic profile information (gender, age, sexuality, etc.) and 50 continuous personality scales (confidence, creativity, honesty, etc.) that OkCupid calculates automatically for its users. In addition, there are categorical answers given to the top 2541 multiple-choice questions on the site. The questions are extremely varied and many are personal, the user is incentivised to answer the questions so that the OkCupid algorithm can match them to someone with similar answers.

Paper on dataset: https://openpsych.net/files/papers/Kirkegaard_2016g.pdf [Kirkegaard, E. O. W., & Bjerrekær, J. D. (2016). The OKCupid dataset: A very large public dataset of dating site users. Open Differential Psychology. https://doi.org/10.26775/odp.2016.11.03]

To download the datasets, go to, https://mega.nz/folder/QIpXkL4Q#b3QXepE6tgyZ3zDhWbv1eg/folder/VIgyCDIQ, and download 'question_data.csv' and 'user_data_public.7z'. Unzip the latter and save both .csv files to the same directory.

The program 'clean_dataset.py' is used to clean the the dataset, i.e. removing irrelevant and useless features; binarising categorical features; merging minority features. The program is to be run in the same directory as the .csv files. The cleaned dataset is written to 'ok.pkl'. The list of surviving and newly created features is written to 'features.txt'. A list of only the newly created features is written to 'new_features.txt'.

These files are then loaded by the program 'okapp.py'. This is a streamlit application that is run locally and interacted with via the browser. It is used to provide an easy-to-use GUI to help the user filter the demographic of the OkCupid dataset, and observe this demographic's probabilities of giving particular answers to a selected question, in comparison to that of the full population.

This app may be used as a tool for researchers or businesses to gain useful insight into a particular demographic’s opinions on divisive topics. A researcher may use this information in preparation for their own investigations. A business may use this information to better understand their target market.

## Use of 'clean_dataset.py':

With 'user_data_public.csv' in the same directory, 'clean_dataset.py' may be run from the terminal by executing the following command:

```
python clean_dataset.py
```

## Use of 'okapp.py':

An environment capable of running the application may be imported in Anaconda via the environment file, 'ok_env.yaml'. After importing the environment, you may have to manually install streamlit by executing the following command in the Anaconda prompt:

```
pip install streamlit
```

Download 'okapp.py' into the same directory as the cleaned dataset and the text files outputted from 'clean_dataset.py'.

To run the app as a streamlit application in the browser, go to the Anaconda prompt and execute:

```
streamlit run okapp.py
```

The app will launch in the browser.

From the sidebar, the user may select keywords to filter the 2541 questions using a multi-selection widget. The filtered questions are displayed. The user may then choose from one of these questions via a drop-down widget in the sidebar. The user has the ability to change their mind on these selections at any point, the app will display the updated information.

A countplot is displayed for the chosen question's data. The user may then choose to remove one or many categories (options) associated with the question using another multi-selection widget in the sidebar. The countplot and dataset will update accordingly.

Probabilities of the population giving any one of the options of the chosen question are then displayed, with the most likely and least likely options highlighted.

The user is then able to filter the demographic via drop-downs in the sidebar. The demographic may be filtered by categorical background information, or by continuous personality trait percentile ranges, or by a combination of an arbitrary number of both.

Upon selecting a personality trait, sliders for the lower and upper bounds of the chosen trait appear to the user. The user may use these to select the percentile range of the trait by which the dataset will be filtered.

After the user has selected the demographic, a new corresponding countplot is displayed for the chosen question's data, specific to the chosen demographic. Probabilities of the chosen demographic giving any one of the options of the chosen question are then displayed, with the most likey and least likley options highlighted.

The user also has the option to tick a box to display the dataframe containing the filtered data.

The user may save the filtered dataframe to 'okcupid_demographic.pkl' by pressing the button, "Save dataframe".

## Example use of 'okapp.py':

https://user-images.githubusercontent.com/100152207/218328778-b5176c10-57a0-4aa2-a923-2fa46cd56447.mp4

##
Feel free to fork the repo and play with / expand on the code however you like.



