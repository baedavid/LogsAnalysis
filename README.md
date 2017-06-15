# LOGs ANALYSIS

Analyzing the data of viewers on newspaper site.

## Getting Started

You will need VM and python 2.
You also need to download following library.

```
pip install psycopg2
```
You need to download [newsdata.psql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

When you download the newsdata.psql, then move the file into vagrant folder.
Using terminal go into vagrant folder and start vagrant.

```
cd ....../vagrant
vagrant up
vagrant ssh
cd /vagrant
```

Load the data and access the data.

```
psql -d news -f newsdata.sql
psql -d news
```

###View
In order to create view for how many views each articles have, you need following code:

Create view
With a mentor's reference and the notes,
I could sort the data like below:

#(1)for article_views
```
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
```
For query #1 and #2, the dataset is setted up in a way below:
id = integer
author = text
title = text
name = text
views= integer

#for error_report:

```
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
```


For query #3, data set below:
date = date FMMonthYYYY
percent_error = text

## running main.py

on terminal by entering python main.py,

the results come out

```
python main.py
```

#results

1. What are the most popular three articles of all time?
```
Candidate is jerk, alleges rival338647
Bears love berries, alleges bear253801
Bad things gone, say good people170098
```

Who are the most popular article authors of all time?
```
Ursula La Multa507594
Rudolf von Treppenwitz423457
Anonymous Contributor170098
Markoff Chaney84557
```

On which days did more than 1% of requests lead to errors?
```
July 17 2016,2.00
```
