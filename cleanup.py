import pandas as pd
import numpy as np
import os
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = "rawData.csv"
def cleanup_data(df):
    courseDesignationList = df['Course Designation'].tolist()

    levelList = []
    breadthList = []
    gradList = []
    lsList = []
    ethnicList = []
    honorsList = []
    genEdList = []
    workList = []
    foreignLangList = []
    lastTaughtList = []

    counter = 0
    for course in courseDesignationList:
        if isinstance(course, str):
            if 'Level - Advanced' in course:
                levelList.append('3')
            elif 'Level - Intermediate' in course:
                levelList.append('2')
            elif 'Level - Elementary' in course:
                levelList.append('1')
            else:
                levelList.append('0')


            if 'Breadth - Literature' in course:
                breadthList.append('Literature')
            elif 'Breadth - Humanities' in course:
                breadthList.append('Humanities')
            elif 'Breadth - Social Science' in course:
                breadthList.append('Social Science')
            elif 'Breadth - Biological Sci.' in course:
                breadthList.append('Biological Science')
            elif 'Breadth - Physical Sci.' in course:
                breadthList.append('Physical Science')
            elif 'Breadth - Natural Science' in course:
                breadthList.append('Natural Science')
            elif 'Breadth - Either Humanities or Social Science' in course:
                breadthList.append('Humanities/Social Science')
            elif 'Breadth - Either Biological Science or Social Science' in course:
                breadthList.append('Biological Science/Social Science')
            elif 'Breadth - Either Social Science or Natural Science' in course:
                breadthList.append('Social Science/Natural Science')
            elif 'Breadth - Either Humanities or Natural Science' in course:
                breadthList.append('Humanities/Natural Science')
            else:
                breadthList.append('N/A')


            if 'Grad 50% - Counts toward 50% graduate coursework requirement' in course:
                gradList.append('1')
            else:
                gradList.append('0')

            if 'L&S Credit - Counts as Liberal Arts and Science credit in L&S' in course:
                lsList.append('1')
            else:
                lsList.append('0')

            if 'Ethnic St - Counts toward Ethnic Studies requirement' in course:
                ethnicList.append('1')
            else:
                ethnicList.append('0')

            if 'Honors - Honors Only Courses (H)' in course:
                honorsList.append('1') # Honors Only
            elif 'Honors - Accelerated Honors (!)' in course:
                honorsList.append('2') # Accelerated Honors
            elif 'Honors - Honors Optional (%)' in course:
                honorsList.append('3') # Honors Optional
            else:
                honorsList.append('0')

            if 'Gen Ed - Communication Part A' in course:
                genEdList.append('1')
            elif 'Gen Ed - Communication Part B' in course:
                genEdList.append('2')
            elif 'Gen Ed - Quantitative Reasoning Part A' in course:
                genEdList.append('3')
            elif 'Gen Ed - Quantitative Reasoning Part B' in course:
                genEdList.append('4')
            else:
                genEdList.append('0')

            if 'Workplace - Workplace Experience Course' in course:
                workList.append('1')
            else:
                workList.append('0')

            if 'Frgn Lang - 1st semester language course' in course:
                foreignLangList.append('1')
            elif 'Frgn Lang - 2nd semester language course' in course:
                foreignLangList.append('2')
            elif 'Frgn Lang - 3rd semester language course' in course:
                foreignLangList.append('3')
            elif 'Frgn Lang - 4th semester language course' in course:
                foreignLangList.append('4')
            elif 'Frgn Lang - 5th + semester language course' in course:
                foreignLangList.append('5')
            else:
                foreignLangList.append('0')
        else:
            levelList.append('0')
            breadthList.append('0')
            gradList.append('0')
            lsList.append('0')
            ethnicList.append('0')
            honorsList.append('0')
            genEdList.append('0')
            workList.append('0')
            foreignLangList.append('0')
        counter += 1

    df['Repeatable'] = df['Repeatable'].str.replace('Yes, unlimited number of completions', '1')
    df['Repeatable'] = df['Repeatable'].str.replace('Yes, for 2 number of completions', '2')
    df['Repeatable'] = df['Repeatable'].str.replace('Yes, for 3 number of completions', '3')
    df['Repeatable'] = df['Repeatable'].str.replace('Yes, for 4 number of completions', '4')
    df['Repeatable'] = df['Repeatable'].str.replace('Yes, for 5 number of completions', '5')
    df['Repeatable'] = df['Repeatable'].str.replace('Yes, for 6 number of completions', '6')
    df['Repeatable'] = df['Repeatable'].str.replace('No', '0')

    lastTaughtList = df['Last Taught'].tolist()
    for i in range(len(lastTaughtList)):
        words = lastTaughtList[i].split(' ')
        if words[0] == 'Fall':
            lastTaughtList[i] = words[1] + '-' + '09-01'
        elif words[0] == 'Spring':
            lastTaughtList[i] = words[1] + '-' + '01-01'
        elif words[0] == 'Summer':
            lastTaughtList[i] = words[1] + '-' + '06-01'

    df['Course Level'] = levelList
    df['Course Breadth'] = breadthList
    df['Grad Req'] = gradList
    df['L&S Credit'] = lsList
    df['Ethnic Studies'] = ethnicList
    df['Honors'] = honorsList
    df['Gen Ed'] = genEdList
    df['Workplace'] = workList
    df['Foreign Language'] = foreignLangList
    df['Last Taught'] = lastTaughtList

    df['Course Designation'] = df['Course Designation'].str.replace('Level - Advanced', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Level - Intermediate', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Level - Elementary', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Literature. Counts toward the Humanities req', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Humanities', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Social Science', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Biological Sci. Counts toward the Natural Sci req', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Physical Sci. Counts toward the Natural Sci req', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Either Humanities or Social Science', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Either Biological Science or Social Science', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Either Social Science or Natural Science', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Either Humanities or Natural Science', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Breadth - Natural Science', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Grad 50% - Counts toward 50% graduate coursework requirement', '')

    df['Course Designation'] = df['Course Designation'].str.replace('L&S Credit - Counts as Liberal Arts and Science credit in L&S', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Ethnic St - Counts toward Ethnic Studies requirement', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Honors - Honors Only Courses (H)', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Honors - Accelerated Honors (!)', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Honors - Honors Optional (%)', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Gen Ed - Communication Part A', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Gen Ed - Communication Part B', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Gen Ed - Quantitative Reasoning Part A', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Gen Ed - Quantitative Reasoning Part B', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Workplace - Workplace Experience Course', '')

    df['Course Designation'] = df['Course Designation'].str.replace('Frgn Lang - 1st semester language course', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Frgn Lang - 2nd semester language course', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Frgn Lang - 3rd semester language course', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Frgn Lang - 4th semester language course', '')
    df['Course Designation'] = df['Course Designation'].str.replace('Frgn Lang - 5th + semester language course', '')

    # delete course designation column
    del df['Course Designation']

    df['Requisites'].fillna('No prerequisites.', inplace=True)
    return df





