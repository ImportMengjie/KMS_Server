import requests
import base64
import io
import model

url='http://127.0.0.1:5000/'
token='f29ce1facfd8ea29472721a76ac9a609099bdcb7'

def uploadfile():
    filename='1.png'

    with open(filename,'rb') as f:
        data = f.read()
        print(data)
        data=base64.b64encode(data)

        payload = {'token': token, 'data': str(data,'utf-8'),'name':'test1','public':True}
        req = requests.post(url + 'app/user/upload',json=payload)
        print(req.text)

def getfile():
    id = '5a18fc8fdee17110b5bf510a'
    payload={'token':token,'fid':id}
    req = requests.get(url + 'app/user/getfile', json=payload)
    print(req.text)

#uploadfile()
getfile()