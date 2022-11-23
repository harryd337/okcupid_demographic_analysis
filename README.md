# Scientific Programming in Python – submission 2

### Project title: GUI to assist processing of OKCupid dataset to predict answers to personal questions based on personality scales and profile information

### Student name: Harry Durnberger

This project attempts to handle a very large dataset (N=68371, 2620 variables) from the online dating site OKCupid to make predictions about it's users. The dataset consists of basic profile information (gender, age, sexuality); 50 personality scales (continuous) that OKCupid calculates automatically for its users; and categorical answers given to the top 2541 questions on the site. The questions are extremely varied and many are personal, the user is incentivised to answer the questions so that the OKCupid algorithm can match them to someone with similar answers.

[Paper on dataset: https://openpsych.net/files/papers/Kirkegaard_2016g.pdf]

The program 'clean_dataset.py' is used to clean the the dataset, i.e. removing irrelevant and useless features; binarising categorical features; merging minority features. The cleaned dataset is written to "ok.csv". The list of surviving and newly created features is written to "features.txt".

These files are then loaded by the program 'okapp.py'. This is a streamlit application that is run locally and interacted with via the browser. It is used to provide an easy-to-use GUI to help the user process the OKCupid dataset, with the aim of generating an accurate ML model trained to predict answers given to a selected question.

## Use of 'okapp.py':

From the sidebar, the user may select keywords to filter the 2541 questions using a multi-selection widget. The filtered questions are displayed. The user may then choose their desired question from a drop-down widget in the sidebar. The user has the ability to change their mind on these options at any point, the app will display the updated information.

A countplot is displayed for the chosen question's data. The user may then choose to remove one or many categories (options) associated with the question using another multi-selection widget in the sidebar. The countplot and dataset will update accordingly.

## App features not yet implemented:

A checkbox appears under the countplot which, when checked, displays a correlation matrix for all the features of the particular subset of the dataset, as defined by the user's choices. The process of feature selection using the correlation matrix is then explained to the user, and they are given the option to change the hyper-parameters using a number input widget. The user may then press a button (widget) which activates the process of feature selection using the correlation matrix for the dataset. This process systematically removes features that are highly correlated with other features. The threshold for 'high correlation' is a hyper-parameter chosen by the user. Features that are highly correlated with fewer other features are removed first (to ensure the most important features are kept), one at a time, and the correlation matrix is updated each iteration until no highly correlated features remain.

At this point the user may also manually remove features using a multi-selection widget. The user now has the option to use recursive feature selection or sequential feature selection or PCA to further remove irrelevant features / reduce dimensionality. Using a drop-down widget, the user may choose which method to use. Validation using MLP for binary or multiclass classification (depending on selected question and number of chosen categories) may be used in tandem with recursive feature selection or sequential feature selection to evaluate the importance of features. All hyper-parameters may be chosen by the user using number input widgets. A button (widget) is pressed by the user to activate the chosen process.

The MLP is then trained to predict the given answers (categories) of the chosen question. Prediction accuracy is displayed. Cross-validation is used to help determine optimal hyper-parameters, which the user may adjust using number input widgets. A test set is kept aside for final testing of the model. When the user is happy with the chosen hyper-parameters they may choose to run the model on the test set to obtain the final accuracy results, which are then displayed. A confusion matrix will be used to visualise the models performance.

At every point in the process the user is free to go back and change any parameters chosen via widgets. The app will update all displays accordingly.
