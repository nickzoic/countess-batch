import csv
from collections import defaultdict
from configparser import ConfigParser
import importlib.resources
import argparse
import sys
import re
import os
from copy import deepcopy

VERSION = '0.0.1'

def read_samplesheet_ids(filename, project=None):
    genes = defaultdict(list)
    with open(filename, encoding="utf8") as fh:
        # skip the rows up to [data]
        while s := fh.readline():
            if s.lower().startswith('[data]'):
                break

        # read the remaining rows as a CSV
        for row in csv.DictReader(fh):
            if project is None or row['SampleProject'] == project:
                if m := re.match(r'(\w+)_(\w+)', row['SampleID']):
                    genes[m.group(1)].append(row['SampleID'])

    print(genes)
    return list(genes.items())


def get_configuration(template, options=None):
    if '/' in template:
        with open(template, encoding="utf-8") as fh:
            template_str = fh.read()
    else:
        template_str = importlib.resources.read_text('countess_batch_templates', f"{template}.ini")

    return ConfigParser(defaults=options).read_string(template_str)


def main():
    parser = argparse.ArgumentParser(
        prog="countess_batch",
        description="A batch frontend for CountESS",
        epilog="See https://github.com/nickzoic/countess-batch/ for more information",
    )

    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('-t', '--template',
                        help='name or filename of template')
    parser.add_argument('-s', '--sample-sheet', default='./SampleSheet.csv',
                        help='location of SampleSheet.csv (default: ./SampleSheet.csv)')
    parser.add_argument('-p', '--project',
                        help='filter project within samplesheet (default: all projects')
    parser.add_argument('-g', '--gene',
                        help='filter gene within samplesheet (default: all genes')
    parser.add_argument('-b', '--barcode-map',
                        help='filename of barcode map (csv)')
    parser.add_argument('-f', '--fastq',
                        help='location of FASTQ file hierarchy')
    parser.add_argument('-x', '--option', action='append',
                        help='options to pass to template')
    parser.add_argument('-o', '--output', default=".",
                        help='output directory for .ini files (default: .)')
    opts = parser.parse_args()

    options = {}
    for opt in opts.option or []:
        if m := re.match(r'([\w_]+)=(.*)', opt):
            options[m.group(1)] = m.group(2)
        else:
            options[opt] = True

    if opts.template:
        config = get_configuration(opts.template, options)
    else:
        print("Must specify --template name or path.  Available template names:")
        for template in importlib.resources.files('countess_batch_templates').iterdir():
            print("* " + template.stem)
        sys.exit(1)

    for gene, samplesheet_ids in read_samplesheet_ids(opts.sample_sheet, opts.project):
        if opts.gene is None or gene == opts.gene:
            print(f"Writing config for {gene}")
            gene_config = deepcopy(config)

            for num, sample_id in enumerate(samplesheet_ids):
                gene_config['fastq_load'][f'files.{num}.filename'] = os.path.join(opts.fastq, sample_id + '.fastq*')
            gene_config['barcode_load']['files.0.filename'] = opts.barcode_map
            gene_config['score_save']['filename'] = os.path.join(opts.output, f"countess_{gene}_scores.csv.gz")

            with open(f"countess_{gene}.ini", "w", encoding='utf-8') as fh:
                gene_config.write(fh)

if __name__ == '__main__':
    main()
