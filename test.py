import requests
import base64
import io
import model

url='http://127.0.0.1:5000/'
token='934004e56569586e62708a4b2fa3a783168c2b29'

def uploadfile():
    filename='1.png'

    with open(filename,'rb') as f:
        data = f.read()
        print(data)
        data=base64.b64encode(data)

        payload = {'token': token, 'data': str(data,'utf-8'),'name':'test2','public':True}
        req = requests.post(url + 'app/user/upload',json=payload)
        print(req.text)

def getfile():
    id = '5a19038fdee17116885cacc2'
    payload={'token':token,'fid':id}
    req = requests.get(url + 'app/user/getfile', json=payload)
    print(req.text)

def modifyfile():
    id = '5a19038fdee17116885cacc2'
    payload={'token':token,'fid':id,'name':'我是sb','delete':True}
    req = requests.post(url + 'app/user/modifyfile', json=payload)
    print(req.json())

def getownfilelist():
    payload = {'token': token}
    req = requests.get(url + 'app/user/getownfilelist', json=payload)
    print(req.json())

def favorite():
    payload = {'token': token,'fid':'5a191880dee17128b40f91fd'}
    req = requests.post(url + 'app/user/favorite', json=payload)
    print(req.json())

#uploadfile()
#getfile()
#modifyfile()
#getownfilelist()
favorite()