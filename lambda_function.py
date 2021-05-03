import json
import os
import datetime
import urllib3
import ast
import boto3

#Global Variables - Customize Here!
districtCode = 363 #Change to your own district. More info from https://apisetu.gov.in/public/marketplace/api/cowin#/Appointment%20Availability%20APIs/findByDistrict
age = 18 # Valid Values are 18 or 45 only
pincodeFirstCharacters = "4110" # Filter according to your pincode
topicArn = 'YOUR_TOPIC_ARN_HERE' # Your topic ARN

def lambda_handler(event, context):
    
    # Build the URL
    rawdate = datetime.datetime.now()
    dateformat = "a"
    date = rawdate.strftime("%d-%m-%Y")
    urlfixed = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="
    url = urlfixed + str(districtCode) + "&date=" + date
    
    # Call HTTP URL (GET)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    y=r.data
    x = y.decode("UTF-8")
    centers=ast.literal_eval(x)
    
    # SNS Client Creation
    sns = boto3.client('sns', region_name='ap-south-1')
    
    # Initialize the dict
    resultDict =[]
    
    #Parse
    if isinstance(centers, dict):
        for k, v in centers.items(): #centers(k is str, v is list)
            for i in v:
                for val in i['sessions']:
                    pincodeMatch = str(i['pincode'])
                    if (val['min_age_limit'] == age and  val['available_capacity'] > 0 and pincodeFirstCharacters == pincodeMatch[:4]):
                        result = "Center Name: " + i['name'] + ", " + "Pin Code: " + str(i['pincode']) + ", " + "Date: " + val['date'] + ", " + "Available Doses: " + str(val['available_capacity'])
                        resultDict.append(result)

    if not resultDict:
        print("Empty")
    else:
        response = sns.publish(TopicArn=topicArn, Message=str(resultDict), Subject="VACCINE ALERT!")
        print("Response Mailed!")
    
    return resultDict
