from __future__ import print_function
import pandas as pd
import json
import os
from os import path
import to_sheets
from to_sheets import updatesheet
# import automate_piwik
# from automate_piwik import get_piwik_data

# import requests
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
#read in the verifications_by_rp_2016-11-02_2016-11-02.csv file into a new Dataframe 
# def main():
    # verification_daily_csvs = os.listdir('data_csvs/verification/daily')
    # verification_weekly_csvs = os.listdir('data_csvs/verification/weekly')

    # billing_daily_csvs = os.listdir('data_csvs/billing/daily')
    # billing_weekly_csvs = os.listdir('data_csvs/billing/weekly')


# def numberToLetters(q):
#     q = q - 1
#     result = ''
#     while q >= 0:
#         remain = q % 26
#         result = chr(remain+65) + result;
#         q = q//26 - 1
#     return result



def aggregate_automate(rpentity):
    if 'ruralpayments.service.gov.uk' in rpentity: #check it the url is in the variable rpentity
        return 'DEFRA RP' #if it is return this url
    elif 'https://www.fitness-to-drive.service.gov.uk/report' in rpentity:
        return 'DVLA F2D REPORT'
    elif 'https://www.fitness-to-drive.service.gov.uk/renew' in rpentity:
        return 'DVLA F2D RENEW'
    elif 'https://www.universal-credit.service.gov.uk' in rpentity:
        return 'DWP UCDS'
    elif 'https://www.viewdrivingrecord.service.gov.uk' in rpentity:
        return 'DVLA VDL'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/FANDF' in rpentity:
        return 'HMRC FANDF'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/MD' in rpentity:
        return 'HMRC CC'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/ISA' in rpentity:
        return 'HMRC SA'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/YSP' in rpentity:
        return 'HMRC YSP'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/PERTAX' in rpentity:
        return 'HMRC PTA'
    elif 'https://prod-left.tax.service.gov.uk/SAML2/TAI' in rpentity:
        return 'HMRC TE'
    elif 'ttps://prod.redundancy-payments.org.uk/' in rpentity:
        return 'Redundancy payments'
    else:
        return rpentity

def get_date(date):
    full_timestamp = date[:date.find('T')]
    return full_timestamp

def get_verification_csvs(csvs,frequency):
    print('data_csvs/verification/'+frequency+'/'+csvs)
    df = pd.read_csv('data_csvs/verification/'+frequency+'/'+csvs)
    df['RP name'] = df.apply(lambda row: aggregate_automate(row['RP Entity Id']),axis=1)
    # df['date'] = df.apply(lambda row: get_date(row['Timestamp']),axis=1)
    df.index = pd.to_datetime(df['Timestamp'])
    # df = df.groupby(['date','RP name','Response type'],as_index=False).resample('W')['Timestamp'].count()
    # df = df.unstack(level=0)

    return df
    # return df

# def get_billing_csvs(billingcsvs, frequency):
#     print('data_csvs/billing/'+frequency+'/'+billingcsvs)
#     df = pd.read_csv('data_csvs/billing/'+frequency+'/'+billingcsvs)
#     # df['IDP name'] = df.apply(lambda row: aggregate_automate(row['Idp Entity Id']),axis=1)
#     # df['RP name'] = df.apply(lambda row: aggregate_f2d(row['RP Entity Id']),axis=1)     
#     df['date'] = df.apply(lambda row: get_date(row['Timestamp']),axis=1)
#     # auto_group_df = df.groupby(['date','IDP name','Billable Status'], as_index=False).count()
#     auto_group_df = df.groupby(['date','Idp Entity Id','Billable Status'], as_index=False).count()
#     return auto_group_df




# resultdf = pd.DataFrame()
# billingdf = pd.DataFrame()
# daily_billingdf = pd.DataFrame()
# weekly_billingdf = pd.DataFrame()

