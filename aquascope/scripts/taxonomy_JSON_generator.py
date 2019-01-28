import csv
import fire
import json
import pandas as pd
from aquascope.util.taxonomy_dictionary_utils import add


def generate(in_file_name, out_file_name=None):
    taxonomy = {}

    df = pd.read_csv(in_file_name)

    for _, data in df[['empire', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']].iterrows():
        add(taxonomy, data.tolist())

    taxonomy_json = json.dumps(taxonomy, sort_keys=True, indent=4, separators=(',', ': '))
    if out_file_name:
        with open(out_file_name, 'w') as outfile:
            outfile.write(taxonomy_json)
    else:
        # if no output file specified produce result to stdout
        print(taxonomy_json)


if __name__ == '__main__':
    fire.Fire(generate)
