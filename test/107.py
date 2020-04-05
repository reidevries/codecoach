#!/usr/bin/env python
import json
import operator


def print_stats(name):
    data = json.load(open("results/{0}.json".format(name)))
    num_recs = []
    product_recs = []
    ids = []
    ranks = []
    product_dict = {}

    for item in data:
        num_recs.append(item['num_recommendations'])
        for rec in item['recommendations']:
            product_recs.append(rec['product_id'])
            ranks.append(rec['rank'])
            ids.append(rec['id'])
            if rec['product_id'] in product_dict:
                product_dict[rec['product_id']]['occurrences'] += 1
            else:
                product_dict[rec['product_id']] = {
                    "title": rec['title'],
                    "occurrences": 1
                }

    sorted_product_dict = sorted(product_dict.iteritems(),
        key=operator.itemgetter(1), reverse=True)

    print "-----------------------"
    print "{0} stats".format(name).upper()
    print "-----------------------"
    print
    print "Min Recommendations:\t", 0
    print "Max Recommendations:\t", sorted(ranks)[-1]
    print "Avg Recommendations:\t", sum(num_recs) / float(len(num_recs))
    print "Unique Products:\t\t", len(product_dict)
    print "Unique Identifiers:\t\t", ', '.join(set(ids))
    print
    print "Top 25 recommended products by freq:"
    for x in sorted_product_dict[0:25]:
        print x[1]['occurrences'], "\t", x[0], "\t", x[1]['title']
    print

print_stats("control")
print_stats("variant")
