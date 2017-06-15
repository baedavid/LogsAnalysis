###LOG ANALYSIS

##Description
#You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.
The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity
The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

#Preparation
- To begin, it needs to be connected to vagrant by vagrant up and vagrant ssh. Then it should be connected to the directory where vagrantfile and the datafile are located by using cd/vagrant.
- using psql -d news -f newsdata.sql then psql - d news enable to load and work on sorting data file.
- I could either sort and create the new variable for this project by editing in the terminal or by creating a separate file. However, I directly worked through the terminal first to set up the variables like views and errors.

#Create view
With a mentor's reference and the notes,
I could sort the data like below:

#(1)for article_views

CREATE VIEW
    article_views
AS
     SELECT
        a.id,
        a.author,
        a.title,
        au.name,
        v.views
     FROM
        (
        SELECT
            l.path,
            count(*) as views
        FROM
            log l,
            articles a (#joining two tables)
        WHERE
            CONCAT('/article/',a.slug) = l.path (#joining the slug into the format by using CONCAT)
        AND
            l.status = '200 OK'
        GROUP BY
            l.path
        )   v,
        articles a,
        authors au
     WHERE
        CONCAT('/article/',a.slug) = v.path
     AND
        au.id = a.author;

For query #1 and #2, the dataset is setted up in a way below:
id = integer
author = text
title = text
name = text
views= integer

#for error_report:

CREATE VIEW
          error_report
    AS
      SELECT
          error_report.date,
          round(100*error_report.errors/total_requests.total,2) as percent_error #to round it to the percentile scale
      FROM
          (SELECT
              date(time) as date (#rename the variable),
              COUNT(*) as errors
           FROM
              log
           WHERE
              status != '200 OK' (#set a condition)
           GROUP BY
              date(time)
           ORDER BY
              COUNT(*)
           ) error_report,
           (SELECT
              date(time) as date,
              COUNT(*) as total (#count the numbers as total)
            FROM
              log #only from the log table
            GROUP BY
              date
           ) total_requests (#it needs to display the date and the total_requests for error report)
       WHERE
            total_requests.date = error_report.date;

For query #3, data set below:
date = date FMMonthYYYY
percent_error = text

# running main.py

on terminal by entering python main.py,

the results come out

#results

What are the most popular three articles of all time?

Candidate is jerk, alleges rival338647
Bears love berries, alleges bear253801
Bad things gone, say good people170098

Who are the most popular article authors of all time?

Ursula La Multa507594
Rudolf von Treppenwitz423457
Anonymous Contributor170098
Markoff Chaney84557

On which days did more than 1% of requests lead to errors?

July 17 2016,2.00
