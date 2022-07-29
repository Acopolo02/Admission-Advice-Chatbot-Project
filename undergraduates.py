import requests
from bs4 import BeautifulSoup

def ScrapUndergraduateCourses():
    try:
        with open("undergraduateweblinks.txt", "r") as file:

            lines = file.readlines()
            for line in lines:
                try:
                    lineSplit = line.split("/")
                    lastInList = lineSplit[-1:]
                    # print(lastInList)
                    courseName = lastInList[0].split("\n")[0]
                    print("courseName " + courseName)
                    Scrap(courseName, line)
                except Exception as e:
                    # print(e.__cause__)
                    # print(e.__str__())
                    continue

    except Exception as e:
        print(e.__str__())



def Scrap(courseName, link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    _courseName = courseName+".txt"

    with open(_courseName, "a+") as f:
        keyinfo = soup.select(".key-info")
        f.write(f"courseName: {courseName}" + "\n")
        print(keyinfo)
        f.write("COURSE OVERVIEW")
        divs = soup.select(".visible-content")
        # print(divs)
        visibleContent = divs[0]
        children = visibleContent.children
        for child in children:
            f.write(child.text + "\n")


        #print(keyinfo)
        courseLength = keyinfo[0].select(".length")
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
        for frame in frames:
            #print(frame)
            try:
                indexIsNone = lenths[index]
            except:
                break
            f.write(lenths[index]+"\n")
            items = frame.select(".items")
            for item in items:
                divs = item.select("div")
                for div in divs:
                    children = div.children

                    for child in children:
                        childText = "" if child.next is None else  child.next.text

                        if childText != "":
                            f.write("moduleName " + childText +"\n")
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

        for item in internationFeeTags:
            itemchilds = item.select("p")
            for itemchild in itemchilds:
                if len(itemchild) > 0:
                    internationalFee = itemchild.text

        f.write("International STUDENT: " + internationalFee + "\n")

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
        localstudent = soup.select(".alevel")
        locaStudentRequirement = ''
        for loc in localstudent:
            # print(loc.name)
            for child in loc.children:
                locaStudentRequirement += child.text +"\n"

        f.write("LOCAL STUDENT: " + locaStudentRequirement)

ScrapUndergraduateCourses()