
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from st_btn_select import st_btn_select
import datetime as dt

stops = pd.read_csv("stops_2020_trimmed.csv")
isinstance(stops['Month_of_Stop'], dt.date) # False
stops['Month_of_Stop'] = stops['Month_of_Stop'].astype('datetime64[ns]')
stops['Month_of_Stop'] = pd.to_datetime(stops['Month_of_Stop'], format='%y%m%d')
stops['Month_of_Stop'] = pd.to_datetime(stops['Month_of_Stop']).dt.date
#stops['Was_a_Search_Conducted'] = [1 if x == 0 else 0 for x in stops['Was_a_Search_Conducted']]
stops['Was_a_Search_Conducted']= 1 - stops['Was_a_Search_Conducted']
from PIL import Image

page = st_btn_select(
  # The different pages
  ('Home Page','Drivers', 'CMPD Divisions & Officers'),
  # Enable navbar
  nav=True
)

# Display the right things according to the page
if page == 'Home Page':
    st.write(

# Intro text

    '''
    # Predicting CMPD Traffic Stops Outcomes
    '''
    )
    image = Image.open('pulled_over_green.png')
    st.image(image)
    
    st.write(
    '''
    Using the public dataset from **[Charlotte Data Portal](https://data.charlottenc.gov/datasets/charlotte::officer-traffic-stops/explore)** we set out to answer the following questions:
       
    * How can Machine Learning techniques be used with sociopolitical data?
    
    * Can we predict the outcome of a traffic stop based on driver and/or officer characteristics?
        
        * More specifically: are any protected attributes like race or gender significant for predicting traffic stop outcomes? 
            
            * (This would imply potential discrimination in traffic policing.)
    
    * If so, what characteristics help predict the outcomes of traffic stops?
    
    * What does this say about the criminal justice system? 
    
    * What solutions can we offer to reconcile disproportionalities based on demographic characteristics like race, ethnicity, and gender? 
    
    Exploratory Data Analysis is made available to others via this Streamlit app, while the entire project and it's results may be found by visiting this project's **[Github.](https://github.com/SrikarVavilala/DSBA-6156-Group-3)**
    '''
    )
# Total traffic stops plot

import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime
from matplotlib.axis import Axis

