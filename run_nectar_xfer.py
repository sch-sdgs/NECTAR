from nectar import nectar_class
import argparse
import os
from producers.StarLims import StarLimsApi

import ConfigParser

dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    parser = argparse.ArgumentParser(description='Transfers nectar data to sitran')
    parser.add_argument('--config_file', metavar='coverage', type=str, help='config file')
    args = parser.parse_args()

    configP = ConfigParser.ConfigParser()
    configP.readfp(open(args.config_file))

    query = configP.get('nectar config', 'query')

    s = StarLimsApi.get_nectar_project(query)
    n = nectar_class.nectar(args.config_file)

    for patient in s:
        if not n.is_done(patient["CONTAINERID"]):


if __name__ == '__main__':
    main()
