#!/bin/bash

NUM_THREADS=8
GENOME_DIR='/home/data/genome/STARIndex/'
REFERENCE_FASTA='/home/data/genome/reference.fa'
ANNOTATION='/home/data/genome/genes.gtf'

STAR \
  --runThreadN ${NUM_THREADS} \ # Number of threads to be used
  --runMode genomeGenerate \
  --genomeDir ${GENOME_DIR} \
  --genomeFastaFiles ${REFERENCE_FASTA} \ # One or more FASTA files with the genome ref seq
  --sjdbGTFfile ${ANNOTATION} \  # path to the file with annotated transcripts in the standard GTF format
#  --limitGenomeGenerateRAM
#  --sjdbOverhang
