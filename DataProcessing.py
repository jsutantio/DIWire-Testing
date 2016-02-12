# DIWIRE TESTING DATA PROCESSING
# Jessica Sutantio
# February 2nd, 2016


"""
From all of the Olin registaration data, we will be creating a visualization 
displaying the most commong courses taken during a student's Olin career. 
Users will be able to filter the data so that they may visualize the informaiton 
based on major and/ or semester.
"""

import csv
import datetime
import time
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# Name of data file
file_name = 'log_20160127_163227.txt'

def get_tempLogs(tempLog):
    """
    tempLog: csv file that contains the temperature data for the various machines
    Goes through the folder directory and extracts all the tempLogs and sorts them by date, time, and machine
    returns : --------------
    """

def get_iterationLogs(iterationLog):
    """
    iterationLog: csv file that contains the DIWire cycle data
    Goes through the folder directory and extracts all the tempLogs and sorts them by date, time, and machine
    returns : --------------
    """

def processMachineLog(file_name):
    """
    takes in a machine log and returns lists of processed data
    """

    # labelling of data lists
    date = []
    timeDay = []
    iteration = []
    iterationTime = []      # time it takes to complete a single cycle
    timeElapsed = []       # time elapsed since start of test for the day
    
    """ sample of important lines from log
    ##### Begin Iteration # 1  at Wed Jan 27 16:32:27 EST 2016
    ##### Completed Iteration # 1  time: 13.643001secs  Total time: 13.648001secs  at Wed Jan 27 16:32:41 EST 2016
    """

    # opens csv file and sorts the data into the lists
    # with open(file_name, 'rb') as csvfile:
    with open(file_name, 'rb') as logFile:
        data = logFile.readlines()
        for line in data:
            if line.startswith("##### Completed"):
                iteration.append(line.split(" ")[4])
                iterationTime.append(line.split(" ")[7][:-4]) # remove "secs" from the value
                # Get the Day of week, month, and date to put into date list
                dayMoDate = line.split(" ")[14] + " " + line.split(" ")[15] + " " + line.split(" ")[16] + " " + line.split(" ")[19].rstrip()
                date.append(dayMoDate)
                # get the time in AM/PM format (because Jess can't read 24HR format to save her life)
                convertTime = time.strftime("%I:%M:%S %p", (time.strptime(line.split(" ")[17] , "%H:%M:%S")))
                timeDay.append(convertTime)
                # get the total time (H:M:S format) that has elapsed since the beginning of the test
                timeSecs = float(line.split(" ")[11][:-4]) # remove "secs" from the value
                timeElapsed.append(datetime.timedelta(seconds=timeSecs))
    
    # form the dataframe with all the lists as columns
    df = pd.DataFrame({'Date': date, 'Time': timeDay, 'Cycle': iteration, 'Cycle Duration': iterationTime, 'Time Elapsed': timeElapsed})
    return df


def processTempLog(file_name):
    """
    takes in a temp log and returns lists of processed temp data with time
    """

def get_df(file_name):
    """
    file_name: --------------
    separates the data from the file into its columns, each column is a list
    returns: df-data frame that holds all the organized data from file_name
    """

    # labelling of data lists
    # date = []
    # timeDay = []
    # iteration = []
    totalCycles = []        # total number of cycles from all days of cycle testing
    # iterationTime = []      # time it takes to complete a single cycle
    # timeElapsed = []       # time elapsed since start of test for the day
    totalRunningTime = []     # total running time from all days of cycle testing
    tempX32 = []
    tempY32 = []
    tempZ32 = []
    tempX8 = []
    tempY8 = []
    tempZ8 = []

    return processMachineLog(file_name)
    


    # with open(file_name, 'rb') as csvfile:
    #     data = csv.reader(csvfile, delimiter=',')
    #     for courseData in data:
    #         tempY32.append(courseData[0])
    #         tempZ32.append(courseData[1])
    #         tempX32.append(courseData[2])
    #         tempY8.append(courseData[3])
    #         tempZ8.append(courseData[4])
    #         tempX8.append(courseData[5])

    # form the dataframe with all the lists as columns
    # df8 = pd.DataFrame({'Date': date, 'Time': timeDay, 'Cycle': iteration, 'Cycle Duration': iterationTime, 'Time Elapsed': timeElapsed, 'Temp X': tempX8, 'Temp Y': tempY8, 'Temp Z': tempZ8})
    # df32 = pd.DataFrame({'Date': date, 'Time': timeDay, 'Cycle': iteration, 'Cycle Duration': iterationTime, 'Time Elapsed': timeElapsed, 'Temp X': tempX32, 'Temp Y': tempY32, 'Temp Z': tempZ32})

    # return df



if __name__ == '__main__':
    
    print get_df(file_name)
