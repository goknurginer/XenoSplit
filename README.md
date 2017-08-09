# XenoSplit
Mapping pipeline 
Author: Göknur Giner & Aaron Lun

XenoSplit is a solution to bioinformatics challenges of transcriptional profiling of patient derived xenografts (PDXs). Xenograft mouse models are known to be challenging as they suffer from the scarcity of human cells. The major challenge of working with these xenografts is the mixed human and mouse information. To classify ambiguous reads, XenoSplit compares human mapping scores with mouse genome mapping scores. First, reads were mapped to human and mouse genomes seperately. Then reads were allocated to a species based on the number of correctly aligned bases. This identifies a sufficient number of human reads to proceed with downstream analyses.

XenoSplit is a simple and effective method, which improves the accuracy and sensitivity of detecting the reads originated from the graft tissue. XenoSplit is a fast computational tool and it is freely available for non commercial use.
 
 
