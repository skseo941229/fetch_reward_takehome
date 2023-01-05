import json
import requests
import json

data1  = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
test1 = requests.post("http://127.0.0.1:8000/receipts/process", json = data1)
test_id = test1.json()
test_ans1 = json.loads(test_id)
print("Test1's id: ", test_ans1['id'])
test1_point = requests.get("http://127.0.0.1:8000/receipts/" + str(test_ans1['id']) +"/points")
print("Test1's point: ", test1_point.text)

data2 = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
test2 = requests.post("http://127.0.0.1:8000/receipts/process", json = data2)
test_id = test2.json()
test_ans2 = json.loads(test_id)
print("Test2's id: ", test_ans2['id'])
test2_point = requests.get("http://127.0.0.1:8000/receipts/" + str(test_ans2['id']) +"/points")
print("Test2's point: ", test2_point.text)
