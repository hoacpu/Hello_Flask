import requests


response = requests.get("http://localhost:5000/list_employee_json")

print (response)
output = response.content
print (output.decode('utf-8'))