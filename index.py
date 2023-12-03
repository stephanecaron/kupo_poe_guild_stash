from http_requests import requestsAPI
from time import sleep

truncated = True

data = requestsAPI.get_initial_fetch()

entries = data['entries']
truncated = data['truncated']
last_time = entries[-1]['time']
last_id = entries[-1]['id']

print(entries[0])
print(last_time)
print(last_id)
while truncated == True:
    data = requestsAPI.get_further_fetch(last_time,last_id)
    
    new_entries = data['entries']
    last_time = new_entries[-1]['time']
    last_id = new_entries[-1]['id']
    truncated = data['truncated']
    print(new_entries[0])
    print(truncated)
    sleep(5)