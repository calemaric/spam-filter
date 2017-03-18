import requests
import json
import csv

API_KEY = "4MdQwafryWTgdCnf4wTWyWGoxzeyyreuAIouXoyLlo9xScZgKufSTUHtMDYrC7Ig"
FORUM = "droidlife"
include = ['spam', 'approved']


def createInclude():
    response = ""

    for x in include:
        response += "&include[]=" + x

    return response


def createUrl(cursor):
    url = 'http://disqus.com/api/3.0/posts/list.json?api_key=' + API_KEY + '&forum=' + FORUM + createInclude() + '&cursor=' + cursor
    return url

def prepareAndWrite(json):
    for object in json:
        for key, value in object.items():
            if value == "":
                value = "NA"

        if object['author']['isAnonymous']:
            object['author']['username'] = "NA"

        if object['author']['isAnonymous']:
            object['author']['reputationLabel'] = "NA"

    writeToCsv(json)

def writeToCsv(json):
    for row in json:
        csv_file.writerow([row["raw_message"],
                           row["dislikes"],
                           row["numReports"],
                           row["likes"],
                           row["author"]["isAnonymous"],
                           row["author"]["username"],
                           row["author"]["reputationLabel"],
                          row['isApproved'],
                          row['points'],
                          row['isSpam']])


csv_file = csv.writer(open("data.csv", "w", encoding='utf-8'))
csv_file.writerow(["raw_message", "dislikes", "num_reports", "likes", "author_is_anonymous", "author_username",
                   "author_reputation_label", "is_approved", "points", "is_spam"])

url = createUrl("")

for i in range(0, 95):
    response = requests.get(url)
    responseJson = response.json()

    print(responseJson)
    prepareAndWrite(responseJson['response'])
    if responseJson['cursor']['hasNext']:
        url = createUrl(responseJson['cursor']['next'])
    else:
        break
