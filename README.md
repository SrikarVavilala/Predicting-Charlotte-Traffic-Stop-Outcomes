# DSBA 6156, Group 3
# Predicting Charlotte Traffic Stop Outcomes

## Data Source
Data is available at the [Charlotte Data Portal](https://data.charlottenc.gov/datasets/officer-traffic-stops/explore).

## Research Questions
1. Which of the **general attributes** correlate the most with the **outcome of the traffic stop** (i.e. search conducted, verbal warning, written warning, citation issued, no action, arrest).
2. What **driver attributes** (race, ethnicity, gender, age) correlate the most with the **outcome of the traffic stop**?
3. What **officer attributes** (race, gender, years of service) correlate the most with the **outcome of the traffic stop**?

## Steps and Approaches
### Preprocessing/clean the dataset: 
- Check for missing values
- Consistency (spelling, etc.)
- Skewness → normalization
### Identify variables to be used. EDA
### Identify most appropriate models to use
- Multi class prediction. 5 different outcomes.
- Binary. Search conducted or not
- Sklearn fairness metrics
### Analysis
- Naive/Gaussian Bayes
- Decision Tree/Random Forest
- Logistic regression
- Parameter tuning
### Visualize/Understand output
### (Potential) Create Streamlit App
If we do create a streamlit app, describe and link [here](google.com).

## Findings
Once finished, findings go here.

## Import Endnotes
We realize that by analyzing this dataset, we could shed light on a potentially controversial topic, that is, how the race/ethnicity/gender of the driver/officier can help to predict the outcome of a traffic stop. 

If this is a finding, it should not be used to guide police targeting, but rather to illuminate bias in traffic stops.  Note that being able to predict the outcome of a traffic stop based on race, ethnicity or gender is inherently unethical/discriminatory. Ideally, traffic stop outcomes based on these characteristics should be proportional to the demographic population of the area under observation.  

Regardless of our findings, we would like to be explicit about the fact that none of our findings are causal. Rather they shed light on correlations in the data that may be used to dismantle bias in policing. 
