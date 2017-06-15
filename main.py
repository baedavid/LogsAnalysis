#!/usr/bin/env python2.7

import datetime #to convert the dataset to date and time easily
import psycopg2

DBName = "news"


def execute(query):
    database = psycopg2.connect(database=DBName)
    n = database.cursor()
    n.execute(query)
    result = n.fetchall()
    database.close()
    return result


def display(query):
    for k in query:
        print query[k][0]
        r = execute(query[k][1])
        for _ in r: #snake-case variable "_"
            print str(_[0]) + str(_[1])

query = dict()

query[1] = ["""
            What are the most popular three articles of all time?
            """]
query[2] = ["""
            Who are the most popular article authors of all time?
            """]
query[3] = ["""
            On which days did more than 1% of requests lead to errors?
            """]
query[1].append("""
                SELECT
                    title,
                    views
                FROM
                    article_views
                ORDER BY
                    views
                DESC
                LIMIT  3
                """)

query[2].append("""
                SELECT
                    name,
                    SUM(views) as views
                FROM
                    article_views
                GROUP BY
                    name
                ORDER BY
                    views
                DESC
                """)


query[3].append("""
                SELECT
                    to_char(date, 'FMMonth DD YYYY,'),
                    percent_error
                FROM
                    error_report
                WHERE
                    percent_error > 1.00;
                """)


display(query) #the results will be appended after to the query for each.
