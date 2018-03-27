#! /usr/bin/env python
"""
Script to scrape and parse the Rutgers eSuds site.
"""

import os
import re
from datetime import datetime

import requests
import boto3
from bs4 import BeautifulSoup


API_ENDPOINT = """http://rutgers.esuds.net/RoomStatus/machineStatus.i?bottomLocationId="""
BUILDING_NUM = [
    # College Ave
    '1277',
    '1279',
    '1280',
    '1282',
    '1283',
    '1284',
    '1285',
    '1286',
    '1287',
    '1288',
    '1289',
    '1672',
    '1572',
    '1040513',
    '1014385',
    '1038177',
    '2076549',
    '2081769',
    '2083734',
    # Busch
    '1216', 
    '1217',
    '1218',
    '1219',
    '1220',
    '1221',
    '1222',
    '1223',
    '1224',
    '1225',
    '1226',
    '1227',
    '1228',
    '1229',
    '1230',
    '1231',
    '1237',
    '1238',
    '1574',
    '1034816',
    '1034817',
    '1034818',
    '1034820',
    '1034821',
    '1034822',
    '1034824',
    '1034825',
    '1034830',
    '1034831',
    '1034832',
    '1034833',
    '1034835',
    '1034836',
    '1034837',
    '1034838',
    '1034839',
    '1034841',
    '1034842',
    '1034843',
    '1034844',
    '1034845',
    '1034847',
    '1034849',
    '1034850',
    '1034851',
    '1034852',
    '1034853',
    '1034854',
    '1034855',
    '1034857',
    '1034858',
    '1034859',
    '1034863',
    '1034876',
    '1034877',
    '1040423',
    '1040424',
    '1040461',
    '1040473',
    # Livingston
    '1302',
    '1303',
    '1304',
    '1306',
    '1307',
    '1308',
    '1309',
    '2043487',
    '2043488',
    '2043489',
    # Cook
    '1290',
    '1291',
    '1292',
    '1575',
    '1039070',
    '2088909',
    # Douglass
    '1293',
    '1294',
    '1295',
    '1296',
    '1297',
    '1298',
    '1299',
    '1300',
    '1301',
    '1039052',
    '1039085',
    '2083703',
]


def lambda_handler(event, context):
    """Scrape from Rutgers eSuds site."""

    d = dict()
    labels = list()
    counts = list()

    # Download and open file from S3
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('esuds-bucket', 'data.csv', '/tmp/data.csv')
    fd = open('/tmp/data.csv', 'a')

    # Loop through building numbers
    for num in BUILDING_NUM:

        washers_running = 0
        dryers_running = 0

        url = API_ENDPOINT + num

        # Make POST request to the api endpoint
        response = requests.post(url=url)

        # Create soup object
        soup = BeautifulSoup(response.text, 'html.parser')

        for tr in soup.find_all('tr'):
            tr = str(tr)
            if 'In Use' in tr:
                if 'Washer' in tr:
                    washers_running += 1
                elif 'Dryer' in tr:
                    dryers_running += 1
        
        fd.write('{},{},{},{}\n'.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            num, washers_running, dryers_running))

    # Close, upload, and delete data file
    fd.close()
    s3.meta.client.upload_file('/tmp/data.csv', 'esuds-bucket', 'data.csv')
