import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzNjYyMjQxLCJpYXQiOjE2NTM2NjE5NDEsImp0aSI6ImY2MTkxYWJjYjA3YTQyOWQ4MTI5Yjc2ZDMzMzM0YTBkIiwidXNlcl9pZCI6MX0.Xo1ZVk6sfgNwSbkUdG2T1x446FiVHiG-9hOndy2rQCQ'

r = requests.get('http://127.0.0.1:7000/projects/', headers=headers)

print(r.text)