#!/usr/bin/env python
from __future__ import division # stops rounding the divisions
import pysam
import sys
import argparse

parser = argparse.ArgumentParser(description='Compare two BAM files for the same reads and allocate them into new files based on matches',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('graft', type=str, help='graft BAM file')
parser.add_argument('host', type=str, help='host BAM file')
parser.add_argument('--count', dest='count', action='store_true', help='switch to reporting mode')
parser.add_argument('--min', dest='min', type=int, help='minimum difference in matches for assignment to either file', default=1)
parser.add_argument('--out', type=str, dest='out', help='graft output BAM file', default='graftOut.bam')
parser.add_argument('--pairedEnd', dest='pairedEnd', action='store_true', help='switch to pairedEnd mode so the mapping scores will be computed using pairs')

args = parser.parse_args()
docount = args.count
fh1 = pysam.Samfile(args.graft, "rb")
fh2 = pysam.Samfile(args.host, "rb")
if not docount:
    oh = pysam.Samfile(args.out, "wb", template=fh1)
    ohcount = ()
mismatch_flag="NM"

def getmatch(read, flag):
    if read.is_unmapped:
        return 0
    mmatch = 0
    for op, num in read.cigar:
        if op == 0 or op == 1 or op==2:
             mmatch += num
    tags=dict(read.tags)
    if flag in tags:
        mmatch -= tags[flag]
    return mmatch

if args.pairedEnd:
    fail = 0
    while 1:
            try:
                read1_1 = fh1.next()
                read1_2 = fh1.next()
            except StopIteration:
                fail += 1
            try:
                read2_1 = fh2.next()
                read2_2 = fh2.next()
            except StopIteration:
                fail += 1
            if fail==1:
                raise ValueError, "incoming BAM files are not of same length"
            elif fail==2:
                break
            if read1_1.qname!=read2_1.qname:
                raise ValueError, "reads in the two BAM files are not in the same order"   
            if read1_1.is_unmapped or read1_2.is_unmapped:
                continue
                
            out1_1=getmatch(read1_1, mismatch_flag)
            out1_2=getmatch(read1_2, mismatch_flag)
            out2_1=getmatch(read2_1, mismatch_flag)
            out2_2=getmatch(read2_2, mismatch_flag)
            out1=(out1_1+out1_2)/2
            out2=(out2_1+out2_2)/2
            if docount:
                print str(out1)+"\t"+str(out2)
                continue
            if out1 - out2 >= args.min:
                oh.write(read1_1)
                oh.write(read1_2)
            
    fh1.close()
    fh2.close()
    if not docount:
        oh.close()        
else:
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
                
            out1=getmatch(read1, mismatch_flag)
            out2=getmatch(read2, mismatch_flag)
            if docount:
                print str(out1)+"\t"+str(out2)
                continue
            if out1 - out2 >= args.min:
                oh.write(read1)
            
    fh1.close()
    fh2.close()
    if not docount:
        oh.close()
    
