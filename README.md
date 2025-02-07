# CountESS Batch Frontend

A utility to generate [CountESS](https://countess-project.github.io/CounteSS/)
configuration file(s) directly from an Illumina sample sheet.

## Installing

`pip install countess-batch`

## Preprocessing

You'll need to install these separately as they have 
licenses which prevent them being bundled into this package.

* First use `bcl2fastq` to generate many fastq files.
  It will put these into a directory structure compatible with
  countess-batch.
* Then use `pear` or `flash2` or `ngmerge` or similar to merge paired end reads

**XXX Need explicit instructions about file layout.**

**XXX These could be run from countess-batch as well, I suppose?**

## Inputs

* `SampleSheet.csv` from which we extract gene/library/replicate/bin
* Already paired FASTQ files in a directory, with a certain structure
  (see instructions above)
* Barcode variant map *OR* Barcode sequence map and target sequence.

Input directories are never written to or deleted from!

## Running

Running:

`countess_batch --template vampseq --sample-sheet SampleSheet.csv --barcode-map barcode_map.csv.gz --fastq fastq_directory/ --output output_directory/`

## Outputs

One or more .ini files which then can be run with `countess_cmd`.

These files are already customized with the appropriate file
locations derived from the Sample Sheet and the command line 
options, so all you have to do is run them with

`countess_cmd countess_$GENE.ini`

## Queueing Jobs

`qsub countess_cmd countess_$GENE.ini`

**XXX maybe add a `--qsub` option to automatically queue the `countess_cmd`**

## Results

Results are written as `output_directory/scores_$GENE_R$REPLICATE.csv.gz` etc.
