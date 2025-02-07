import importlib.resources
import glob
import countess_batch.templates

VERSION = '0.0.1'

def main():
    print("Available templates:")

    for template in importlib.resources.files(countess_batch.templates).iterdir():
        if template.suffix == '.ini':
            print("* " + template.stem)
