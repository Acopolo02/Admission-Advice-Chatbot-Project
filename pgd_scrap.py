import json
from turtle import home
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import os


def checkWord(word, sentence):
  if word in sentence.lower():
    return True
  else:
    return False



def PgdScrap(link):
    courseLink = link
    courseName = courseLink.split("/")[-1:]

    response = requests.get(courseLink)
    soup = BeautifulSoup(response.text, "html.parser")

    path = "./pdg_results"
    fileName = path + "/"+courseName[0]+".txt"

    if os.path.exists(fileName) is False:
        os.mkdir(path)
        with open(courseName[0]+'.html', 'w+') as f:
            f.write(response.text)

    with open(fileName, 'w+', encoding='utf-8') as f:
       # soup = BeautifulSoup(content, 'lxml')
        f.write("Course Information  for " + courseName[0]+ "\n")
        #csv_file = open('criminal_justice_and_crime.csv', 'w')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['course_name','degree_ma_status', 'degree_phd_status', 'full_time_duration', 'part_time_duration', 'course_description', 'home_part_time_fee', 'eu_fee', 'entry_requirement_info'])

        # course name
        course_name = soup.find('div', class_ = "text-content").h1.text.replace(' ', '-')[6:].lower()

        
        degree = soup.find_all('tr')[1]
        degree_status_text = degree.td.text

        # check M.Sc
        isDegree_ma_status = checkWord('ma', degree_status_text) 
        degree_ma_status = 'MA' if isDegree_ma_status else 'none'

        # check PhD
        isDegree_phd_status = checkWord('PhD', degree_status_text) 
        degree_phd_status = 'PhD' if isDegree_phd_status else 'none'

        # full time
        full_time_duration = degree.find_all('td')[1].text

        # part time
        part_time_duration = degree.find_all('td')[2].text

        # course description
        desc = soup.find('div', class_ = "unit golden-large")
        course_desc = desc.find_all('p')[3].text
        course_description = " ".join(course_desc.split())
        
        # fees
        fee = soup.find('div', class_ = "unit whole")
        fees = fee.find_all('ul')
        
        # home fee
        home_fee = fees[0].text.replace(' ', '').split(':')[1]
        home_part_time_fee = fees[1].text.replace(' ', '').split(':')[1]

        # eu/international fee
        eu_fee = fees[2].text.replace(' ', '').split(':')[1]

        # entry enquiry
        enquiry = soup.find_all('div', class_ = "unit golden-large")[1]
        entry_requirement_info = enquiry.find('div').text

        print(f'success result.')

        # export data as csv file
        csv_writer.writerow([course_name,degree_ma_status, degree_phd_status, full_time_duration, part_time_duration, course_description, home_part_time_fee, eu_fee, entry_requirement_info])
        csv_file.close()



PgdScrap("https://www.hull.ac.uk/study/postgraduate/taught/education-ma")