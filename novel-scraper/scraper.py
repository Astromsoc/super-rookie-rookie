# script to scrape text data from the website

import os
import yaml
import requests
import argparse

from tqdm import tqdm
from bs4 import BeautifulSoup


def retriever(url):
    """
    Retrieve the url and return a soup object
        Inputs:
            url: (str) the url to retrieve
        Returns:
            soup: (bs4.BeautifulSoup) the soup object of retrieved url
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def web_parser(
        soup, args
    ):
    """
    Parse the url and return the text
        Inputs:
            soup: (bs4.BeautifulSoup) the soup object of retrieved url
        Returns:
            text: (str) the target text
    """
    result = soup.find(
        "div",
        {
            args['key']: args['val']
        }
    )
    return result.get_text().strip() if result is not None else ''


def main(args):

    configs = yaml.safe_load(open(args.config_file))

    url = configs['GLOBAL']['url']
    start = configs['GLOBAL']['start']
    pages = configs['GLOBAL']['pages']

     # check output validity
    if os.path.exists(configs['OUT']):
        print(f"Output file [{configs['OUT']}] already exists. Suffix added.")
        out_path = configs['OUT'].replace('.txt',  '_new.txt')
    else:
        out_path = configs['OUT']


    # scrape all the target texts
    full_results = list()
    for pg in tqdm(range(start, start + pages + 1)):
        full_results.append(
            web_parser(
                retriever(
                    url.format(pg)), 
                    configs['WEB']
            )
        )
        print(type(full_results[-1]))
    
    # write to file
    with open(out_path, 'w') as f:
        f.write('\n'.join(full_results))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config_file',
        type=str,
        help='path to config file',
    )

    parser.add_argument(
        '--output_file',
        type=str,
        help='path to output file'
    )

    args = parser.parse_args()
    if not os.path.exists(args.config_file):
        raise FileNotFoundError(f'Config file [{args.config_file}] not found.')
    
    main(args)