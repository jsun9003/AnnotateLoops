# AnnotateLoops

This Python script annotates genomic loops, focusing on identifying Super Enhancer (SE) and promoter (P) loops. It takes BEDPE format loop files as input, along with an annotation file mapping files to labels. The script intersects loop anchors with SE and P annotation files, categorizing loops accordingly. Output files are generated for SE-P loop combinations, as well as a summary file detailing the annotated loops. The script enhances genomic analysis by providing insights into SE and P loop interactions.

## Features
- Annotates loops by intersecting loop anchors with SE and P annotation files.
- Categorizes loops into SE-P combinations.
- Generates detailed output files and a summary file.

## Usage
```sh
usage: Annotate_loops.py [-h] -a ANNOTATION_FILE -i INPUT [INPUT ...] [-o OUTPUT_DIRECTORY]
Annotate_loops.py: error: the following arguments are required: -a/--annotation_file, -i/--input

## Arguments
-a ANNOTATION_FILE, --annotation_file: Path to the annotation file that maps files to labels.
-i INPUT [INPUT ...], --input: BEDPE format loop files.
-o OUTPUT_DIRECTORY, --output_directory: Directory to save the output files. (Optional)

## Example Annotation File
annotate.txt
ESC.mm9.SE.bed SE
promoters_3kb_merged-TID_GID_GN.bed P
