# Overwatch career Web Scraper

A simple cli script that searches for some data from the [overwatch career site](https://playoverwatch.com/en-us/career/pc/)



## How to use:

The script uses BeautifulSoup for scraping and Requests to get the page

Here are some commands:

Add the battletag to be monitored to the Sqlite3 database file

```
CareerOW.py -add Nickname-1234

```

For updating data
```
CareerOW.py -update

```

For showing the battletag

```
CareerOW.py -users

```

For showing the last data

```
CareerOW.py -data

```


Note: Change the url if you play on another region or platform


## What is that?:

A simple web scraper to retrieve some useful information regarding Overwatch's competitive matches.
To get an idea of ​​how quickly I go down to bronze.

Since the last update I have turned this script into a cli utility


Note: Overwatch does not have official Api yet
