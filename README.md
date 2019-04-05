# Overview
XenoSplit is a fast computational tool to detect the true origin of the graft RNA-Seq and DNA-Seq libraries prior to profiling of patient-derived xenografts (PDXs). To classify ambiguous reads from a PDX experiment, XenoSplit operates on host and graft BAM files and computes a "goodness of mapping" metric using CIGAR strings and edit distances. XenoSplit is compatible with [Subread](https://academic.oup.com/nar/article-lookup/doi/10.1093/nar/gkt214), [Bowtie2](https://www.nature.com/articles/nmeth.1923), [STAR](https://github.com/alexdobin/STAR), [Subjunc](https://academic.oup.com/nar/article-lookup/doi/10.1093/nar/gkt214), [TopHat2](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2013-14-4-r36) and [BWA](https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btp324), and is freely available under the terms of GNU General Public License v2.0. 

# Installation 
Download XenoSplit repository from GitHub in a chosen location:

    git clone https://github.com/goknurginer/XenoSplit.git

This will create a library folder called XenoSplit in the current location.

# Usage
Go into the XenoSplit folder and view the help page as below:

    python xenosplit.py --help
  
 or specify the location yourself by replacing `path` in the following code with your home directory, i.e. `user/Documents`. 
 
    python path/XenoSplit/xenosplit.py --help
 
 This will output the following help page:
 ```
 usage: xenosplit.py [-h] [--count] [--min MIN] [--out OUT]
                     [--aligner {subread,subjunc,star,tophat,bowtie,bwa}]
                     [--pairedEnd]
                     graft host

Compare two BAM files for the same reads and allocate them into new files
based on matches

positional arguments:
  graft                 graft BAM file
  host                  host BAM file

optional arguments:
  -h, --help            show this help message and exit
  --count               switch to reporting mode (default: False)
  --min MIN             minimum difference in matches for assignment to either
                        file (default: 1)
  --out OUT             graft output BAM file (default: graftOut.bam)
  --aligner {subread,subjunc,star,tophat,bowtie,bwa}
                        aligner type (default: subread)
  --pairedEnd           switch to pairedEnd mode so the mapping scores will be
                        computed using pairs (default: False)
 ```
 
 ## Important notes
 * XenoSplit requires both mapped and unmapped reads to be reported in one BAM file. Therefore, while working with [STAR](https://github.com/alexdobin/STAR) and [TopHat2](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2013-14-4-r36) the following steps should be followed:
    * **Warnings when aligning with [STAR](https://github.com/alexdobin/STAR):** STAR does not report the unmapped reads unless the option `--outSAMunmapped Within` is set during the alignment. Set this option during the alignment with STAR.
 
    * **Warnings when aligning with [TopHat2](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2013-14-4-r36):**  TopHat2 reports mapped (accepted_hits.bam) and unmapped (unmapped.bam) reads in separate files. Moreover, accepted_hits.bam file comprises secondary and supplementary reads. Prior to running XenoSplit, these reads should be removed and accepted_hits.bam and unmapped.bam should be merged. [samtools](http://www.htslib.org/) can be used
       * to remove secondary and supplementary reads from accepted.bam files:
       
              samtools view -h -F 256 -F 2048 accepted_hits.bam > accepted_hits_rm.bam
        * to concatenate `accepted_hits_rm.bam` and `unmapped.bam` files:
       
              samtools merge -o output.bam accepted_hits_rm.bam unmapped.bam 
 * At the moment XenoSplit only accepts BAM files that are sorted by read names (i.e., the QNAME field) rather than by chromosomal coordinates. [samtools](http://www.htslib.org/) can be used to sort bam files by name as below:

        samtools sort -n -o input.sorted.bam  input.bam
        
  ## Single-end example
  If the samples are single-end:
      
    python xenosplit.py --out graftOut.bam graft.bam host.bam
      
  ## Paired-end example
  If the samples are paired-end, `--pairedEnd` mode should be turned on:
      
    python xenosplit.py --pairedEnd --out graftOut.bam graft.bam host.bam
  
  ## Specifying the aligner
  If the samples are aligned with [STAR](https://github.com/alexdobin/STAR) then `--aligner` should be specified as below:
  
    python xenosplit.py --out graftOut.bam --aligner star graft.bam host.bam

  ## Reporting the goodness of mapping scores
  XenoSplit can switch into reporting mode using `--count` argument. In this mode, XenoSplit does not output the `graftOut.bam` file, only prints out the graft and host "goodness of mapping" scores for each read on the screen. These scores can be saved in `goodnessOfMapping.txt` file and further analysed. To save the scores the following code can be run:
     
    python xenosplit.py --count graft.bam host.bam > goodnessOfMapping.txt
   
# Citation

# Contributing
Bug reports and feature requests are welcome. Please follow the steps below to do so:
1. Create an issue to discuss your idea
2. [Fork](https://github.com/goknurginer/XenoSplit/fork) XenoSplit
3. Create your feature branch with `git checkout -b new-feature`
4. Commit your changes with `git commit -am 'Add some feature'`
5. Push to the branch with `git push origin new-feature`
6. Create a new Pull Request
