import requests
import time
import json
print(time.asctime( time.localtime(time.time()) ))
key = "清华大学"

url  = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A'+key+'&wt=json&rows=10000&indent=true&&fl=PntData_tags%2CEntity_pers%2CEntity_orgs%2COWord_neg%2CDataS_p_location%2COpinion%2COWord_pos%2CDate'
print(time.asctime( time.localtime(time.time()) ))
r = requests.get(url,verify=False)
print(time.asctime( time.localtime(time.time()) ))

r = r.json()["response"]["docs"]
print(time.asctime( time.localtime(time.time()) ))