if page == 'Drivers':
    selected_options =  st.sidebar.multiselect("Select one or more Driver's Race:",
             ["White", "Black", "Asian","Native American","Other/Unknown"],default=["Black"])
    
    colors = {'White': "#800000FF", 'Black': "#ADB17DFF", 'Asian': "#5B8FA8FF","Native American":"#725663FF","Other/Unknown":"#D49464FF"}
    outcomes = {'Arrest': "#AC8181", 'Citation Issued': "#CFCECA", 'No Action Taken': "#99ced3","Verbal Warning":"#C9A959","Written Warning":"#253D5B"}
    
    selected_year = st.sidebar.multiselect("Select one or both years of traffic stops:",['2020','2021'],default=['2020'])
    
    data = stops
    data['year'] = pd.DatetimeIndex(data['Month_of_Stop']).year
    data['year'] = data['year'].astype(str)
    data = data[data['year'].str.contains('|'.join(selected_year))]
    
    
    data = data.groupby(['Driver_Race','Month_of_Stop'], as_index=False)['Officer_Race'].count()
    data = data[data.stack().str.contains('|'.join(selected_options)).any(level=0)]
    
    locator = mdates.MonthLocator()
    date_form = DateFormatter("%b-%y")
    plot1 = sns.lineplot(data=data, x='Month_of_Stop', y='Officer_Race', hue='Driver_Race',palette=colors)
    plot1.set_xlabel("Month of Stop")
    plot1.set_ylabel("Count of Stops")
    plot1.set_title("Total Traffic Stops by CMPD")
    
    Axis.set_major_locator(plot1.xaxis,locator)
    plot1.xaxis.set_major_formatter(date_form)
    plot1.tick_params(axis='x', rotation=90)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
    #-----------------------------------
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    
    view = st.selectbox("Select a way to view the data:",['Counts','Percents'])
            
    data_2 = stops
    data_2['year'] = pd.DatetimeIndex(data_2['Month_of_Stop']).year
    data_2['year'] = data_2['year'].astype(str)
    data_2 = data_2[data_2['year'].str.contains('|'.join(selected_year))]
    data_2['Was_a_Search_Conducted'] = data_2['Was_a_Search_Conducted'].astype(str)
    data_2 = data_2[data_2['Driver_Race'].str.contains('|'.join(selected_options))]
    
    if view == 'Counts':
        plot2 = data_2.groupby(['Result_of_Stop', 
                                'Was_a_Search_Conducted']).size().reset_index().pivot(columns='Result_of_Stop', 
                                                                                    index='Was_a_Search_Conducted', values=0).plot(kind='bar', stacked=True,color=outcomes)
    else:
        plot2= pd.crosstab(data_2['Was_a_Search_Conducted'], data_2['Result_of_Stop']).apply(lambda r: r/r.sum()*100, axis=1)
        plot2 = plot2.plot.bar(figsize=(10,10), stacked=True, rot=0,color=outcomes)
        
    plot2.set_title("Result of Stop by 'Was a Search Conducted'")
    plot2.set_xlabel("Was a Search Conducted")
    plot2.set_ylabel('Count of Stops')
    plot2.set_xticklabels(['Yes','No'])
    plot2.tick_params(axis='x', rotation=0)
    st.pyplot()

    #----------------------------------------
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    
    data_3 = stops
    data_3 = data_3[data_3['Was_a_Search_Conducted']==1]
    data_3['year'] = pd.DatetimeIndex(data_3['Month_of_Stop']).year
    data_3['year'] = data_3['year'].astype(str)
    data_3 = data_3[data_3['year'].str.contains('|'.join(selected_year))]
    
    metric = st.selectbox("Select another variable to view the vehicle searches by:",['Driver Ethnicity','Driver Gender','Driver Age'])
    if metric == 'Driver Gender':
        plot3 = data_3.groupby(['Was_a_Search_Conducted', 
                                'Driver_Gender']).size().reset_index().pivot(columns='Was_a_Search_Conducted', 
                                                                                    index='Driver_Gender', values=0).plot(kind='bar', stacked=False)
        plot3.set_title("Vehicle Searches by Driver Gender")
        plot3.set_xlabel("Driver Gender")
        plot3.set_xticklabels(['Female','Male'])
        plot3.tick_params(axis='x', rotation=0)
        plot3.get_legend().remove()
        
    elif metric == 'Driver Ethnicity':
        plot3 = data_3.groupby(['Was_a_Search_Conducted', 
                                'Driver_Ethnicity']).size().reset_index().pivot(columns='Was_a_Search_Conducted', 
                                                                                    index='Driver_Ethnicity',values=0).plot(kind='bar', stacked=False)
        plot3.set_title("Vehicle Searches by Driver Ethnicity")
        plot3.set_xlabel("Driver Ethnicity")
        plot3.set_xticklabels(['Hispanic','Non-Hispanic'])
        plot3.tick_params(axis='x', rotation=0)
        plot3.get_legend().remove()

    elif metric == 'Driver Age':
        binwidth = st.selectbox("Select the size for Driver's Age binwidth:",list(range(1,11)),index=4)
        plot3 = sns.histplot(data_3['Driver_Age'],binwidth= binwidth)
        plot3.set_title("Vehicle Searches by Driver Age")
        plot3.set_xlabel("Driver Age")
        
    else:
        st.text("")
        
    plot3.set_ylabel("Count of Searches")
        
    st.pyplot()
     
