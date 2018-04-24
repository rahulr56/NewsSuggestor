import requests

url = "https://github.com/rahulr56/NewsSuggestor/blob/master/sample.json"

response = requests.get(url)
print(response.json())
