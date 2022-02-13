from flask import Flask, render_template
import requests
import json
import numpy
import time

ce_nifty = {}
pe_nifty = {}
time_count_nifty = []
start_nifty = 0

ce_bank = {}
pe_bank = {}
time_count_bank = []
start_bank = 0

date = "03-Feb-2022"

for i in range(16000,19050,50):
    ce_nifty[i] = []
    pe_nifty[i] = []

for i in range(35000,40100,100):
    ce_bank[i] = []
    pe_bank[i] = []


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nifty',methods=['GET', 'POST'])
def nifty():
    return render_template('nifty.html')

@app.route('/bankNifty',methods=['GET', 'POST'])
def bankNifty():
    return render_template('bankNifty.html')

@app.route('/getNiftyData',methods=['GET', 'POST'])
def niftyData():
    global start_nifty
    while True :
        try :
            new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(new_url,headers=headers)
            k = json.loads(page.text)
            start_nifty += 1  
            for i in k['records']['data'] :
                if i['expiryDate'] == date and i['strikePrice'] in ce_nifty and i['strikePrice'] in pe_nifty:
                    c1 = i['CE']['changeinOpenInterest']*50/100000
                    p1 = i['PE']['changeinOpenInterest']*50/100000
                    ce_nifty[i['strikePrice']].append(round(c1,2))
                    pe_nifty[i['strikePrice']].append(round(p1,2))
            time_count_nifty.append(start_nifty)
            return_dict = {}
            return_dict['CE'] = ce_nifty
            return_dict['PE'] = pe_nifty
            return_dict['Time'] = time_count_nifty
            return_json = json.dumps(return_dict)
            return return_json
        except :
            time.sleep(2)

@app.route('/getBankNiftyData',methods=['GET', 'POST'])
def bankNiftyData():
    global start_bank
    while True :
        try :
            new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(new_url,headers=headers)
            k = json.loads(page.text)
            start_bank += 1  
            for i in k['records']['data'] :
                if i['expiryDate'] == date and i['strikePrice'] in ce_bank and i['strikePrice'] in pe_bank:
                    c1 = i['CE']['changeinOpenInterest']*25/100000
                    p1 = i['PE']['changeinOpenInterest']*25/100000
                    ce_bank[i['strikePrice']].append(round(c1,2))
                    pe_bank[i['strikePrice']].append(round(p1,2))
            time_count_bank.append(start_bank)
            return_dict = {}
            return_dict['CE'] = ce_bank
            return_dict['PE'] = pe_bank
            return_dict['Time'] = time_count_bank
            return_json = json.dumps(return_dict)
            return return_json
        except :
            time.sleep(2)

app.run(debug=True, port=8039)

