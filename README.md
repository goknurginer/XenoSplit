# XenoSplit
Mapping pipeline 
Author: Göknur Giner & Aaron Lun

XenoSplit is a solution to bioinformatics challenges of transcriptional profiling of patient derived xenografts (PDXs). Xenograft mouse models are known to be challenging as they suffer from the scarcity of human cells. The major challenge of working with these xenografts is the mixed human and mouse information. To classify ambiguous reads, XenoSplit compares human mapping scores with mouse genome mapping scores. First, reads were mapped to human and mouse genomes seperately. Then reads were allocated to a species based on the number of correctly aligned bases. This identifies a sufficient number of human reads to proceed with downstream analyses.

XenoSplit is a simple and effective method, which improves the accuracy and sensitivity of detecting the reads originated from the graft tissue. XenoSplit is a fast computational tool and it is freely available for non commercial use.

## XenoSplit flow chart:
![flow1](https://github.com/goknurginer/XenoSplit/blob/master/flow1.png)

## XenoSplit arguments:
![flow2](https://github.com/goknurginer/XenoSplit/blob/master/flow2.png)

## XenoSplit perfomance:
![NumMapped](https://github.com/goknurginer/XenoSplit/blob/master/NumMapped.png)

XenoSplit removes the reads which was mistakenly mapped to human. False positive reads are trimmed by using XenoSplit without comprimising true positives.
![NumMapped_Splitter](https://github.com/goknurginer/XenoSplit/blob/master/NumMapped_Splitter.png)


## How to run XenoSplit
python xenosplit.py --help

Step 1. Align your fastq files to human and mouse genome first. (human.bam and mouse.bam will be produced)
Step 2. XenoSplit your human.bam and mouse.bam files (compare those two files' mapping scores for each read)

### Using XenoSplit with Subread and Subjunc (http://subread.sourceforge.net/)
python xenosplit.py --out1 --out1 human_splitted.bam human.bam mouse.bam

### Using XenoSplit with Bowtie2
python XenoSplit_bowtie.py --out1 human_splitted.bam human.bam mouse.bam

### XenoSplit arguments
python XenoSplit.py --count human.bam mouse.bam > counts.txt

