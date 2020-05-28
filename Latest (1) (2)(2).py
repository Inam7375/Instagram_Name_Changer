#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import threading
import time
import random
import re
from urllib.parse import urlencode
import Proxy

targets = []
# deal with config.json
with open("config.json") as file:
    config = json.load(file)

with open("list.txt", "r") as file:
    targets = file.read().splitlines() 

#proxies = []
#with open('proxies.txt',this  'r', encoding='utf-8') as px:
#    while True:
#        l=px.readline()
#        if l=='':
#            break
#        proxies.append('http://'+l.strip('\n'))

email = config['email']
username = config['username']#input("Enter Username : ")
password = config['password']#input("Enter Password : ")
list_of_ua = config.get("list_of_ua")
#targets = config['targetUsernames']
user_agent = random.sample(list_of_ua, 1)[0]
checkAvailable = False
successfullyChanged = False


#def getRandomProxy():
#        proxy = random.choice(proxies)
#        proxy_dict = {
#               'http':proxy
#            }
#        return proxy_dict



def checkUsername(targetUsername, s, successfulLogin, username):
    #global stop_threads
    #start monitoring the username    
    #while not stop_threads:
    #while True:
    try:
        global checkAvailable
        global successfullyChanged
        #global proxy
        usernameURL = 'https://www.instagram.com/web/search/topsearch/?'+ urlencode({
            'context':'blended', 'query':targetUsername, 'rank_token':'0.395359231827089', 'count':'1'
            })
        try:
            #res = requests.get(usernameURL, timeout=20)
            ip = Proxy.returned_proxies()
            res = requests.get(usernameURL, proxies=ip, timeout=20)
        except requests.exceptions.Timeout:
            print('[{0}] is not available'.format(targetUsername))
            #proxy=getRandomProxy()
            return None            
        
        #time.sleep(1)
        if res.status_code == 200:
            #print(res.text)
            try:
                json_data = json.loads(res.text)
                #print(json_data)
                if len(json_data['users']) == 0 and len(json_data['places']) == 0:
                    checkAvailable = True
                    print('[{0}] is available!!!'.format(targetUsername))
                    #changeUsername(targetUsername)
                    #print('[{0}] Completed Turbo Killing Thread'.format(targetUsername))
                    #time.sleep(5)
                    #system.exit()
                    availableUsername = targetUsername
                    if successfulLogin:
                        #r = s.get("https://www.instagram.com/")
                        #csrftoken = re.search('(?<="csrf_token":")\w+', r.text).group(0)
                        #s.cookies["csrftoken"] = csrftoken
                        #s.headers.update({"X-CSRFToken": csrftoken})
                        #finder = r.text.find(username)
                        #if finder != -1:
                        url_edit = "https://www.instagram.com/accounts/edit/"
                        #r = s.get("https://www.instagram.com/")
                        #csrftoken = re.search('(?<="csrf_token":")\w+', r.text).group(0)
                        #s.cookies["csrftoken"] = csrftoken
                        #s.headers.update({"X-CSRFToken": csrftoken})
                        formData = {
                            'first_name': 'Vnes',
                            'email': email,
                            'username': availableUsername,
                            'phone_number':'',
                            'biography':'',
                            'external_url':'',
                            'chaining_enabled': 'on'
                            }
                       # print(availableUsername)
                        rf = s.post(url_edit, data=formData)
                        print(rf.text)
                        with open('Found_Names.txt', 'a') as f:
                            f.write(targetUsername+'\n')
                        with open("config.json") as file:
                                update = json.load(file)
                                update['username'] = availableUsername
                                username = availableUsername
                                with open('config.json', 'w') as f:
                                    json.dump(update, f)
                        successfullyChanged = True
                        print('Successfully Changed the Username.')
                    else:
                        checkAvailable = False
                        print("Login error! Connection error!")
                else:
                    print('[{0}] is not available'.format(targetUsername))
            except:
                print('[{0}] is not available'.format(targetUsername))
                #proxy=getRandomProxy()
    except: pass

def changeUsername():
    try:
        global username
        global checkAvailable
        s = requests.Session()
        #s.proxies = getRandomProxy()
        s.headers.update({
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Host": "www.instagram.com",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/",
            "User-Agent": user_agent,
            "X-Instagram-AJAX": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
        })
        #print(username, password, email)
        login_post = {
            "username": username, #change from username to email.
            "password": password,
        }
        r = s.get('https://www.instagram.com/')
        csrf_token = re.search('(?<="csrf_token":")\w+', r.text).group(0)
        s.headers.update({"X-CSRFToken": csrf_token})
        time.sleep(2 * random.random())

        url_login = "https://www.instagram.com/accounts/login/ajax/"
        login = s.post(url_login, data=login_post, allow_redirects=True)

        if login.status_code not in (200, 400):
            print("[{0}] Login failed!".format(username))
            print("Response Status: {login.status_code}")
        else:
            loginResponse = login.json()
            #print(loginResponse)
            csrftoken = login.cookies["csrftoken"]
            s.headers.update({"X-CSRFToken": csrftoken})

            if loginResponse.get("errors"):
                print("Something is wrong with Instagram! Please try again later...")
                print(loginResponse["errors"]["error"])
            elif loginResponse.get("message") == "checkpoint_required":
                print('[{0}] checkpoint required!'.format(username))
            elif loginResponse.get("authenticated") is False:
                print("Login error! Check your login data!")
                return
            else:
                rollout_hash = re.search('(?<="rollout_hash":")\w+', r.text).group(0)
                s.headers.update({"X-Instagram-AJAX": rollout_hash})
                successfulLogin = True
                # ig_vw=1536; ig_pr=1.25; ig_vh=772;  ig_or=landscape-primary;
                s.cookies["csrftoken"] = csrftoken
                s.cookies["ig_vw"] = "1536"
                s.cookies["ig_pr"] = "1.25"
                s.cookies["ig_vh"] = "772"
                s.cookies["ig_or"] = "landscape-primary"
                print("[{0}] Login succeeded!".format(username))
                #time.sleep(2 * random.random())

                tin = input("Would you like to start (y/n)?: ")
                if tin.lower() == "y":
                    while True:
                        for x in targets:
                            #name = targets[x]
                            #checkUsername(name)
                            #x += 1
                            t = threading.Thread(target=checkUsername, args=(x, s, successfulLogin, username), daemon=True)
                            time.sleep(0.01)
                            t.start()
                            if checkAvailable:
                                t.join()
                                break
                        if successfullyChanged:
                            break
                else:
                    exit()
                   #else:
                   # print("Login error! Check your login data!")
    except:
        print('ERROR')

               


if __name__ == '__main__':
    print("Instagram Username Taker")
    print("=" * 60)
    print("Username: {}".format(username))
    print("Password: {}".format("*" * len(password)))
    print("# Of Targets: {}".format(str(len(targets))))
    #print(f"Endpoint: {endpoint}")
    print("=" * 60)
    print("")
    #print(targets)
    #stop_threads = False
    changeUsername()


# In[ ]:




