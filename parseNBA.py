
# -*- coding: utf-8 -*-
HEADERTEXT1 = """
Below is the league’s assessment of officiated events that occurred in the last two minutes of last night’s games which were within five points at the two-minute mark (and during
overtime, where applicable). The plays assessed include all calls (whistles) and notable non-calls. Notable non-calls will generally be defined as material plays directly related to the
outcome of a possession. Calls that are indirectly related to the outcome (e.g., a non-call on contact away from the play) and/or plays that are only observable with the help of a
stop-watch, zoom or other technical support, but have some merit in reporting, are noted in brackets along with the explanatory comments. The league may change an opinion after further
review, particularly when a new video angle becomes available. If you have any questions, please contact the NBA Communications Department.
"""
HEADERTEXT2 = """
Below is the league’s assessment of officiated events that occurred in the last two minutes of last night’s games which were within five points at the two-minute mark (and during overtime,
where applicable). The plays assessed include all calls (whistles) and notable non-calls. Notable non-calls will generally be defined as material plays directly related to the outcome of a
possession. Calls that are indirectly related to the outcome (e.g., a non-call on contact away from the play) and/or plays that are only observable with the help of a stop-watch, zoom or other
technical support, but have some merit in reporting, are denoted with an *. The league may change an opinion after further review, particularly when a new video angle becomes available. If
you have any questions, please contact the NBA Communications Department.
"""
HEADERTEXT3 = """
Below is the league’s assessment of officiated events that occurred in the last two minutes of last night’s games which were within five points at the two-minute mark (and during
overtime, where applicable). The plays assessed include all calls (whistles) and notable non-calls. Notable non-calls will generally be defined as material plays directly related to the
outcome of a possession. Calls that are indirectly related to the outcome (e.g., a non-call on contact away from the play) and/or plays that are only observable with the help of a
stop-watch, zoom or other technical support, but have some merit in reporting, are denoted with an *. The league may change an opinion after further review, particularly when a new
video angle becomes available. If you have any questions, please contact the NBA Communications Department.
"""

HEADERTEXT4 = """
Below is the league’s assessment of officiated events that occurred in the last two minutes of last night’s games which were within five points at the two-minute mark (and during overtime,
where applicable). The plays assessed include all calls (whistles) and notable non-calls. Notable non-calls will generally be defined as material plays directly related to the outcome of a
possession. Calls that are indirectly related to the outcome (e.g., a non-call on contact away from the play) and/or plays that are only observable with the help of a stop-watch, zoom or other
technical support, but have some merit in reporting, are noted in brackets along with the explanatory comments. The league may change an opinion after further review, particularly when a
new video angle becomes available. If you have any questions, please contact the NBA Communications Department.
"""


HEADERTEXT =  HEADERTEXT1.strip() + HEADERTEXT2.strip() + HEADERTEXT3.strip() + HEADERTEXT4.strip()
IGNORETEXT = """
                                                                             (CC = Correct Call, IC = Incorrect Call, CNC = Correct Non-Call, INC = Incorrect Non-Call)
Common Play Abbreviations: RSBQ - Rhythm, Speed, Balance, Quickness; POC - Point of Contact; OOB - Out of Bounds; FOM - Freedom of Movement
Common Camera Abbreviations: L/RHH - Left or Right Hand Held; L/RATR - Left or Right Above the Rim; L/RO - Slash - Left or Right Slash
For more information about the rules, go to http://www.nba.com/news/officiating for rule and case books, the NBA Video Rulebook, Misunderstood Rule Explanations and other information
"""


HEADER = "Period            Time                             Call Type                                             Committing Player                                              Disadvantaged Player   Review Decision      Video"

NBAURL = "http://official.nba.com/nba-officiating-last-two-minute-report-%s-%d-%d/"
NBAURL_ALL = "http://official.nba.com/nba-last-two-minute-reports-archive"
import csv
import re
import os
from subprocess import call
import requests
import urllib2
from bs4 import BeautifulSoup as bs

print "Start"

data_header = ["Game", "Period", "Time", "Call Type", "Committing Player", "Disadvantaged Player", "Review Decision", "Comment"]
path = "/Users/rcepsg02/repos/NBAreferees/output/"


def parseFile(infile, outfile):
    data = []
    comment = ""
    g = open(outfile, 'wb')
    writer = csv.writer(g)
    writer.writerow(data_header)
    with open(infile, 'rb') as f:
        start = True
        for line in f:
            if line.replace("","").strip() not in HEADERTEXT.strip() + IGNORETEXT.strip():
                line = line.strip()
                if line not in HEADER:
                    if start:
                        game = line
                        start = False
                        continue
                    if not start:
                        if re.search(r'(\d+/\d+/\d+)',line):
                            start = True
                        elif line[0] == "Q":
                            if data != []:
                                #print [game] + data + [comment]
                                writer.writerow([game] + data + [comment])
                            data =  [x.strip() for x in line.split("          ") if x.strip() != "" and x.strip() != 'Video' and x.strip() != ","]
                            if len(data) == 4:
                                data = data[0:3] + ["",""] + data[3:]
                            elif len(data) == 5:
                                data = data[0:4] + [""] + data[4:]
                        elif "Comment:" in line:
                            comment = line.replace("Comment:","").strip()
                        else:
                            comment = comment + " " + line
    g.close()

def getList(month, day, year):
    #page = requests.get(NBAURL % (month, day, year))
    page = requests.get(NBAURL_ALL)
    soup = bs(page.text)
    gameData = soup.find('div', attrs={'class':'entry-content'})
    i = 0
    for link in gameData.find_all('a'):
        if link.text != "Last Two Minute Reports":
            print link
            pdffile = path + "_".join([month,str(day),str(year)])+"_%d.pdf" % i
            try:
                with open(pdffile, 'wb') as f:
                    print "Writing File %d" % i
                    f.write(urllib2.urlopen(link.get('href')).read())
                rawtext = path + "_".join([month,str(day),str(year)])+"_%d.txt" % i
                parsetext = path + "_".join([month,str(day),str(year)])+"_%d.csv" % i
                print "Converting ", rawtext
                convertPDF(pdffile, rawtext)
                print "Parsing ", parsetext
                parseFile(rawtext,parsetext)
                i = i + 1
            except urllib2.HTTPError:
                print "Error! File Not Found, NBA.com Lied to Us!"
#def pullPDF():
    

def convertPDF(pdf, convertedFile):
#    call(["C:/Program\ Files/XPDF/bin64/pdftotext", pdf, convertedFile, "-layout"])
    call(["pdftotext","-layout", pdf, convertedFile])
if __name__ == '__main__':
    getList("march", 2, 2015)

