from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import cleanup

COURSES_URL = "https://guide.wisc.edu/courses/"
df = pd.DataFrame()
courseBlockList = []
courseNamesList = []
courseDescList = []
courseCreditsList = []
requisitesList = []
repeatableList = []
lastTaughtList = []
courseDesignationList = []


def get_sites():

        urls = []

        r = requests.get(COURSES_URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        majors = soup.find('div', id='atozindex')
        majorLinks = majors.find_all('a')
        for link in majorLinks:
                url = "https://guide.wisc.edu" + link.get('href')
                urls.append(url)
        return urls



def dataset_maker(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        courses = soup.find('div', class_='page_content')

        courseBlocks = courses.find_all('span', class_='courseblockcode')
        for course in courseBlocks:
                courseToAdd = course.text.replace('\xa0', ' ')
                courseToAdd = courseToAdd.replace('\u200b', '')
                courseToAdd = courseToAdd.replace('  ', ' ')
                courseBlockList.append(courseToAdd)


        courseDescs = soup.find_all('p', class_='courseblockdesc')
        for desc in courseDescs:
                descToAdd = desc.text.replace('\xa0', ' ')
                descToAdd = descToAdd.replace('\u200b', '')
                descToAdd = descToAdd.replace('  ', ' ')
                descToAdd = descToAdd.replace('\n', '')
                courseDescList.append(descToAdd)

        courseCredits = soup.find_all('p', class_='courseblockcredits')
        for credit in courseCredits:
                creditToAdd = credit.text.replace('\xa0', ' ')
                creditToAdd = creditToAdd.replace('\u200b', '')
                creditToAdd = creditToAdd.replace('  ', ' ')
                creditToAdd = creditToAdd.replace('\n', '')
                creditToAdd = creditToAdd.replace(' credits.', '')
                creditToAdd = creditToAdd.replace(' credit.', '')
                courseCreditsList.append(creditToAdd)
        courseNames = soup.find_all('p', class_='courseblocktitle')

        for courseName in courseNames:
                courseNameToAdd = courseName.find('strong').text
                courseNameToAdd = str(courseNameToAdd)
                courseNameToAdd = courseNameToAdd.strip()
                index = courseNameToAdd.find('—')
                courseNameToAdd = courseNameToAdd[index + 1:]
                courseNameToAdd = courseNameToAdd.strip()

                courseNamesList.append(courseNameToAdd)
        extras = soup.find_all('div', class_='cb-extras')

        isRepeatable = False

        isLastTaught = False

        isRequisites = True

        isCourseDesignation = False
        for extra in extras:
                extraText = extra.text
                courseDesIndex = extraText.find('Course Designation:')
                if courseDesIndex != -1:
                        extraText = extraText[:courseDesIndex] + "\n" + extraText[courseDesIndex:]
                        isCourseDesignation = True
                repeatableIndex = extraText.find('Repeatable for Credit:')
                if repeatableIndex != -1:
                        extraText = extraText[:repeatableIndex] + "\n" + extraText[repeatableIndex:]
                        isRepeatable = True
                lastTaughtIndex = extraText.find('Last Taught:')
                if lastTaughtIndex != -1:
                        extraText = extraText[:lastTaughtIndex] + "\n" + extraText[lastTaughtIndex:]
                        isLastTaught = True
                #####################################################################################
                extraList = extraText.split('\n')
                if isCourseDesignation is True:
                        for ex in extraList:
                                if ex.find('Course Designation:') != -1:
                                        courseDesignationList.append(ex.replace('Course Designation: ', '').strip())
                                        isCourseDesignation = False
                elif isCourseDesignation is False:
                        courseDesignationList.append('N/A')
                if isRepeatable is True:
                        for ex in extraList:
                                if ex.find('Repeatable for Credit:') != -1:
                                        repeatableList.append(ex.replace('Repeatable for Credit: ', '').strip())
                                        isRepeatable = False
                elif isRepeatable is False:
                        repeatableList.append('N/A')
                if isLastTaught is True:
                        for ex in extraList:
                                if ex.find('Last Taught:') != -1:
                                        lastTaughtList.append(ex.replace('Last Taught: ', '').strip())
                                        isLastTaught = False
                elif isLastTaught is False:
                        lastTaughtList.append('N/A')
                if isRequisites is True:
                        for ex in extraList:
                                if ex.find('Requisites:') != -1:
                                        requisitesList.append(ex.replace('Requisites: ', '').strip())
                elif isRequisites is False:
                        requisitesList.append('N/A')





def main():
        urls = get_sites()
        for url in urls:
                dataset_maker(url)
                print(url)
        # Make the table
        df['Course Block #'] = courseBlockList
        df['Course Name'] = courseNamesList
        df['Course Description'] = courseDescList
        df['Course Credits'] = courseCreditsList
        df['Requisites'] = requisitesList
        df['Repeatable'] = repeatableList
        df['Last Taught'] = lastTaughtList
        df['Course Designation'] = courseDesignationList

        f = cleanup.cleanup_data(df)

        f.to_csv('data/classes.csv', index=False)


if __name__ == "__main__":
        main()





