import csv
import importlib.resources
import sys

VERSION = '0.0.1'

def read_samplesheet(filename):
    with open(filename, encoding="utf8") as fh:
        # skip the rows up to [data]
        while s := fh.readline():
            if s.lower().startswith('[data]'):
                break
        # read the remaining rows as a CSV
        reader = csv.DictReader(fh)
        for row in reader:
            yield row

def main():
    print("Available templates!")

    for template in importlib.resources.files('countess_batch.templates').iterdir():
        if template.suffix == '.ini':
            print("* " + template.stem)

    print(list(read_samplesheet(sys.argv[1])))

if __name__ == '__main__':
    main()
