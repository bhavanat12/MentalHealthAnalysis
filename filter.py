"""

This file will load all the scraped data, and reduce it into a single spark file containing only selftext and subreddit attributes

The data exists in the following directory structure:

data/
    data_SUBREDDIT_NAME_1/
        metadata.json
        data_0.json
        data_1.json
        data_2.json
        ...
        data_n.json
    data_SUBREDDIT_NAME_2/
        metadata.json
        data_0.json
        data_1.json
        data_2.json
        ...
        data_n.json
    data_SUBREDDIT_NAME_3/
        metadata.json
        data_0.json
        data_1.json
        data_2.json
        ...
        data_n.json
    ...


"""

import sys
import json
import os
from tqdm import tqdm

def cleanup(text):
    # Simplify cleanup using translate and str.maketrans
    translation_table = str.maketrans("", "", "\n'\"\\\t\r,")
    return text.translate(translation_table)

def get_data_paths(data_folder):
    # Use list comprehension for a more concise code
    return [os.path.join(subdir, file) for subdir, dirs, files in os.walk(data_folder) for file in files if file.endswith('.json')]

def main(data_folder, new_data_folder):
    try:
        # Use exist_ok parameter to avoid the need for a separate try-except block
        os.makedirs(new_data_folder, exist_ok=True)
    except OSError as e:
        print(f"ERROR CREATING NEW DIRECTORY AT {new_data_folder}, returning ...")
        return

    total_data_list_txt = []

    print("FILTERING THE DATA .....")
    for filename in tqdm(get_data_paths(data_folder)):
        with open(filename, 'r') as file_temp:
            data_json_temp = json.load(file_temp)
            data_json_temp = [f"{el['subreddit']}, {cleanup(el['selftext'])}, {el['created_utc']}\n" for el in data_json_temp]
            total_data_list_txt.extend(data_json_temp)

    print(f"LENGTH: {len(total_data_list_txt)}, needs to be > 75k")

    # Use 'with' statement to automatically close the file
    with open(os.path.join(new_data_folder, "filtered_data.txt"), 'w') as fout:
        print("WRITING TO FILE")
        for el in tqdm(total_data_list_txt):
            fout.write(el)

if __name__ == "__main__":
    # Use unpacking for better readability
    data_folder, new_data_folder = sys.argv[1:3]
    print(f"Original data folder: {data_folder}, new data folder: {new_data_folder}")
    main(data_folder, new_data_folder)
