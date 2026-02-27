#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', required=True)
parser.add_argument('--output_path', required=True)
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# construct dataset: date[hashtag][date]
data = defaultdict(lambda: defaultdict(int))

# loop over .lang file from input
all_dates = []
for file in os.listdir(args.input_folder):
    if not file.endswith('.lang'):
        continue
    dates = re.search(r'geoTwitter(\d{2}-\d{2}-\d{2})', file)
    if not dates:
        continue
    date = dates.group(1)
    all_dates.append(date)

    # load input file
    file_path = os.path.join(args.input_folder, file)
    with open(file_path) as f:
        counts = json.load(f)

    # sum counts across languages for each hashtag
    for hashtag in args.hashtags:
        if hashtag in counts:
            data[hashtag][date] = sum(counts[hashtag].values())
        else:
            data[hashtag][date] = 0

# sort list by date
all_dates = sorted(set(
    date for hashtag in data for date in data[hashtag]
))

# plot a line for each hashtag
plt.figure(figsize=(12, 6))
for hashtag in args.hashtags:
    counts = [data[hashtag].get(date, 0) for date in all_dates]
    label = 'Coronavirus in Korean' if hashtag == '#코로나바이러스' else hashtag
    plt.plot(all_dates, counts, label=label)

plt.title('Hashtag Usage Over 2020')
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.xticks(all_dates[::28], rotation=45, ha='right')  # show every 4 weeks
plt.legend()
plt.tight_layout()

plt.savefig(args.output_path)
print('saved figure to:', args.output_path)
