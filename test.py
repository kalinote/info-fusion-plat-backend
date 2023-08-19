import requests

response = requests.get(
            url="http://backend-service:8080/api/stats/overview",
            headers={
                'Authorization': '.e7WGTiAc5B76z-Q4zzUJATP0k_4ACCc-Cemx5HuqrrQ'
            }
        )

print(response.text)