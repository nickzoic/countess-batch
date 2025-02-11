# CountESS Batch Frontend

A utility to generate [CountESS](https://countess-project.github.io/CounteSS/)
configuration file(s) directly from an Illumina sample sheet.

CountESS allows for flexible, exploratory processing of data but it is not
necessarily a very efficient interface for processing hundreds of separate genes
in parallel.  This frontend allows a user to generate a batch of CountESS
configuration files from a Sample Sheet and a CountESS configuration template,
and these configurations can then be processed efficiently in parallel.

## Installing

`pip install countess-batch`

This will install a command line utility `countess_batch` and bring in `countess` as well.
You can run this within a virtual environment such as `venv` or in conda if you'd prefer.

*TODO: Add venv install instructions.*

*TODO: Add conda install instructions.*

## Preprocessing

You'll need to install these programs separately as they have 
licenses which prevent them being bundled into this package.

* First use `bcl2fastq` to process your Illumina files and generate many fastq files.
  It will put these into a directory structure compatible with countess-batch.
* Then use `pear` or `flash2` or `ngmerge` or similar to merge paired end reads

*TODO: Add bcl2fastq install and run instructions.*

*TODO: Add pear install and run instructions.*

*TODO: Add flash2 install and run instructions.*

*TODO: Add ngmerge install and run instructions.*

Current commands:

`bcl2fastq -R ${rundirectory} -o ./bcl2fastq_output/ --sample-sheet ./${samplesheet} --no-lane-splitting -p 6 -r 1 -w 1 --minimum-trimmed-read-length 10 --mask-short-adapter-reads 10`

`pear -f ./bcl2fastq_output/${FOLDER}/${SAMPLE}_R1_001.fastq.gz -r ./bcl2fastq_output/${FOLDER}/${SAMPLE}_R2_001.fastq.gz -o ./pear_output/${FOLDER}/${SAMPLE}/${SAMPLE} -q 30 -j 8 -n 10`

## Inputs

countess-batch itself reads the following files:

* `SampleSheet.csv` from which we extract project/gene/library/replicate/bin names.

*TODO: We might not need this at all, or we might need it to select which 
files to actually read (although there is a `--gene` filter)

* Already paired FASTQ files in a directory, with a certain naming scheme
  (see instructions above)
* Barcode variant map as a two-column CSV file mapping barcode to variant.

*TODO: Document expected FASTQ file naming scheme.*

`pear_output/$GENE/L${LIB}_R${REP}_B${BIN}_*/L${LIB}_R${REP}_B${BIN}_*.assembled.fastq`

NOTE: These files and directories are never written to or deleted by countess-batch!
The only files written by countess-batch are written to the output directory.

## Templates

countess-batch uses a "template" to generate the new CountESS configuration file(s).
Selected templates are included in countess-batch, or can be provided as a regular file.
At the moment, the only included template is called "vampseq". 

## Running

Running:

`countess_batch --template vampseq --sample-sheet SampleSheet.csv --barcode-map barcode_map.csv.gz --fastq fastq_directory/ --output output_directory/`

For short help on command line options:

`countess_batch --help`

## Outputs

One or more .ini files, one per project per gene, which then can be run with `countess_cmd`.

These files are already customized with the appropriate file
locations derived from the Sample Sheet and the command line 
options, so all you have to do is run them with

`countess_cmd countess_$GENE.ini`

... or queue them up with

`qsub countess_cmd countess_$GENE.ini`

## Results

When CountESS is run, results are written as `$OUTPUT/countess_$PROJECT_$GENE_scores.csv.gz`
with the following columns:

* Variant
* Score per replicate
* Mean Score
* Score Variance

Intermediate results will also be written as `$OUTPUT/countess_$PROJECT_$GENE_counts.csv.gz`
for cross-checking purposes, with the following columns:

* Variant
* Replicate
* Count per bin
* Score
