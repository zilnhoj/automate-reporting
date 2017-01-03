# automate-reporting

The purpopse of this script is to 
 - Collect data from spreadsheets emailed to the team 
 - Aggregate the data to show daily and weekly values
 - collect data from PIWIK using the PIWIK api
 - Output the collated data in to Google Sheets

# Instructions

Clone the project

When you have cloned it you need to set up a creds folder one level down from your autmoate-reporting folder

In your creds folder you need to make a JSON file which contains your PIWIK token.

The JSON file should be in the format 

{
	"token" : "foo"
}
Replace "foo" with your PIWIK token
You need to call this file piwik_token.json

You will also need to set up acdess to the Google Drive api in order to push the data in the scrip to your spreadsheet

Follow the instructions on how to Authenticate as shown in this blog post http://pbpython.com/pandas-google-forms-part1.html.  
You will need to:
 - set up a project in Google Developer Console
 - download a client_secrets.json file - save the file to your creds folder
 - share the email address given in your client_secrets.json file with your Google drive spreadsheet
 
There is a few things you need to be aware of when running this script


 - You need to copy all the csv files to the relavent folder i.e. all daily verification data needs to go into the data_csvs/verification/daily folder
 - Do not put dublicate files into the folder as all data in the folder will ba aggregates and you will isntroduce duplicated data into your reporting 
 - If you make changes to the script and are commiting them back up to GitHub make sure that you do not include the csv files in the data_csv's folder in the push - remove all files and store them locally before you push back to GitHub

There are 4 seperate scripts used to automate the report reporting process.
 - automate_piwik.py - uses the PIWIK API to get data you need for each RP and puts the data into a Pandas dataframe
 - automate_reporting.py - gathers all the data from your relevant data_csv's folders and aggregates the data into relevant Pandas dataframes for you
 - to_sheets.py - passes the data from dataframes into your Google Sheets tabs
 - data_to_sheets.py - collects all the Pandas dataframes and uses the to_sheets.py script to pass the data into your Google Sheets tabs

# Running the script

When you are running the script for the first time you need to 
 
 - open up the data_to_sheets file in your favourite text editor 
 - look for the line - 'piwik_data = get_piwik_data('2016-11-07,2016-11-13')' - 
 	this line sets the date period for the PIWIK API and should be match the time frame for your latest weekly csv data set.  If you need to get data for a number of weeks you need to run the script for each separate week chaning the date here each time
 
 - in the terminal window make sure you are in the automate-reporting folder
 - type source bin/activate 
 - this activates your virtual environment 
 - type pip install -r requirements.txt
 - this install all the python libraries you need to run the scripts
 - if you want to run the script in iPython type ipython 
 - then type run data_to_sheets.py
 - if you don't want to use ipython type python data_to_scripts.py


