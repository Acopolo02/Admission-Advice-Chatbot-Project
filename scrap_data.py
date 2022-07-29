from turtle import home
import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to scrap data from website
# Accepts a link through the "link" parameter
def Scrap(link):
    courseLink = "https://www.hull.ac.uk/study/undergraduate/drama-and-theatre-practice-ba-hons"
    courseLink = link
    courseName = courseLink.split("/")[-1:]

    # print(courseName)
    
    response = requests.get(courseLink)
    soup = BeautifulSoup(response.text, "html.parser")

    fileName = "./results/" + courseName[0]+".txt"

    with open(fileName, "w", encoding='utf-8') as f:
        keyinfo = soup.select(".key-info")
        f.write(f"courseName: {(courseName[0]+'').upper()}" + "\n")

        f.write("COURSE OVERVIEW")

        divs = soup.select(".visible-content")
        visibleContent = divs[0]
        
        # print(visibleContent)
        children = visibleContent.children
        for child in children:
            f.write(child.text + "\n")

        # print(keyinfo)
        courseLength = keyinfo[0].select(".length")

        # print("\n \n hello ")
        f.write("courseLength " + courseLength[0].text +"\n")
        
        courseCode = keyinfo[0].select(".ucas")[0].text
        f.write("courseCode " + courseCode +"\n")

        title = soup.select(".slabtext")[0].text
        f.write("courseTitle " + title +"\n")

        description = soup.select(".course-interest")[0].text

        courseMode = soup.find("strong", {"property":"courseMode"}).text
        f.write("courseMode " + courseMode +"\n")        
        
        f.write("description " + description +"\n")
        startInformation = keyinfo[0].select(".start")

        frames = soup.select(".frame")
        f.write("\n")
        f.write("courseModules " + "\n")
        lenths = ["First Year", "Second Year", "Third Year", "Fourth Year"]
        index = 0;
        courseModuleToInsertToSQL = ''

        for frame in frames:
            #print(frame)
            try:
                indexIsNone = lenths[index]
            except:
                break
            f.write(lenths[index]+"\n")
            items = frame.select(".items")

            courseModuleToInsertToSQL = courseModuleToInsertToSQL + "\n" + lenths[index]

            for item in items:
                divs = item.select("div")
                for div in divs:
                    children = div.children

                    for child in children:
                        childText = "" if child.next is None else  child.next.text

                        if childText != "":
                            f.write("moduleName " + childText +"\n")
                            courseModuleToInsertToSQL = courseModuleToInsertToSQL + "\n" + "moduleName " + childText

                        #f.write("moduleDescription" + child.next_sibling.text)
            index = index + 1

        homefeeTags = soup.select(".home")
        internationFeeTags = soup.select(".international")
        # print(internationFeeTags)
        homeStudentFee = 0
        internationalFee = 0

        f.write("FEE AND FUNDING " + "\n")

        for item in homefeeTags:
            itemfee = item.select("strong")[0].text
            homeStudentFee = itemfee
        
        f.write("Home STUDENT: " + homeStudentFee + "\n")
        
        # print(homeStudentFee)
        feesToAddToSQL = "Home STUDENT: " + homeStudentFee + "\n"

        for item in internationFeeTags:
            itemchilds = item.select("p")
            for itemchild in itemchilds:
                if len(itemchild) > 0:
                    internationalFee = itemchild.text

        f.write("International STUDENT: " + internationalFee + "\n")

        feesToAddToSQL = feesToAddToSQL + "International STUDENT: " + internationalFee

        # itemfee = item.select("strong")[0].text
        # internationalFee = itemfee

        moreFeeInfo = ''

        moreInfoTags = soup.select(".more-info")
        for tag in moreInfoTags:
            children = tag.children
            for child in children:
                moreFeeInfo += child.text

        f.write("Additional Information about FEE" + moreFeeInfo)


        # entry requirement
        intl = soup.select("#intl-panel")
        internationalStudenEnty = ''
        for itn in intl[0].children:
            internationalStudenEnty += itn.text


        f.write("ENTRY REQUIREMENT: " + "\n")

        f.write("INTERNATIONAL STUDENT: " + internationalStudenEnty)
        
        entryRequirementsToAddToSQL = "INTERNATIONAL STUDENT: " + internationalStudenEnty + '\n'

        localstudent = soup.select(".alevel")
        locaStudentRequirement = ''
        for loc in localstudent:
            # print(loc.name)
            for child in loc.children:
                locaStudentRequirement += child.text +"\n"

        f.write("LOCAL STUDENT: " + locaStudentRequirement)
        
        entryRequirementsToAddToSQL = entryRequirementsToAddToSQL + "LOCAL STUDENT: " + locaStudentRequirement

        addDataToDB(courseName[0], courseLength[0].text, courseCode, title, description, courseModuleToInsertToSQL, feesToAddToSQL, entryRequirementsToAddToSQL)

# function adds data written in text file to db
def addDataToDB(courseName, courseLength, courseCode, courseTitle, description, courseModules, courseFee, entryRequirements):
    # DB
    try:
        sqlConnection = sqlite3.connect('./db/admission_advice_chatbot_db.db')
        cursor = sqlConnection.cursor()


        cursor.execute('''INSERT INTO `Departments` 
            (Name, CourseName, CourseLength, CourseCode, CourseTitle, Description, CourseModules, CourseFee, EntryRequirements) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (courseName, courseName, courseLength, courseCode, courseTitle, description, courseModules, courseFee, entryRequirements))
        sqlConnection.commit()
        print("Successfully added to column", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqlConnection:
            sqlConnection.close()
            print("The SQLite connection is closed")


    # for child in startInformation[0].children:
        # print(child.text)


    # with open(courseName, "a+") as f:
    #     f.write("COURSE OVERVIEW")
    #     divs = soup.select(".visible-content")
    #     visibleContent = divs[0]
    #     children = visibleContent.children
    #     for child in children:
    #         f.write(child.text)
    #     study_mode = keyinfo[0].select("courseMode")
    #     print(description)



#Scrap()


# Function is not called
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("courses-links.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split("\n")
            validLine = line_split[0]
            # print(validLine)
            Scrap(validLine)


