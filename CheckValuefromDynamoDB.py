import boto3
import json
import datetime
import time
import calendar
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print (event)
    center_name = event['sessionState']['intent']['name']
    ##center_name = center_name[0]
    print (center_name)
    client = boto3.resource("dynamodb")
    table = client.Table("cent_info")
##check today is weekday or not##
    today = datetime.today().isoweekday()
    if ((today > 0) and (today < 6)):
        wd = 'true'
        dayno = datetime.today().weekday()
        if (dayno == 0):
            daystart = 'mostrat'
            daystop = 'moend'
        else:
            if (dayno == 1):
                daystart = 'tustart'
                daystop = 'tuend'
            else: 
                if (dayno == 2):
                    daystart = 'westart'
                    daystop = 'weend'
                else:
                    if (dayno == 3):
                        daystart = 'thstart'
                        daystop = 'thend'
                    else:
                        daystart = 'frstart'
                        daystop = 'frend'
            
    else:
        wd = 'false'
        dayno = datetime.today().weekday()
        if (dayno == 5):
            daystart = 'ststart'
            daystop = 'stend' 
        else: 
            daystart = 'sunstart'
            daystop = 'suend'
            
## Getting Center Specific info ##
    
    all = table.query(KeyConditionExpression=Key('icename').eq(center_name))
    item_all = all['Items']
    ##print(item_all)
    ##return ((item_all[0]["tp1"]),(item_all[0]["tp2"]),)
    
## Getting center opening hours##

    censtart = item_all[0][daystart]
    censtop = item_all[0][daystop]
    censtartdt = datetime.strptime(censtart,'%H:%M')
    censtopdt = datetime.strptime(censtop,'%H:%M')
    censtartdt = censtartdt.time()
    censtopdt = censtopdt.time()

## Getting center information ##
    tp1 = item_all[0]["tp1"]
    tp2 = item_all[0]["tp2"]
    cen_actual_name = item_all[0]["cename"]
    
## Getting the current time##

    current = datetime.now()
    current = current + timedelta(hours=8)
    current = current.time()
    current = current.replace(microsecond=0)
    
## Check Center is open now ##
    if (censtartdt<=current<=censtopdt):
        response =  {
    "sessionState": {
        "dialogAction": {
            "type": "Close"
         },
         "intent": {
            "name":"BranchName",
            "state": "Fulfilled"
        }
    },
    "messages": [
        {
            "contentType": "PlainText",
            "content": "Great! "+cen_actual_name+" center is open now. Let me tranfer you there"
        }
    ]
}
    else:
        response =  {
    "sessionState": {
        "dialogAction": {
            "type": "Close"
         },
         "intent": {
             "name":"BranchName",
            "state": "Fulfilled"
        }
    },
    "messages": [
        {
            "contentType": "PlainText",
            "content": "I'm sorry! "+cen_actual_name+" center is close now, Let me transfer to our friendly helpdesk team!"
        }
    ]
}
    return response
    
        
