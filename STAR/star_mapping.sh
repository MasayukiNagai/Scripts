#!/bin/bash

NUM_THREADS=8
INDEX='/home/data/genome/STARIndex'
REFERENCE_FASTA='/home/data/genome/reference.fa'
ANNOTATION='/home/data/genome/genes.gtf'
INDIR='/home/data/input'
OUTIDR='/home/data/output'
sample='sample'

STAR \
  --runThreadN ${NUM_THREADS} \ # Number of threads to be used
  --genomeDir ${INDEX} \  # Path to the dir where the genome indices are stored
  --readFilesIn ${INDIR}/${sample}_1.fastq ${INDIR}/${sample}_2.fastq \ # input files
  --sjdbGTFfile ${ANNOTATION} \  # path to the file with annotated transcripts in the standard GTF format
  --outSAMtype BAM SortedByCoordinate \  # output unsorted Aligned.out.bam file
  --outFileNamePrefix ${OUTDIR}/${sample}  # prefix for output files
