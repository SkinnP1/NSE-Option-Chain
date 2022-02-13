from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from flask import Flask, render_template
import requests
import json
import numpy

ce_nifty = {}
pe_nifty = {}

ce_bank = {}
pe_bank = {}

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
    while True:
        try :
            driver = webdriver.Chrome("./chromedriver")
            url = "https://www.moneycontrol.com/indices/fno/view-option-chain/NIFTY/2022-02-17"
            driver.minimize_window()
            driver.get(url)
            rows = driver.find_elements_by_tag_name("tr")
            rows.pop(0)
            rows.pop(0)
            for i in rows :
                cells = i.find_elements_by_tag_name("td")
                strike = int(float(cells[5].get_attribute("innerHTML")))
                c = cells[1].get_attribute("innerHTML").strip()
                p = cells[-2].get_attribute("innerHTML").strip()
                if c == "-":
                    call_change = 0
                else :
                    call_change = int("".join(c.split(",")))

                if p == "-":
                    put_change = 0
                else :
                    put_change = int("".join(p.split(",")))
                
                
                if strike in ce_nifty : 
                    ce_nifty[strike].append(call_change/100000)
                    pe_nifty[strike].append(put_change/100000)
            
            return_dict = {}
            return_dict['CE'] = ce_nifty
            return_dict['PE'] = pe_nifty
            return_json = json.dumps(return_dict)
            driver.close()
            return return_json
        except :
            driver.close() 
            time.sleep(5)
        

@app.route('/getBankNiftyData',methods=['GET', 'POST'])
def bankNiftyData():
    while True:
        try :
            driver = webdriver.Chrome("./chromedriver")
            url = "https://www.moneycontrol.com/indices/fno/view-option-chain/BANKNIFTY/2022-02-17"
            driver.minimize_window()
            driver.get(url)
            rows = driver.find_elements_by_tag_name("tr")
            rows.pop(0)
            rows.pop(0)
            for i in rows :
                cells = i.find_elements_by_tag_name("td")
                strike = int(float(cells[5].get_attribute("innerHTML")))
                c = cells[1].get_attribute("innerHTML").strip()
                p = cells[-2].get_attribute("innerHTML").strip()
                if c == "-":
                    call_change = 0
                else :
                    call_change = int("".join(c.split(",")))

                if p == "-":
                    put_change = 0
                else :
                    put_change = int("".join(p.split(",")))
                
                
                if strike in ce_bank : 
                    ce_bank[strike].append(call_change/100000)
                    pe_bank[strike].append(put_change/100000)
            
            return_dict = {}
            return_dict['CE'] = ce_bank
            return_dict['PE'] = pe_bank
            return_json = json.dumps(return_dict)
            driver.close()
            return return_json
                
        except :
            driver.close() 
            time.sleep(5)

app.run(debug=True, port=8125)