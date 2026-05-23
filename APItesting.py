import requests

response = requests.get("https://randomfox.ca/floof/")
x = response.json()
if response.status_code == 200:
    print(
        f"Success! You have successfully retrieved the data: {x}")

print(x["link"])
