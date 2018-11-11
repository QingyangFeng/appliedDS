import json
import re
data = [] 
r = open('topic_v2.json', 'r')
f = open('label.txt','w')
i = 0
for line in r:
    data.append(json.loads(line))
   
    if i <= 400:
       data[i]['text'] = re.sub(r'\n','',data[i]['text'])#remove \n
       print  i,u''.join(data[i]['text'],).encode("utf-8").strip()
       #f.write('\n')
    else: 
       break
    i = i+1
f.close() 
