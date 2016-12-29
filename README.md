# automate-reporting

The purpopse of this script is to 
 - Collect data from spreadsheets emailed to the team 
 - Aggregate the data to daily and weekly data sets
 - collect data from the PIWIK api
 - Output the collated data in to Google Sheets

# Instructions

Clone the project

When you have cloned it you need to set up a creds folder one level down from your autmoate-reporting folder

In your creds folder you need to make a JSON file which contains your PIWIK token.

The JSON file should be in the format 

{
	"token" : "foo"
}
where "foo" is your PIWIK token
You need to call this file piwik_token.json

You will also need to set up acdess to the Google Drive api in order to push the data in the scrip to your spreadsheet

Follow the instructions on Authentication in this blog post http://pbpython.com/pandas-google-forms-part1.html to
 - set up a project in Google Developer Console
 - download a client_secrets.json file - save the file to your creds folder
 - chare the email address given in your client_secrets.json file with your Google drive spreadsheet
 
The is a few things you need to do when runnging this script

 1 You need to copy all the csv files to the relavent folder i.e. all daily verification data needs to go into the data_csvs/verification/daily folder
 2 Do not put dublicatte files as this duplicated data will ba aggregates and you will include duplicated data into your reporting 
 3 If you make changes to the script and are commiting them back up to GitHub make sure that you do not include the data in the push - remove all files and store them locally before you push back to GitHub
 
 
 
