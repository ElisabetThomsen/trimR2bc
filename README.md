# trimR2bc - A trimming tool for linked (barcoded) reads
Tool for removing barcode contamination in linked reads.

Linked reads have a barcode, which is the 16 first bases in R1. The barcode is added during fragmentation, so fragments originating from the same original DNA molecule will have the same barcode. This is a great aid when aligning the reads and assembling e.g. habloblocks.

The barcode is removed from R1 by the barcode-aware aligners.

If the insert size is of propper length the barcode will not be present in R2. On the other hand, if the insert size is too short this will lead to sequencing the barcode in the end of R2 and thus leading to barcode contamination. This contamination can act like adapter contamination, which interferes with the mapping of the reads and increases the risk of calling false positive variants.

trimR2bc removes the barcode contamination from R2.
