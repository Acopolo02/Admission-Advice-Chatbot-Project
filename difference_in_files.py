# Spots differences between two files and returns result in difference_report.html

import difflib

first_file = "./html/undergraduate/british-politics-and-legislative-studies-ba-hons.txt"

# file to compare
second_file = "./html/undergraduate/music-community-and-education-ba-hons.txt"

first_file_lines = open(first_file).readlines()
second_file_lines = open(second_file).readlines()

difference = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines, first_file, second_file)
difference_report = open('./html/difference_report.html', "w")
difference_report.write(difference)
difference_report.close()