if page == 'CMPD Divisions & Officers':
    
    colors = {'White': "#800000FF", 'Black': "#ADB17DFF", 'Asian': "#5B8FA8FF","Native American":"#725663FF","Other/Unknown":"#D49464FF"}
    
    all = st.sidebar.checkbox("Select all")
    if all:
        selected_options = st.sidebar.multiselect("Select one or more CMPD Division:",
             ["Metro","North Tryon","North","University City","Central","Freedom","Westover","Hickory Grove","Independence","Eastway","Steele Creek","Providence","South"],
                                                 ["Metro","North Tryon","North","University City","Central","Freedom","Westover","Hickory Grove","Independence","Eastway","Steele Creek","Providence","South"])
    else:
        selected_options =  st.sidebar.multiselect("Select one or more CMPD Division:",
            ["Metro","North Tryon","North","University City","Central","Freedom","Westover","Hickory Grove","Independence","Eastway","Steele Creek","Providence","South"],default=['Metro'])
        
    selected_year = st.sidebar.multiselect("Select one or both years of traffic stops:",['2020','2021'],default=['2020'])
    
    data = stops
    data['year'] = pd.DatetimeIndex(data['Month_of_Stop']).year
    data['year'] = data['year'].astype(str)
    data = data[data['year'].str.contains('|'.join(selected_year))]
    
    data = data[data['CMPD_Division'].str.contains('|'.join(selected_options))]
    data['CMPD_Division'] = data['CMPD_Division'].str.replace(' Division', '')
    
    
    
    catorder= ["Black","White","Asian","Native American","Other/Unknown"]
    div_order = ['Metro', 'North Tryon', 'North', 'University City', 'Central', 'Freedom', 'Westover','Hickory Grove',
                 'Independence','Eastway','Steele Creek','Providence','South']
    
    div_order2 = [i for i in div_order if any(i for j in selected_options if str(j) in i)]
    
    
    
    cross_tab_prop = pd.crosstab(index=data['CMPD_Division'], columns=data['Driver_Race'],normalize="index")
    cross_tab_prop.columns = pd.CategoricalIndex(cross_tab_prop.columns.values, 
                                 ordered=True, 
                                 categories=catorder)
    plot = cross_tab_prop.sort_index(axis=1).loc[div_order2].plot(kind='bar',stacked=True,color=colors)
    
    
    plot.tick_params(axis='x', rotation=90)
    plot.set_ylabel("Percentage of Stops")
    plot.set_xlabel("CMPD Division")
    plot.set_title("Percentage of Stops by Race within each CMPD Division")
    
    st.pyplot()

    #-------------------------------------------------------------
    
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    
    data2 = stops
    data2['year'] = pd.DatetimeIndex(data2['Month_of_Stop']).year
    data2['year'] = data2['year'].astype(str)
    data2 = data2[data2['year'].str.contains('|'.join(selected_year))]
    data2 = data2[data2['Was_a_Search_Conducted']==1]
    data2 = data2[data2['CMPD_Division'].str.contains('|'.join(selected_options))]
    data2['Officer_Years_of_Service'] = round(data2['Officer_Years_of_Service']/4) + (data2['Officer_Years_of_Service'] % 4 > 0)
    
    #code line plot here
    view = st.selectbox("Select a way to view the data:",['Counts','Percents'])
    
    if view == 'Counts':
        catorder= ["Black","White","Asian","Native American","Other/Unknown"]
        plot2= pd.crosstab(index=data2['Officer_Years_of_Service'], columns=data2['Driver_Race'])
        plot2.columns = pd.CategoricalIndex(plot2.columns.values, 
                                 ordered=True, 
                                 categories=catorder)
        plot2 = plot2.sort_index(axis=1).plot.bar(stacked=True, color=colors)
        plot2.set_ylabel("Count of Searches")
        
    else:
        catorder= ["Black","White","Asian","Native American","Other/Unknown"]
        plot2= pd.crosstab(index=data2['Officer_Years_of_Service'], columns=data2['Driver_Race'],normalize="index")
        plot2.columns = pd.CategoricalIndex(plot2.columns.values, 
                                 ordered=True, 
                                 categories=catorder)
        plot2 = plot2.sort_index(axis=1).plot.bar(figsize=(10,10),stacked=True, rot=0,color=colors)
        plot2.set_ylabel("Percent of Searches")
        
    plot2.set_xticklabels(['1-4','5-8','9-12','13-16','17-20','21-24','25-28','29-32','33-36'])
    plot2.tick_params(axis='x', rotation=0)
    plot2.set_xlabel("Officer Years of Service")
    plot2.set_title("Cumulative Vehicle Searches by Race for each grouping of Officer Years of Service")
    
    st.pyplot()
