import requests

url = "https://raw.githubusercontent.com/rahulr56/NewsSuggestor/master/examples/sample.json"

response = requests.get(url)
# print (response)
print(response.json())
