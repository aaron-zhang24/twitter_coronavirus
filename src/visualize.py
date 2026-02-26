#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

# generate top 10 item keys and values
top_ten = sorted(items[:10], key =lambda item: item[1])
labels, values = [item[0] for item in top_ten], [item[1] for item in top_ten]

# plot the top 10 keys and values
plt.figure(figsize=(12,6))
plt.bar(labels, values)
plt.title(args.key)
plt.xlabel('Language' if 'lang' in args.input_path else 'Country')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')

# save output as png
output_path = args.input_path + '.' + args.key.replace('#','') + '.png'
plt.savefig(output_path)
print('saved figure to:', output_path)
