"""

This file would scrape data from reddit via the praw api.

"""

import json
import requests
import time
import os
import sys

def get_pushshift_data(after, before, sub):
    url = f'https://api.pushshift.io/reddit/search/submission/?&size=1000&after={after}&before={before}&subreddit={sub}'

    try:
        r = requests.get(url, timeout=5)
        data = json.loads(r.text)
        return data['data']
    except Exception as e:
        print(f"Error: {e}")
        return None

def main(subreddit_name, base):

    start = 1223305736
    end = 1682630862
    bucket = 250000
    data = []
    n = 0
    total_filesize = 0
    dir = f"data_{subreddit_name}/"

    try:
        os.makedirs(base, exist_ok=True)
        os.chdir(base)
        os.makedirs(dir, exist_ok=True)
    except Exception as e:
        print(f"Error: {e}")
        return

    for i in reversed(range(start, end, bucket)):
        temp_data = get_pushshift_data(i, i + bucket, subreddit_name)
        if temp_data is not None:
            data.extend(temp_data)

        if len(data) > 10000:
            filename = f"{dir}data_{n}.json"
            with open(filename, 'w') as f:
                json.dump(data, f)

            with open(f"{dir}metadata.txt", 'a') as f:
                f.write(f"File: {filename}, {i}, {start}\n")

            file_size = os.path.getsize(filename) / 1000000
            total_filesize += file_size
            print(f"Added file {filename} of size {file_size} MB, with length: {len(data)}")
            print(f"Total data processed: {total_filesize} MB")
            data = []
            
            n += 1

        time.sleep(0.2)
        print(len(data))

    print(len(data), type(data))

if __name__ == "__main__":
    try:
        reddit_name, base = sys.argv[1:3]
        print(f"Scraping the {reddit_name} subreddit into {base}")
        main(reddit_name, base)
    except IndexError:
        print("Usage: python script.py <reddit_name> <base_directory>")
