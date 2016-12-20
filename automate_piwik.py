import pandas as pd
import requests
import json
import csv

# def get_piwik_data(start_date,end_date):
def get_piwik_data(date):
# print('start date is {}, end date is {}'.format(start_date,end_date))

# start_date = '2016-11-01'
# end_date = '2016-11-30'
    services = [
        'DWP UCDS', 'DEFRA RP', 'BIS RP', 'DVLA VDL',
        'DVLA F2D REPORT', 'DVLA F2D RENEW', 'HMRC SA', 'HMRC CC',
        'HMRC TE', 'HMRC YSP', 'HMRC PTA', 'HMRC FF',
    ]

    # Pages for which we need page view data
    pages = {
        'cancel_register': 'Cancel - REGISTER',
        'choosing': 'About choosing a company',
        'idp_chosen': 'was chosen for registration',
        'matching': 'Matching Outcome - Match',
        'register_failure': 'Failure - REGISTER',
        'sign_in_start': 'Sign In -',
        'success_register': 'Success - REGISTER',
        'success_sign': 'Success - SIGN_IN'
    }

    # Build the URL
    protocol = 'https'
    domain = 'analytics.ida.digital.cabinet-office.gov.uk'
    path = 'index.php'
    url_template = '{}://{}/{}'
    url = url_template.format(protocol, domain, path)
    with open("../creds/piwik_token.json") as ft:
        token = json.load(ft)

    token = token['token']

    # Build the query string
    qs = {
        'module': 'API',
        'method': 'Actions.get',
        'idSite': '1',
        'period': 'range',
        # 'date': '{},{}'.format(start_date,end_date), # TODO: Update this for the required Date Range
        'date': date,# TODO: Update this for the required Date Range
        'format': 'json',
        'token_auth': token,
    }
    results = {}

    for service in services:
        print("Processing service: {}".format(service))
        service_results = []
        for segment_name, segment_match in pages.items():
            print('Looking up segment: {}'.format(segment_name))
            qs['segment'] = 'pageTitle=@{},customVariableValue1=={}'.format(segment_match, service)
            response = requests.get(url, qs)
            print(response.url)
            raw_result = response.json()
            result = {
                'segment': segment_name,
                'unique_page_views': raw_result['nb_uniq_pageviews'],
                'page_views': raw_result['nb_pageviews']
            }
            service_results.append(result)
        results[service] = service_results

    with open('views.json', 'w') as my_file:
        json.dump(results, my_file, indent=2)

    # Export as csv
    with open('views.csv', 'w') as my_file:
        field_names = ['service', 'segment', 'unique_page_views',
                       'page_views']

        gds_writer = csv.DictWriter(my_file, fieldnames=field_names)
        gds_writer.writeheader()
        for service, segments in results.items():
            for segment in segments:
                segment['service'] = service
                gds_writer.writerow(segment)



    piwikdata = pd.read_csv('views.csv')
    piwikdata['date'] = date[:date.find(',')]
    piwikdata = piwikdata[['date','service', 'segment', 'unique_page_views', 'page_views']]
    return piwikdata

# piwik_date = get_piwik_data('2016-11-01','2016-11-30')
# piwik_data = get_piwik_data()
