# CountESS Batch Processor

A utility to generate [CountESS](https://countess-project.github.io/CounteSS/)
configuration files directly from an Illumina sample sheet.

## Installing

`pip install countess-batch`

## Preprocessing

* First use `bcl2fastq` to generate many fastq files.
* Then use `pear` or `flash2` or `ngmerge` or similar to merge paired end reads

**XXX These could be run from countess-batch as well, I suppose?**

## Inputs

* SampleSheet.csv (?)
* Paired FASTQ files in a directory
* Barcode variant map *OR* Barcode sequence map and target sequence

## Outputs

* One or more .ini files which can be run with `countess_cmd`.

## Running

Running:

`countess_batch --template vampseq --sample-sheet SampleSheet.csv --barcode-map barcode_map.csv.gz --fastq fastq_directory/ --output output_directory/`

## Queueing

**XXX maybe add a --qsub option to automatically queue the `countess_cmd $XXX.ini`**