def verification_data():

    verification_daily_csvs = os.listdir('data_csvs/verification/daily')
    verification_weekly_csvs = os.listdir('data_csvs/verification/weekly')


    if '.DS_Store' in verification_daily_csvs:
        verification_daily_csvs.remove('.DS_Store')

    if '.DS_Store' in verification_weekly_csvs:
        verification_weekly_csvs.remove('.DS_Store')

    # billing_daily_csvs = os.listdir('data_csvs/billing/daily')
    # billing_weekly_csvs = os.listdir('data_csvs/billing/weekly')
    frequency = ['daily','weekly']
    resultdf = pd.DataFrame()
    daily_resultdf = pd.DataFrame()
    weekly_resultdf = pd.DataFrame()


    for freq in frequency:
        
        if freq =='daily':
            verification_csvs = verification_daily_csvs
            for csv in verification_csvs:
            
                daily_resultdf = daily_resultdf.append(get_verification_csvs(csv,freq))
                
            # daily_resultdf.reset_index(inplace=True)
            daily_resultdf['frequency'] = freq
            print(daily_resultdf.columns)
            daily_resultdf.index = pd.to_datetime(daily_resultdf['Timestamp'])
            # daily_resultdf = daily_resultdf.groupby(['date','RP name','Response type'], as_index=False).count()

        else:
            verification_csvs = verification_weekly_csvs

            for csv in verification_csvs:
                weekly_resultdf = weekly_resultdf.append(get_verification_csvs(csv,freq))
            
            # weekly_resultdf.reset_index(inplace=True)
            weekly_resultdf['frequency'] = freq
            weekly_resultdf.index = pd.to_datetime(weekly_resultdf['Timestamp'])
            

    return daily_resultdf, weekly_resultdf

def format_vf_df(df,type): #type is either NEW or RETURNING

    if type == 'new':
        df = df[df['Response type']=='NEW']
        df.fillna(0, inplace=True)
        df = df[['Timestamp','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT']]


    else:
        df = df[df['Response type']=='RETURNING']
        df.fillna(0, inplace=True)
        df = df[['Timestamp','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT']]
        
    return df

def totals(df):
    dfcolumns = list(df.columns)
    dfcolumns.remove('Timestamp')
    df['total'] = df[dfcolumns].sum(axis=1)
    return df['total']

def set_cols(df):
    df['total'] = totals(df)

    df = df[['Timestamp','total','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP','DVLA F2D RENEW','DVLA F2D REPORT']]

    return df

def get_final_df():
    daily_resultdf, weekly_resultdf = verification_data()

    daily_resultdf = daily_resultdf.groupby(['RP name','Response type']).resample('D')['Response type'].count()
    daily_resultdf = daily_resultdf.unstack(level=0)
    daily_resultdf.reset_index(inplace=True)
    # daily_resultdf['total'] = totals(daily_resultdf)


    weekly_resultdf = weekly_resultdf.groupby(['RP name','Response type']).resample('W')['Response type'].count()
    weekly_resultdf = weekly_resultdf.unstack(level=0)
    weekly_resultdf.reset_index(inplace=True)
    # weekly_resultdf['total'] = totals(weekly_resultdf)

    daily_new_pivot = format_vf_df(daily_resultdf,'new')
    daily_new_pivot = set_cols(daily_new_pivot)
    weekly_new_pivot = format_vf_df(weekly_resultdf,'new')
    weekly_new_pivot = set_cols(weekly_new_pivot)
    daily_returning_pivot = format_vf_df(daily_resultdf,'returning')
    daily_returning_pivot = set_cols(daily_returning_pivot)
    weekly_returning_pivot = format_vf_df(weekly_resultdf,'returning')
    weekly_returning_pivot = set_cols(weekly_returning_pivot)

    return daily_new_pivot, weekly_new_pivot, daily_returning_pivot, weekly_returning_pivot

