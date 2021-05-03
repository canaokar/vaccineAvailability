import json
import os
import datetime
import urllib3
import logging
import ast
import boto3

def lambda_handler(event, context):
    
    logger = logging.getLogger()
    # API Call for Today
    rawdate = datetime.datetime.now()
    dateformat = "a"
    date = rawdate.strftime("%d-%m-%Y")
    districtCode = 363
    urlfixed = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="
    url = urlfixed + str(districtCode) + "&date=" + date
    
    #Call HTTP URL (GET)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    y=r.data
    x = y.decode("UTF-8")
    centers=ast.literal_eval(x)
    
    #SNS Client Creation
    sns = boto3.client('sns', region_name='ap-south-1')
    
    #Parameters
    age = 18
    charsToMatch = "4110"
    resultDict =[]
    
    logger.info(centers)
    #Parse
    if isinstance(centers, dict):
        for k, v in centers.items(): #centers(k is str, v is list)
            for i in v:
                for val in i['sessions']:
                    pincodeMatch = str(i['pincode'])
                    if (val['min_age_limit'] == age and  val['available_capacity'] == 0 and charsToMatch == pincodeMatch[:4]):
                        result = "Center Name: " + i['name'] + ", " + "Pin Code: " + str(i['pincode']) + ", " + "Date: " + val['date'] + ", " + "Available Doses: " + str(val['available_capacity'])
                        resultDict.append(result)

    if not resultDict:
        print("Empty")
    else:
        response = sns.publish(TopicArn='YOUR_TOPIC_HERE', Message=str(resultDict), Subject="VACCINE ALERT!")
        print("Response Mailed!")
    
    return resultDict
