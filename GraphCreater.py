#Graphs appear one at a time, click x to go to the next
#Import relevant libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import natsort



def get_data(x_to_find, column_in_sheet):
    '''
    x_to_find is a string of a specific response such as undergraduate students
    column_in_sheet is a Pandas series object representing the column in the csv
    '''
    limit_rows = df[column_in_sheet == x_to_find]
    return limit_rows
    

    
def convert_agree_to_num(data_series):
    '''
    Given a pandas data series of agree responses, creates a sum changing agree to numerical values
    '''
    sum = 0
    for i in data_series:
        if i == 'Strongly Agree':
            sum +=5
        elif i == 'Agree':
            sum +=4
        elif i == 'Neutral':
            sum +=3
        elif i == 'Disagree':
            sum +=2
        elif i == 'Strongly Disagree':
            sum +=1
    return sum
def convert_often_to_num(data_series):
    '''
    Given a Pandas Data series, change all frequent values to a numeric value to sum
    '''
    sum = 0
    for i in data_series:
        if 'Often' in i:
            sum += 3
        if 'Sometimes' in i:
            sum +=2
        if 'Rarely' in i:
            sum+=1
    
    return sum
        
def get_data_for_all(column1, num_of_column2, uses_agree, uses_often_values = False):
    '''
    Column1 is an Pandas Series object, Column2 is an int
    Retrieves data needed for x and y axis
    '''
    list_of_x = []
    list_of_y = []
    #Gets the average value for each item in column1
    for i in natsort.natsorted(set(column1.values.tolist())):
        total = 0;
        series = get_data(i,column1)
        values = get_method_from_num(num_of_column2, series)
        #print(values)
        
        #Convert to a numeric sum
        if (uses_agree):
            total = convert_agree_to_num(values)
        elif (uses_often_values):
            total = convert_often_to_num(values)
        else:
            total = sum(values)
        #Calculate average
        list_of_y.append(total / len(series))
        list_of_x.append(i)
    return (list_of_x, list_of_y)

def get_method_from_num(num_of_column, series_to_act_on):
    '''
    Given a number from the column indexed 0, return that column of data from a series
    '''
    return series_to_act_on[df.columns[num_of_column]]
   





if __name__ == "__main__":
    #Read in the google spread sheet (downloaded inside the folder)
    df = pd.read_csv("ChatGPT Survey.csv")
    
    #Plot gpa vs how much they think ChatGPT is plagiarism
    gpa_vs_plag = get_data_for_all(df.gpa,12,True) 
    print(gpa_vs_plag)
    plt.bar(gpa_vs_plag[0], gpa_vs_plag[1], zorder = 3)
    plt.grid(axis='y',zorder = 1)
    plt.xlabel("GPA")
    plt.ylabel("ChatGPT is Plagiarism (1 - Strongly Disagree, 5 - Strongly Agree)")
    plt.title("GPA vs thoughts on whether ChatGPT is plagiarism")
    plt.show()

    #Plot hours studied againts productivity
    hours_studied_vs_productivity_increase = get_data_for_all(df.study_hours,10,False)
    plt.bar(hours_studied_vs_productivity_increase[0],hours_studied_vs_productivity_increase[1], zorder = 3, width=0.5)
    plt.xlabel("Hours Studied in a week")
    plt.ylabel("Increase in productivity from ChatGPT")
    plt.ylim(2.5,3.5)
    plt.grid(axis= 'y', zorder = 0)
    plt.title("How Producitivty Increases Based on How Long an Individual Studies")
    plt.show()
    
    #Plot education level vs thoughts on plagiarism
    education_level_vs_plag = get_data_for_all(df.education, 12, True)
    plt.barh(education_level_vs_plag[0],education_level_vs_plag[1], zorder = 3, height= 0.5)
    plt.grid(axis='x', zorder = 1)
    plt.ylabel("Level of Education")
    plt.xlabel("ChatGPT is Plagiarism (1 - Strongly Disagree, 5 - Strongly Agree)")
    plt.title("Thoughts on ChatGPT as Plagiarism by Different Education Levels")
    plt.show()
    
    #Pie chart with extra style
    good_colours = ['#5adf00', '#fc4c27', '#ddea32']
    explosion = (0.05,0.05,0.05)
    options_for_affects = ('Yes', 'No', 'Maybe')

    #Get the number of responses for each of the options
    num_of_yes = len(df[df.affects_on_thinking == options_for_affects[0]])
    num_of_no = len(df[df.affects_on_thinking == options_for_affects[1]])
    num_of_maybe = len(df[df.affects_on_thinking == options_for_affects[2]])

    plt.pie([num_of_yes,num_of_no,num_of_maybe], autopct='%1.1f%%', colors = good_colours, shadow=True, explode=explosion)
    plt.legend(options_for_affects)
    plt.title("Number of Students Who Believe ChatGPT Will Disincentivize an Individual's Critical Thinking Ability")
    plt.show()
    
    
    