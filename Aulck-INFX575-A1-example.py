#Lovenoor Aulck - INFX 575 Assignment 1 Example
#4/6/2016

#Please note - this code has been stripped down from its original form. There may be bit/pieces of
#leftover code that are redundant or unnecessary. At the least, it should give an idea of how to scrape.
#There are definite ways to improve the code (i.e. zipping the lists before iteration to do a single
#loop through) but this still runs pretty quick (<2 secs) as a working example.

from bs4 import BeautifulSoup; #import beautiful soup scraper
import urllib2 #url library
import pandas as pd; #dataframe for final output
import re #regular expression package

#%%
url= 'http://www.pugetsound.edu/academics/faculty-scholarship/faculty-list/all/' #set url
page = urllib2.urlopen(url) #open the url
soup = BeautifulSoup(page.read()) #read in beautiful soup

#%%
names = [s.get_text() for s in soup.find_all('h3')] #get faculty name list
depts = [(s.get_text()).strip() for s in soup.find_all("td", { "class":"dept" })] #get department list
education = [s.get_text() for s in soup.find_all('ul')] #get degree list
education = education[:-1] #list has erroneous value
degrees = [(s.get_text()).split(',')[0].strip() for s in soup.find_all('li')] #get a list of every degree earned for all faculty
degrees = degrees[:617] #remove erroneous elements
degrees = list(set(degrees)) #take only unique values
degrees = degrees[1:] #keep as a list of degree names

#%%
fname = [] #empty lists
lname = []
title = []
department = []
degreeList = []
gradYr = []
schoolNum = []

for each in names:
    each = each.strip() #remove white space
    current = each.split(',') #split at comma
    fname.append(current[1].strip()) #first name after the comma
    lname.append(current[0]) #last name before the comma

for each in depts:
    each = each.strip() #remove white space
    current = each.split(',') #split at comma
    title.append((current[0].split('and')[0]).strip()) #take only the first position
    if len(current) > 1: #if a department is listed, get it
        currentDept = current[1].split('\n')
        department.append((currentDept[0].split('and')[0].split('&')[0]).strip())
    else:
        department.append("") #if not, add a blank

for each in education:
    current = [(x.strip()) for x in each.split(',')] #split the education info at commas
    years = '' #empty strings
    degree = ''
    location = ''
    tokens = [] #empty token array
    for each in current: #creates a list of string elements as tokens
        if (not each.isdigit() and each[0:4].isdigit()): #to check for names and degrees melded together
            tokens.append(each[0:4])
            tokens.append(each[4:])
        else:
            tokens.append(each)
    for each in tokens: #check each token
        if each.isdigit(): #if a year
            years += (each + ', ')
        elif each in degrees: #if a degree
            degree += (each + ', ')
        else: #else a location/school
            location = each
    location = location.lower() #convert to lower case
    locationTokens = re.findall(r"[\w']+", location) #split location into tokens
    gradYr.append(years[:-2]) #remove unnecessary commas/spaces
    degreeList.append(degree[:-2]) #remove unnecessary commas/spaces

#%%

output = pd.DataFrame(fname) #create a dataframe for outputs
output.columns = ['firstnames']
output['lastname'] = lname
output['graddegree'] = degreeList
output['gradyear'] = gradYr
output['facultyschool'] = 370
output['facultydept'] = department
output['facultytitle'] = title

output.to_csv('Aulck-INFX575-PS1 dataset.csv')
