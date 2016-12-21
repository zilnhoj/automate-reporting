import automate_reporting
from automate_reporting import get_final_df
import to_sheets
from to_sheets import updatesheet 
from to_sheets import spreadsheet_setup
import pandas as pd
import automate_piwik
from automate_piwik import get_piwik_data

daily_new_pivot, weekly_new_pivot, daily_returning_pivot, weekly_returning_pivot = get_final_df()
len_daily_new_pivot = len(daily_new_pivot)
len_daily_returning_pivot = len(daily_returning_pivot)
len_weekly_new_pivot = len(weekly_new_pivot)
len_weekly_returning_pivot = len(weekly_returning_pivot)


updatesheet('testing-automation authentication datasets', 'Daily Verifications RP Data From Script',daily_new_pivot,2,len_daily_new_pivot)
updatesheet('testing-automation authentication datasets', 'Daily Signins RP Data From Script',daily_returning_pivot,2,len_daily_returning_pivot)
updatesheet('testing-automation authentication datasets', 'Weekly Verifications RP Data From Script',weekly_new_pivot,2,len_weekly_new_pivot)
updatesheet('testing-automation authentication datasets', 'Weekly Signins RP Data From Script',weekly_returning_pivot,2,len_weekly_returning_pivot)

# piwik_data = get_piwik_data('2016-11-07,2016-11-13')
# gc = spreadsheet_setup()
# spreadsheet = gc.open('testing-automation authentication datasets')
# worksheet = spreadsheet.worksheet('PIWIK Data From Script')
# pwkdf = pd.DataFrame(worksheet.get_all_values())
# start_cell = len(pwkdf)
# length_new_data = len(piwik_data)

# if start_cell>1:
# 	updatesheet('testing-automation authentication datasets', 'PIWIK Data From Script',piwik_data,start_cell,length_new_data)
# else:
# 	updatesheet('testing-automation authentication datasets', 'PIWIK Data From Script',piwik_data,2,length_new_data)
