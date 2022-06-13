import json

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["search_db"]
sites_collection = db['sites']
categorised_collection = db['categorised_collection']

with open("rated_results.json", "r", encoding='utf8') as read_file:
    data = json.load(read_file)

results = {}
'''
'category_number': category['Number'], 'rate': total_avg,'site_name': i.get('name'),
                     'full_name':i.get('full_name'), 'tax_number': i.get('tax_number'),
                     'url': i.get('url'), 'sites': i.get('_id')
'''
for d in data:
    if d['_id'] in results:
        results[d['_id']]['category_number'].append(d['category_number'])
        results[d['_id']]['rates'].append(d['rate'])
        continue
    results[d['_id']] = {'category_number': [d['category_number']], 'rates': [d['rate']], 'site_name': d['site_name'],
                      'full_name': d['full_name'], 'tax_number': d['tax_number'], 'url': d['url'], '_id': d['_id']}

results = [i[1] for i in results.items()]
print(results)
categorised_collection.insert_many(results)
