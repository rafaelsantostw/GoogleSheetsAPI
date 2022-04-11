import requests
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Function to get api data
def getData():
	try:
		#Insert your api url here
		url = ""
		response = requests.get(url)
		data = response.json()
		return data
	except:
		return "Error to call endpoint"

#Function to create a new worksheet with current date name in your spreadsheet with param data.
def generate_google_sheets(sheetsData):
	today = date.today()
	create_date = today.strftime("%d-%m-%Y")

	#You need the credentials.json file in your project
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope) 
	client = gspread.authorize(creds)
	
	spreadsheet = client.open("YOUR_SPREADSHEET_NAME")
	worksheet = spreadsheet.add_worksheet(create_date, len(sheetsData)+1, 1)
  
  #Insert the number of columns that correspond your sheetsData param
	df = pd.DataFrame (sheetsData, columns = ['Data'])
 
	data = [df.columns.values.tolist()]
	data.extend(df.values.tolist())
	worksheet.insert_rows(data)

apiResponse = getData()
generate_google_sheets(apiResponse)
