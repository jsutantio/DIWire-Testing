# On the Right Course
# Aditi Joshi and Jessica Sutantio
# Software Design Final Project


""" From all of the Olin registaration data, we will be creating a visualization 
displaying the most commong courses taken during a student's Olin career. 
Users will be able to filter the data so that they may visualize the informaiton 
based on major and/ or semester.
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Name of data file
file_name = 'CourseEnrollmentsFA02-SP15.csv'

def get_df(file_name):
    """
    file_name: csv file that contains the course data
    separates the data from the file into its columns, each column is a list
    returns: df-data frame that holds all the organized data from file_name
    """

    # labelling of data lists
    ID = []
    academicYear = []
    academicStatus = []
    major = []
    courseNum = []
    courseSect = []
    courseTitle = []
    professor = []

    # opens csv file and sorts the data into the lists
    with open(file_name, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for courseData in data:
            ID.append(courseData[0])
            academicYear.append(courseData[1])
            academicStatus.append(courseData[2])
            major.append(courseData[3] + courseData[4]) # includes concentration
            courseNum.append(courseData[5]) # seems to output a ton of spaces after #
            courseSect.append(courseData[6])
            courseTitle.append(courseData[7].strip() + ' ' + courseData[8].strip()) # includes subtitle
            professor.append(courseData[9])

    # semester = course_time(academicStatus,academicYear)

    df = pd.DataFrame({'ID': ID, 'academicYear': academicYear, 'academicStatus': academicStatus, 'major': major, 'courseNum': courseNum, 'courseSect': courseSect, 'courseTitle': courseTitle, 'professor': professor})

    return df

class CourseDF(object):
    """ 
    class creates the dataframe that contains the cleaning and 
    filtering functions
    """

    def __init__(self, df):
        self.df = df

    def semLabel(self):
        """
        takes the df and goes row by row to determine the semester the
        course was registered for
        returns: df that has the semesters labeled from 1-4.5
        """
       
        # relabeling semester row by row
        for i in range(len(self.df.index)):
            status = self.df.loc[i,'academicStatus']
            year = self.df.loc[i,'academicYear']
            if (status=='TF') or (status=='FF'):
                sem = 1.0
                # print sem
            elif status=='FR':
                sem = 1.5
            elif status=='SO' and ('FA' in year):
                sem = 2.0
            elif status=='SO' and ('SP' in year):
                sem = 2.5
            elif status=='JR' and ('FA' in year):
                sem = 3.0
            elif status=='JR' and ('SP' in year):
                sem = 3.5
            elif status=='SR' and ('FA' in year):
                sem = 4.0
            elif status=='SR' and ('SP' in year):
                sem = 4.5
            else:
                sem = np.nan

            # overwrite the academicStatus to use our numbering convention (1-4.5)
            self.df.loc[i,'academicStatus'] = sem

        return self.df

    def majorAssignment(self):
        """
        this method takes in each student's ID and their major. If their major is 
        undefined at any point, the function will take in the first major it finds
        for that ID 
        MAJORS SYNTAX
         ['Undeclared              ' 
         'Mechanical Engineering  '
         'Engineering             '
         'Undeclared              Systems                 '
         'Engineering             Systems                 '
         'Undeclared              Computing               '
         'Engineering             Computing               '
         'Undeclared              Materials Science       '
         'Mechanical Engineering  Materials Science       '
         'Engineering             Materials Science       '
         'Mechanical Engineering  Computing               '
         'Undeclared              Bioengineering          '
         'Engineering             Bioengineering          '
         "Electr'l & Computer Engr"
         'Undeclared              Self Designed           '
         'Engineering             Self Designed           '
         'Mechanical Engineering  Bioengineering          '
         "Electr'l & Computer EngrComputing               "
         "Electr'l & Computer EngrSystems                 "
         'Mechanical Engineering  Systems                 '
         'Mechanical Engineering  Self Designed           '
         "Electr'l & Computer EngrSelf Designed           "
         'Undeclared              Design                  '
         'Mechanical Engineering  Design                  '
         'Engineering             Design                  '
         'Undeclared              Robotics                '
         'Mechanical Engineering  Robotics                '
         'Engineering             Robotics                '
         'Exchange Student        Computing               '
         "Electr'l & Computer EngrRobotics                "]
        """

        # # all majors that they can list from: ME, ECE, E:C, E:Robo, E:Bio, E:MatSci, E:Design, E:Systems
        # major_convert = {'ME': 'Mechanical Engineering  ', 'ECE': "Electr'l & Computer Engr", 'E:C': 'Engineering             Computing               ', 'E:Robo': 'Engineering             Robotics                ', 'E:Bio': 'Engineering             Bioengineering          ', 'E:MatSci': 'Engineering             Materials Science       ', 'E:Design': 'Engineering             Design                  ', 'E:Systems': 'Engineering             Systems                 '}
        # major = major_convert[self.df.col.major]

        # finds all the unique ids of all ids
        uniqueIDs = self.df.ID.unique()
        uniquemajors = self.df.major.unique()

        # find the start and end indices of the unique IDs 
        for idNum in uniqueIDs:
            IDindex = self.df[self.df['ID']==idNum].index.tolist()
            startID = IDindex[0]
            endID = IDindex[-1]
            # find the last updated major of the student
            latestMajor = self.df['major'][endID]
            # change all previous majors to be the same as last updated major
            self.df.loc[startID:endID+1, 'major'] = latestMajor

        return self.df

    def OSS(self):
        """
        assigns all OSS's (courseNum: ) to have "Olin Self Study" as courseTitle
        """

        for i in range(len(self.df.index)):
            courseNumber = self.df.loc[i,'courseNum']
            title = self.df.loc[i,'courseTitle']
            
            if 'ENGR4198' in courseNumber:
                title = 'Olin Self Study in Engineering'
            elif 'AHSE4198' in courseNumber:
                title = 'Olin Self Study in Arts, Humanities, Social Sciences'
            elif 'AHSE4598' in courseNumber:
                title = 'Olin Self Study in Business and Entrepreneurship'
            elif 'SCI4198' in courseNumber:
                title = 'Olin Self Study in Science'
            elif 'MTH4198' in courseNumber:
                title = 'Olin Self Study in Mathematics'
            elif 'ISR4198' in courseNumber:
                title = 'Olin Self Study'
            elif 'ENGR0098' in courseNumber:
                title = 'Independent Study in Engineering'
            elif 'AHSE0098' in courseNumber:
                title = 'Independent Study in Arts, Humanities, Social Sciences'
            elif 'SCI0098' in courseNumber:
                title = 'Independent Study in Science'
            elif 'MTH0098' in courseNumber:
                title = 'Independent Study in Mathematics'

        return self.df

    def oldCourses(self):
        """ Get rid of courses that are no longer offered from the df by
        looking at courses that are only offered in the last 4 years
        """
        # find all the unique courses
        uniqueCourse = self.df.courseNum.unique()
        new_df = pd.DataFrame()

        for course in uniqueCourse:
            courseindex = self.df[self.df['courseNum']==course].index.tolist()
            if '14' not in self.df['academicYear'][courseindex[-1]] and '12' not in self.df['academicYear'][courseindex[-1]]:
                new_df = new_df.append(self.df.loc[courseindex])
                # print len(self.df)
                # new_df = self.df.drop(self.df.index[[courseindex]])

        pd.options.mode.chained_assignment = None 
        self.df = self.df[self.df.index.map(lambda x: x not in new_df.index)]
        self.df = self.df.reset_index()
        return self.df


    def AHScount(self):
        """
        count the number of AHS classes taken in a sem by a student
        """
        # finds all the unique ids of all ids
        uniqueIDs = self.df.ID.unique()
        semesters = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
        
        # loop through the unique ids 
        for idNum in uniqueIDs:
            # set the count of that person's AHS classes to 0
            count = 0
            # find start and end indeces for that id
            IDindex = self.df[self.df['ID']==idNum].index.tolist()
            startID = IDindex[0]
            endID = IDindex[-1]
            for i, row in enumerate(self.df.loc[startID:endID].iterrows()):
                if 'AHSE' in row[1][3] and idNum == row[1][0]:
                    self.df['courseNum'][row[0]] = 'AHSE' + str(count)
                    self.df['courseTitle'][row[0]] = 'AHSE class' + str(count)
                    count += 1

        return self.df



    def courseNames(self):
        """
        make courses of the same courseNum have the first courseTitle assciated
        with it
        """

        # start dictionary that pairs courseNum with courseTitle
        NumTitlePair = {}
        # find all the unique courseNums and put
        uniqueCourseNum = self.df.courseNum.unique()
        
        # run thru df backwards and assign the latest courseTitle to the courseNum
        for i in reversed(range(len(self.df.index))):
            year = self.df.loc[i,'academicYear']
            if ('MTH2188' in self.df.courseNum[i]) and ('FA' in year):
                self.df.courseTitle[i] = 'Linearity II'
            elif ('MTH2188' in self.df.courseNum[i]) and ('SP' in year):
                self.df.courseTitle[i] = 'Linearity I'
            elif self.df.courseNum[i] in NumTitlePair:
                self.df.courseTitle[i] = NumTitlePair[self.df.courseNum[i]]
            else:
                NumTitlePair[self.df.courseNum[i]] = self.df.courseTitle[i]

        return self.df

    def dataCleaning(self):
        self.semLabel()
        self.majorAssignment()
        self.OSS()
        self.AHScount()
        self.oldCourses()
        self.courseNames()

        return self.df

class FilterDF(object):
    """
    end goal is to get the appropriate df from the queried order of filtering
    """

    def __init__(self, df, sem=None, major=None):
        self.df = df
        self.sem = sem
        self.major = major

    def capped_percent(self, df):
        """
        NEED TO MAKE SURE THE VALUES OUTPUT IN FULL DF: INCLUDES THE COURSE TITLE
        takes in the semester filtered df and outputs the top ten percentages in a df
        """

        # counts the number of students registered in specified semester
        # type: integer
        numStudents = df.ID.nunique()
        # count the number of people (all gradYears) registered for a course
        # type: series (index is courseNum; value is number of students)
        courseFreq = df.groupby('courseTitle').ID.nunique()
        # print 'courseFreq',str(courseFreq),str(type(courseFreq))
        # calcs the % by dividing the number of registered students per course by total number of students
        # type: series
        percentages = (courseFreq/numStudents)*100
        # sort the Series by highest to lowest percentage
        # type: series
        percentages.sort(ascending=False)
        # limit the list of courses to the top 10
        # type: series
        capped_percentages = percentages.head(10)
        # list of courses
        # type: list
        courses = capped_percentages.index.values.tolist()
        # list of percentages
        # type: list
        list_percent = capped_percentages.tolist()
        # combine them back into a dataframe
        # type: df
        capped_percents = pd.DataFrame({'courseTitle': courses, 'Percent': list_percent})

        return capped_percents

    def semFilter(self, df):
        """
        Filters the data by a specified semester and outputs a df that 
        contains data for only that semester
        returns modified df that only contains info for that specified 
        semester
        """
        semDF = df[df['academicStatus'] == self.sem]

        return semDF

    def majorFilter(self, df):
        """
        Filters the data by a specified major and outputs a df that 
        contains data for only that major
        returns modified df that only contains info for that specified 
        semester
        """
        majorDF = df[df['major'] == self.major]

        return majorDF

    def output8Sem(self):
        """
        For scenarios (no filter or only majorFilter) in which all 8 sem are displayed,
        run through semFilter and capped_percent for each sem
        return all 8 sem in 8 separate dfs compiled into a list
        """
        
        semList = [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5]
        dfList = []

        for element in semList:
            self.sem = element
            dfList.append(self.semFilter(self.df))

        return dfList

    def filter(self):
        # filtered by sem and major at the same time
        if self.sem != None and self.major != None:
            return self.capped_percent(self.majorFilter(self.semFilter(self.df)))
        # filtered by semester only
        elif self.sem != None:
            return self.capped_percent(self.semFilter(self.df))
        # filtered by major only
        elif self.major != None:
            eightDFs = self.output8Sem()
            filteredEightDFs = []
            # go thru the list of dfs and filter major
            for element in eightDFs:      
                filteredEightDFs.append(self.capped_percent(self.majorFilter(element)))
            return filteredEightDFs
        # no filter
        else:
            eightDFs = self.output8Sem()
            filteredEightDFs = []
            for element in eightDFs:
                filteredEightDFs.append(self.capped_percent(element))
            return filteredEightDFs

class RenderDF(object):

    def __init__(self, filtered):
        self.filterOutput = filtered
        self.df = filtered
    
    def addPercentSymbol(self,percentList):
        """
        takes a list of the percentages and returns a list of the rounded #s with
        the percent symbol
        """

        list_percent = percentList
        list_percentages = []
        for element in list_percent:
            list_percentages.append(str(int(element))+'%')

        return list_percentages

    def plot(self,label):
        """
        set up the plot settings with matplotlib
        """

        # Data lists for plotting        
        courseTitle = self.df['courseTitle'].tolist()
        y_position = np.arange(len(courseTitle))
        y_pos = y_position[::-1]
        percentages = self.df['Percent'].tolist()
        prettyPercentages = self.addPercentSymbol(percentages)

        ### Set up the figure
        fig, ax1 = plt.subplots(figsize=(20,15), facecolor='white')
        # No visible borders
        ax1.spines['left'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        # Pushes the left labels away from bars
        ax1.spines['left'].set_position(('outward', .4))
        # Set the color scheme
        colors=['#D0DD2B','#98C73D', '#00A9E0', '#67CDDC', '#3B3B3D']

        # Plot the horizontal bars
        rects = plt.barh(y_pos, percentages, align='center', color=colors,
                         edgecolor='none')

        # Add the appropriate labeling of data points
        plt.xticks([])
        plt.yticks(y_pos,prettyPercentages, color='#3B3B3D', size='x-large')
        plt.tick_params(right="off")
        plt.tick_params(left="off")

        # Write in the courseTitle inside each bar
        for i,rect in enumerate(rects):
            barWidth = rect.get_width()
            # print 'width', barWidth
            # print courseTitle[i], len(courseTitle[i])

            # If bars aren't wide enough to print the title inside
            if barWidth < (len(courseTitle[i]) + 0.2*barWidth):
                # Shift the text to the right side of the right edge
                xloc = barWidth + .3
                clr = '#3B3B3D'
                align = 'left'
            else:
                # Shift the text to the left side of the right edge
                xloc = barWidth-.3
                clr = 'white'
                align = 'right'

            # Center the text vertically in the bar
            yloc = rect.get_y()+rect.get_height()/2.0
            ax1.text(xloc, yloc, courseTitle[i], horizontalalignment=align,
                     verticalalignment='center', color=clr, size='x-large')

        # Save plot to file
        plot_name = "plot{}.png".format(label)
        plt.savefig(plot_name,bbox_inches='tight', transparent=True,
                    edgecolor='none')

        plt.show()

    def render(self, semInput, majorInput):
        """
        Takes the input df (whether it's a list of 8 or not) saves the appropriate
        number of figures through the plot function
        """
        
        # Format file labelling
        if majorInput is None:
            majorInput = ''
        if semInput is None:
            semInput = ''

        encodeSem = [1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5]
        # For scenarios with 8 sem
        if isinstance(self.filterOutput, list):
        # if type(self.filterOutput)== <type 'list'>:
            for i in range(8):
                label = str(encodeSem[i])+'_'+majorInput
                self.df = self.filterOutput[i] 
                self.plot(label)
        else:
            label = str(semInput)+'_'+majorInput
            self.plot(label)

if __name__ == '__main__':
    
    # FILTER HERE    
    semInput= None
    majorInput = 'Mechanical Engineering  '

    data = CourseDF(get_df(file_name))
    cleanDF = data.dataCleaning()    
    testFilter = FilterDF(cleanDF, sem=semInput, major=majorInput)
    # print testFilter.filter()

    plotThis = testFilter.filter()
    final = RenderDF(plotThis)
    final.render(semInput,majorInput)