# The Ole' Ball and Chain: A Society Burdened by Moral Grandstanding

In the past few years, we have seen a drastic increase in the number of books being challenged and/or banned across the United States. According to the American Library Association (ALA), the number of titles targeted for censorship in 2023 rose an astounding 65% from the number of titles targeted in 2022. This dramatic increase got me thinking. What could be causing this surge in book censorship efforts? What types of books are being targeted? Does attempting to censor or ban a book make it more appealing to readers?

In this project I'll explore the topic of book censorship in the United States. I'll use data collected from the ALA, EveryLibrary, Goodreads, Publishers Weekly, and the National Center for Education Statistics in my analysis.  


## Getting Started

First, you need to download the `book_censorship` GitHub repository.

You can clone the repository from the command line:
```
!git clone https://github.com/grrlofhighart/book_censorship.git

```
Or you can download the repository from:

https://github.com/grrlofhighart/book_censorship/archive/master.zip



## Project Structure:

  1. ALA_Banned_Archive.ipynb - Guide for Collection of Banned Book data from the ALA website.
  2. Goodreads_List_Scrape.ipynb - Guide for Collection of Book data from the Goodreads website. Includes book title, series, isbn, isbn13, publish date, author, number of pages, genres, number of review, reviews text, number of ratings, average rating, and rating distribution.
  3. PW_Scrape.ipynb - Guide for Collection of book data from the Publishers Weekly website.
  5. Book_Analysis - Walkthrough of my analysis of the data collected.
     

## Websites mentioned:

  1. [American Library Association](https://www.ala.org/bbooks/frequentlychallengedbooks/top10/archive)
  2. [Goodreads Listopia: Best Banned, Censored, and Challenged Books](https://www.goodreads.com/list/show/1360.Best_Banned_Censored_and_Challenged_Books)
  3. [EveryLibrary](https://www.everylibraryinstitute.org/book_censorship_database_magnusson)
  4. [Publishers Weekly](https://www.publishersweekly.com/pw/nielsen/top100.html)
  5. [National Center for Education Statistics](https://nces.ed.gov/ccd/elsi/)


# What You Will Need

To run all scripts in this project you will need [Python 3](https://www.python.org/downloads/) along with the following Python libraries:

- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Requests](https://requests.readthedocs.io/en/latest/user/install/#install)
- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
- [lxml](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser)
- [geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/)
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Numpy](https://numpy.org/install/)
- [matplotlib](https://matplotlib.org/stable/install/index.html)
- [seaborn](https://seaborn.pydata.org/installing.html)

You can install these Python libraries by running `pip install -r requirements.txt`

