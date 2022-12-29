import json

news = {'type': "python",
        'mpname': "小明",
        'mpdata':{'account': "btcquant"}
       }
print (news);
print (type(news))

json_encode = json.dumps(news)
print (json_encode)
print (type(json_encode))

json_decode = json.loads(json_encode)
print (json_decode)
print (type(json_decode))
