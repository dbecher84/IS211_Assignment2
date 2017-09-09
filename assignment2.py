#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Downloads a csv file of person info from url using command prompt"""

import urllib2
import csv
import datetime
import logging
import logging.handlers
import argparse


parser = argparse.ArgumentParser(description='url to download file from')
parser.add_argument('-u', '--url', type=str, help="The url of the csv file to download")
args = parser.parse_args()


LOG_ERRORS = 'error.log'
logging.basicConfig(filename=LOG_ERRORS, filemode='w', level=logging.ERROR)
logger = logging.getLogger('assignment2')
URL = args.url
#https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv

def main(input_url):
    """combines functions to diplay person data from id number.
    args:
        unput_url (str): url of csv file to be downloaded.

    retruns:
        see returns for displayperson function.

    example:
        >>> main('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
        Enter employee id number: 50
        ('Trevor Clarkson', '01/08/1979')
        Enter employee id number: 60
        ('Madeleine Roberts', '03/05/2002')
        Enter employee id number: -5
    """

    downloaded = downloaddata(input_url)
    processdata(downloaded)
    repeat = True
    while repeat:
        emp_id = int(raw_input("Enter employee id number: "))
        if emp_id > 0:
            displayperson(emp_id)
        else:
            repeat = False

def downloaddata(url=URL):
    """functions that accepts a url.
    args:
        url (str): a url for a webiste. default=URL
    returns:
        data: url object.
    """
    data = urllib2.urlopen(url)
    return data


PERSON_DATA = {}


def processdata(file_contents=downloaddata):
    """
    args:
        file_content: a csv file from the specified url.
                      default=downloaddata

    returns:
        dictionary entry to be added to the PERSON_DATA dictionary.
    """
    extract = csv.reader(file_contents)
    next(extract, None)
    row_count = 2
    for row in extract:
        try:
            row_id = row[0]
            date = datetime.datetime.strptime(row[2], '%d/%m/%Y')
            id_data = {int(row[0]):(row[1], date.strftime('%d/%m/%Y'))}
            PERSON_DATA.update(id_data)
            row_count += 1
        except ValueError:
            logging.error('Error at line #%s for ID #%s' %(row_count, row_id))
            row_count += 1


def displayperson(person_id, dictionary=PERSON_DATA):
    """Displays the name and birthday of person.
    args:
        person_id (int): the id number of the person
        dictionary (dict): Dicionary of people with id as keys

    returns:
        tuple: the persons name and birthday

    example:
        >>> displayperson(50)
        ('Trevor Clarkson', '01/08/1979')
    """

    try:
        birthday = dictionary[person_id]
        print birthday
    except Exception:
        print "No user found with that ID."


if args.url:
    main(URL)
else:
    print "No argument was given"
