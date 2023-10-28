import requests
import json

data = json.dumps(
    {
        "username": "admin",
        "password": "HgTQytfDB7t9qjz_aXGdYHCsQf@Dv9@m*7EbTgD_p6LFa8zRtH!7!3.izsrKr9ZT7oANcZ.4ykqLVRWGB9bAF7NhRJVjh@qzU9A.",
    }
)

response = requests.post(
    url=f"http://192.168.31.50:8080/api/login",
    data=data
)

print(json.loads(response.text).get('data'))

