# MTG-Database
Magic the Gathering Database

## *Preface*
This is a temporary readme for this project as everything is very rough around the edges.  

## Description
This project's goal is to utilize Python and SQLite together in order to 
1. Connect to the [MTG API](https://magicthegathering.io/)
1. Consume/Process the information available using Python
1. Convert data into SQL friendly format and populate a SQLlite database for local use

## Requirements
1. Python 3.6+
1. [SQLite3](https://www.sqlite.org/index.html)
1. [MTGSDK](https://magicthegathering.io/)
1. SQLite3 library

## The TL:DR
Install Python3.6+ and SQLite.
Place libraries either in the same folder as the core scripts or in your Python Lib folder.
Run FirstTimeSetup.py to create and populate your DB with Ravnica Allegiance.  
The Database should be created and ready to go.

## Key Scripts

### mtgdb.py
This is the primary function storage.  All primary functions are in here.

### FirstTimeSetup.py
Run this script if you are using this for the first time.  Creates your database and populates it with RNA

### RefreshSet.py
Open this and modify the setcode variable to whatever set code you want to populate your DB with.  This will drop all records currently
from that set in the database and then repopulate the entire set

### UpdateDB
Will attempt to bring the DB up to date.  WARNING: can have a significant run time for first time use.  Intended use is for continued database maintenance as new sets are released.


## TODO's

* Add Format legality
* correct double ' character issue in DB
* add card rulings
* add TCG price data
