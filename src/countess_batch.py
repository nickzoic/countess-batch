import csv
from collections import defaultdict
from configparser import ConfigParser
import importlib.resources
import argparse
import sys
import re

VERSION = '0.0.1'

def read_samplesheet_ids(filename, project=None):
    with open(filename, encoding="utf8") as fh:
        # skip the rows up to [data]
        while s := fh.readline():
            if s.lower().startswith('[data]'):
                break

        # read the remaining rows as a CSV
        for row in csv.DictReader(fh):
            if project is None or row['SampleProject'] == project:
                yield row['SampleID']

def main():
    parser = argparse.ArgumentParser(
        prog="countess_batch",
        description="A batch frontend for CountESS",
        epilog="See https://countess-project.github.io/"
    )

    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-t', '--template', help='name or filename of template')
    parser.add_argument('-s', '--sample-sheet', default='./SampleSheet.csv',
                        help='location of SampleSheet.csv (default: ./SampleSheet.csv)')
    parser.add_argument('-p', '--project',
                        help='filter project within samplesheet (default: all projects')
    parser.add_argument('-g', '--gene',
                        help='filter gene within samplesheet (default: all genes')
    parser.add_argument('-b', '--barcode-map', help='barcode map (csv)')
    parser.add_argument('-f', '--fastq', help='location of FASTQ file hierarchy')
    parser.add_argument('-o', '--output', help='output directory (default: .)', default=".")
    opts = parser.parse_args()

    if opts.template:
        if '/' in opts.template:
            with open(opts.template, encoding="utf-8") as fh:
                template = fh.read()
        else:
            template = importlib.resources.read_text('countess_batch_templates', opts.template+".ini")
    else:
        print("Must specify --template name or path.  Available template names:")
        for template in importlib.resources.files('countess_batch_templates').iterdir():
            print("* " + template.stem)
        sys.exit(1)

    config = ConfigParser()
    config.read_string(template)

    print(config)

    for sample_id in read_samplesheet_ids(opts.sample_sheet, opts.project):
        print(sample_id)

if __name__ == '__main__':
    main()
