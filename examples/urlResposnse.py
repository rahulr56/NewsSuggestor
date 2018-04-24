import json
import requests

url = "https://raw.githubusercontent.com/rahulr56/NewsSuggestor/master/examples/sample.json"


def getResponse():
    response = requests.get(url)
    # print (response)
    return response.json()

def parseJson():
    jsonData = json.loads(json.dumps(getResponse()))
    print ("JSON DATA RECEIVED is :\n"+str(jsonData))
    print ("\njsonData['a'] : " + jsonData['a'])
    print ("jsonData['b'] : " + str(jsonData['b']))
    print ("jsonData['c'] : " + str(jsonData['c']))
    print ("jsonData['c'][0] : " + str(jsonData['c'][0]))
    print ("jsonData['c'][1] : " + str(jsonData['c'][1]))
    print ("jsonData['c'][2] : " + str(jsonData['c'][2]))
    print ("jsonData['c'][3] : " + str(jsonData['c'][3]))
    print ("jsonData['d'] : " + str(jsonData['d']))
    print ("jsonData['d']['aa'] : " + str(jsonData['d']['aa']))
    print ("jsonData['d']['aa'] : " + str(jsonData['d']['cc']))


if "__main__" == __name__:
    parseJson()
