# CountESS Batch Processor

A utility to generate [CountESS](https://countess-project.github.io/CounteSS/)
configuration file(s) directly from an Illumina sample sheet.

## Installing

`pip install countess-batch`

## Preprocessing

* First use `bcl2fastq` to generate many fastq files.
* Then use `pear` or `flash2` or `ngmerge` or similar to merge paired end reads

**XXX These could be run from countess-batch as well, I suppose?**

## Inputs

* `SampleSheet.csv` from which we extract gene/library/replicate/bin
* Already paired FASTQ files in a directory, with a certain structure.
* Barcode variant map *OR* Barcode sequence map and target sequence.

Input directories are never written to.

## Outputs

One or more .ini files which can be run with `countess_cmd`.

These files are already customized with the appropriate file
locations derived from the Sample Sheet and the command line 
options.

## Running

Running:

`countess_batch --template vampseq --sample-sheet SampleSheet.csv --barcode-map barcode_map.csv.gz --fastq fastq_directory/ --output output_directory/`

## Queueing Jobs

**XXX maybe add a --qsub option to automatically queue the `countess_cmd $XXX.ini`**