# daily_new_pivot, weekly_new_pivot, daily_returning_pivot, weekly_returning_pivot = get_final_df()


    # daily_new_pivot = format_vf_df(daily_resultdf, 'new')



    # weekly_resultdf = weekly_resultdf[['date','RP name','Response type', 'RP Entity Id']]
    # daily_resultdf = daily_resultdf[['date','RP name','Response type', 'RP Entity Id']]
    # daily_resultdf.rename(columns={'RP Entity Id':'count'}, inplace=True)
    # weekly_resultdf.rename(columns={'RP Entity Id':'count'}, inplace=True)

    # # daily_billingdf = daily_billingdf[['date','Idp Entity Id', 'Billable Status','Timestamp']]
    # # weekly_billingdf = weekly_billingdf[['date','Idp Entity Id', 'Billable Status','Timestamp']]
    # # daily_billingdf.rename(columns={'Timestamp':'count'}, inplace=True)
    # # weekly_billingdf.rename(columns={'Timestamp':'count'}, inplace=True)

    # daily_resultdf_new = daily_resultdf[daily_resultdf['Response type']=='NEW']
    # daily_resultdf_returning = daily_resultdf[daily_resultdf['Response type']=='RETURNING']

    # weekly_resultdf_new = weekly_resultdf[weekly_resultdf['Response type']=='NEW']
    # weekly_resultdf_returning = weekly_resultdf[weekly_resultdf['Response type']=='RETURNING']

    # daily_new_pivot = daily_resultdf_new.pivot(index='date', columns='RP name', values='count')
    # daily_returning_pivot = daily_resultdf_returning.pivot(index='date', columns='RP name', values='count')
    # weekly_new_pivot = weekly_resultdf_new.pivot(index='date', columns='RP name', values='count')
    # weekly_returning_pivot = weekly_resultdf_returning.pivot(index='date', columns='RP name', values='count')


    # daily_new_pivot.fillna(0, inplace=True)
    # daily_new_pivot['date'] = daily_new_pivot.index
    # daily_new_pivot = daily_new_pivot[['date','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP']]
    # daily_new_pivot['total'] = daily_new_pivot.sum(axis=1)

    # daily_returning_pivot.fillna(0, inplace=True)
    # daily_returning_pivot['date'] = daily_returning_pivot.index
    # daily_returning_pivot = daily_returning_pivot[['date','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP']]
    # daily_returning_pivot['total'] = daily_returning_pivot.sum(axis=1)

    # weekly_new_pivot.fillna(0, inplace=True)
    # weekly_new_pivot['date'] = weekly_new_pivot.index
    # weekly_new_pivot = daily_new_pivot[['date','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP']]
    # weekly_new_pivot['total'] = weekly_new_pivot.sum(axis=1)

    # weekly_returning_pivot.fillna(0, inplace=True)
    # weekly_returning_pivot['date'] = weekly_returning_pivot.index
    # weekly_returning_pivot = weekly_returning_pivot[['date','DEFRA RP','DVLA VDL','DWP UCDS','HMRC CC','HMRC FANDF','HMRC PTA','HMRC SA','HMRC TE','HMRC YSP']]
    # weekly_returning_pivot['total'] = weekly_returning_pivot.sum(axis=1)

    # for freq in frequency:
        
    #     if freq =='daily':
    #         print('billing: '+freq)
    #         billing_csvs = billing_daily_csvs
    #         for csv in billing_csvs:
            
    #             daily_billingdf = daily_billingdf.append(get_billing_csvs(csv,freq))

    #         daily_billingdf['frequency'] = freq

    #     else:
    #         billing_csvs = billing_weekly_csvs

    #         for csv in billing_csvs:
            
    #             weekly_billingdf = weekly_billingdf.append(get_billing_csvs(csv,freq))

    #         weekly_billingdf['frequency'] = freq
# piwik_date = get_piwik_data('2016-11-01','2016-11-30')

# weekly_new_pivot.fillna(0, inplace=True)
# weekly_returning_pivot.fillna(0, inplace=True)


# daily_billingdf = daily_billingdf[['date','IDP name', 'Billable Status','Idp Entity Id']]
# weekly_billingdf = weekly_billingdf[['date','IDP name', 'Billable Status','Idp Entity Id']]
# daily_billingdf.rename(columns={'Idp Entity Id':'count'}, inplace=True)
# weekly_billingdf.rename(columns={'Idp Entity Id':'count'}, inplace=True)


# updatesheet('testing_auto', 'first_sheet',daily_resultdf)

# updatesheet('testing-automation authentication datasets', 'Daily Verifications RP Data From Script',daily_new_pivot)
# updatesheet('testing-automation authentication datasets', 'Daily Signins RP Data From Script',daily_returning_pivot)
# updatesheet('testing-automation authentication datasets', 'Weekly Verifications RP Data From Script',weekly_new_pivot)
# updatesheet('testing-automation authentication datasets', 'Weekly Signins RP Data From Script',weekly_returning_pivot)
# SCOPE = ["https://spreadsheets.google.com/feeds"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', SCOPE)

# gc = gspread.authorize(credentials)
# num_lines, num_columns = daily_new_pivot.tail(1).shape
# # spreadsheet = gc.open(spreadsheet_name)
# spreadsheet = gc.open('testing-automation authentication datasets')
# worksheet = spreadsheet.worksheet('testing verifications by rp')
# wks_columns = worksheet.col_count

# if __name__ == '__main__':
#   main()