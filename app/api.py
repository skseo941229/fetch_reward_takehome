from dataclasses import dataclass
from fastapi import Request, FastAPI, HTTPException
from decimal import Decimal
import math 
import uuid 
import json 
app = FastAPI()

point_data = {}

@app.post('/receipts/process')
async def process(request:Request):
    """ 
    Calculate the point and return id  
    """
    
    receipt_list = await request.json()
    
    #Check json format 
    check_keys = {'retailer','total','items','purchaseDate','purchaseTime'}
    if not (receipt_list.keys() >= check_keys):
        return HTTPException(status=404, detail='Check json data')
    
    point = 0
    #One point for every alphanumeric character in the retailer name
    point += sum(s.isalpha() for s in receipt_list['retailer'])
    
    #50 points if the total is a round dollar amount with no cents
    point += 50 if Decimal(receipt_list['total']) == round(Decimal(receipt_list['total'])) else 0
    
    #25 points if the total is a multiple of 0.25
    point += 25 if Decimal(receipt_list['total'])%Decimal(.25) ==0 else 0
    
    # 1) Store item name and # of items in the dictionary 
    # 2) Store item name and price 
    # 3) Store item name and its trimmed length
    item_list = {}
    item_price = {}
    total_item = 0
    for item in receipt_list['items']:
        description = item['shortDescription']
        price = item['price']
        if description in item_list:
            item_list[description] += 1
        else:
            item_list[description] = 1
            item_price[description] = price
        total_item +=1
    
    #5 points for every two items on the receipt
    point += 5*(total_item//2)
    
    #if the trimmend length of the item description is a multiple of 3, round(price *0.2) 
    for key, value in item_list.items():
        trimmed_length = len(key.strip())
        if trimmed_length %3 ==0:
            point += math.ceil(Decimal(item_price[key])*Decimal(0.2))

    #6 points if the day in the purchase date is odd 
    date = int(receipt_list['purchaseDate'][-2:])
    point += 6 if date %2 == 1 else 0

    #10 points if the time of purchase is after 2:00pm and before 4:00 
    time = int(receipt_list['purchaseTime'][:2])
    minute = int(receipt_list['purchaseTime'][-2:])
    if (time == 14 and minute >=1) or time==15:
        point += 10
    
    #randomly generate an id
    new_id = str(uuid.uuid4())
    
    #store id and point
    point_data[new_id] = point 
    
    response = {
        'id': new_id
    }
    return json.dumps(response)

@app.get('/receipts/{id}/points')
async def get_points(id):
    """ 
    Return the points awarded based on the ID 
    """
    
    if id not in point_data:
        return HTTPException(status=404, detail='ID not found')
    response = {
        'points': point_data[id]
    }
    return json.dumps(response)
        