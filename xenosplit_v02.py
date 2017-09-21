# Title: XenoSplit code
# Author: Aaron Lun and Goknur Giner
#!/usr/bin/env python

import pysam
import sys
import argparse

parser = argparse.ArgumentParser(description='Compare two BAM files for the same reads and allocate them into new files based on matches')
parser.add_argument('bam1', type=str, help='first input BAM file')
parser.add_argument('bam2', type=str, help='second input BAM file')
parser.add_argument('--count', dest='count', action='store_true', help='switch to reporting mode')
parser.add_argument('--min', dest='min', type=int, help='minimum difference in matches for assignment to either file', default=1)
parser.add_argument('--out1', type=str, dest='out1', help='first output BAM file', default='out1.bam')
parser.add_argument('--out2', type=str, dest='out2', help='second output BAM file', default='out2.bam')

args = parser.parse_args()
docount = args.count
fh1 = pysam.Samfile(args.bam1, "rb")
fh2 = pysam.Samfile(args.bam2, "rb")
if not docount:
    oh1 = pysam.Samfile(args.out1, "wb", template=fh1)
    oh2 = pysam.Samfile(args.out2, "wb", template=fh2)

def getmatch(read):
    if read.is_unmapped:
        return 0
    mmatch = 0
    for op, num in read.cigar:
        if op == 0 or op == 1 or op == 2:
             mmatch += num
    tags=dict(read.tags)
    if "NM" in tags:
        mmatch -= tags["NM"]
    return mmatch

fail = 0
while 1:
    try:
        read1 = fh1.next()
    except StopIteration:
        fail += 1
    try:
        read2 = fh2.next()
    except StopIteration:
        fail += 1
    if fail==1:
        raise ValueError, "incoming BAM files are not of same length"
    elif fail==2:
        break
    if read1.qname!=read2.qname:
        raise ValueError, "reads in the two BAM files are not in the same order"   
    if read1.is_unmapped and read2.is_unmapped:
        continue
        
    out1=getmatch(read1)
    out2=getmatch(read2)
    if docount:
        print str(out1)+"\t"+str(out2)
        continue
    if out1 - out2 >= args.min:
        oh1.write(read1)
    elif out2 - out1 >= args.min:
        oh2.write(read2)
    
fh1.close()
fh2.close()
if not docount:
    oh1.close()
    oh2.close()
