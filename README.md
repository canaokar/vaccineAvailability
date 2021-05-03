# Vaccine Availability Checker

This is a simple serverless application that helps you check the slot availability for any age using the CoWIN open APIs

The script uses Lambda with Python 3.8 environment and an active SNS Topic to send you the alerts. You can trigger the lambda function using CloudWatch Events (EventBridge) to run at specific intervals. 

**Requirements**:
1. Lambda needs a role to allow permissions to publish to SNS topic.
2. SNS Email Subscription needs to be confirmed.
3. Lambda Memory: 128 MB
4. Lambda Duration: 15 sec

**Lambda Role Policy**:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1620068379252",
      "Action": [
        "sns:Publish"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:sns:<region>:<account_ID>:<topic_name>"
    }
  ]
}

**Customization**:
You can customize the script as per your location and requirements:
1. **districtCode**: You can add the district code for your district by looking it up on the link provided here: https://apisetu.gov.in/public/marketplace/api/cowin#/Appointment%20Availability%20APIs/findByDistrict
2. **age**: Set the age 18 or 45
3. **pincodeFirstCharacters**: This is an additional filter which I have added to filter slots near to your location. This is added so that the rural pincodes are filtered out. First four characters are matched. You can customize it by changing the number of characters on **line 42** of the **lambda_function.py** file
4. **topicArn**: You can add your own SNS Topic ARN here to receive alerts. Make sure the Topic type is Standard and subscription is added and confirmed (for email)

Feel free to get in touch with me if you need any assistance. 
