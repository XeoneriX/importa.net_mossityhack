import json

import gensim
import nltk
import numpy as np
import pymongo
from nltk.tokenize import word_tokenize, sent_tokenize

# save your model as


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["search_db"]
sites_collection = db['sites']

nltk.download('punkt')

with open('list_category.json', encoding='utf8') as f:
    categories = json.load(f)

collection_dict = []  # list[dict{category_num, name, url, rate}]

with open('final_results', 'w', encoding='utf8') as file:
    for category in categories:
        if category['CategoryName'] == '':
            continue
        print(category['CategoryName'], category['Number'])
        file_docs = sent_tokenize(category['CategoryName'], 'russian')
        gen_docs = [[w.lower() for w in word_tokenize(text)] for text in file_docs]
        dictionary = gensim.corpora.Dictionary(gen_docs)
        # with open('file-name', 'wb') as f:
        #     dill.dump(dictionary, f)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
        tf_idf = gensim.models.TfidfModel(corpus)
        sims = gensim.similarities.Similarity('.', tf_idf[corpus],
                                              num_features=len(dictionary))
        for i in sites_collection.find({"$text": {"$search": category['CategoryName']}}):
            avg_sims = []
            tokens = sent_tokenize(i.get('meta_data'))
            for line in tokens:
                query_doc = [w.lower() for w in word_tokenize(line)]
                query_doc_bow = dictionary.doc2bow(query_doc)
                query_doc_tf_idf = tf_idf[query_doc_bow]
                sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
                avg = sum_of_sims / len(file_docs)
                avg_sims.append(avg)
            total_avg = np.sum(avg_sims, dtype=np.float32)
            if total_avg != 0:
                entry = {'category_number': category['Number'], 'rate': float(total_avg),
                         'site_name': str(i.get('name')),
                         'full_name': str(i.get('full_name')), 'tax_number': str(i.get('tax_number')),
                         'url': str(i.get('url')), '_id': str(i.get('_id'))}
                collection_dict.append(entry)
                file.write(str(entry) + '\n')

with open('rated_results.json', 'w', encoding='utf8') as json_file:
    json.dump(collection_dict, json_file, indent=4, ensure_ascii=False)
