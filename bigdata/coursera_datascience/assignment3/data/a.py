import json

x = open('books.json')
for i in x:
    y = json.loads(i)
    print y[0]
