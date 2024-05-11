#!/usr/bin/env python3
import argparse
import os
import re
from collections import defaultdict
from itertools import combinations

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="""Annotate loops with anchor types.""")
    parser.add_argument("-a", "--annotation_file", nargs=1, required=True,
                        help="""File recording annotation files and corresponding labels.
Example:
promoter.bed P
super_enhancer.bed SE
Note NA will stand for nothing_labeled, so NA should not be used.""")
    parser.add_argument("-i", "--input", nargs="+", help="input loop files with first 6 cols are two anchors", required=True)
    parser.add_argument("-o", "--output_directory", nargs=1, default=[os.getcwd()], help="output folder for results")
    args = parser.parse_args()

    anno_file = args.annotation_file[0]
    loop_files = args.input
    output_directory = args.output_directory[0]

    os.system("which bedtools")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    d_anno_files, labels = defaultdict(list), []
    with open(anno_file) as f:
        for line in f:
            file, label = re.split(r"\s", line.strip())
            labels.append(label)
            d_anno_files[label] = file
    labels.sort()

    for f in loop_files:
        d = defaultdict(list)
        os.system(f"cut -f 1-3 {f} > {output_directory}/tmp1")
        os.system(f"cut -f 4-6 {f} > {output_directory}/tmp2")
        os.system(f"cat {output_directory}/tmp1 {output_directory}/tmp2 | bedtools sort -i - | uniq > {output_directory}/tmp3")
        for l in labels:
            os.system(f"intersectBed -a {output_directory}/tmp3 -b {d_anno_files[l]} -wa -u > {output_directory}/tmp4")
            with open(f"{output_directory}/tmp4") as intersect_file:
                for line in intersect_file:
                    d[line.strip()].append(l)
        for c in combinations(labels, 2):
            with open(f"{output_directory}/{c[0]}-{c[1]}.{f}", "w") as f1, \
                 open(f"{output_directory}/annotated.{f}", "w") as f2:
                f1.write("")
                f2.write("")
        with open(f) as loop_file:
            for line in loop_file:
                anchor1, anchor2 = "\t".join(line.strip().split("\t")[:3]), "\t".join(line.strip().split("\t")[3:6])
                element1 = sorted(d[anchor1]) if d[anchor1] else ["NA"]
                element2 = sorted(d[anchor2]) if d[anchor2] else ["NA"]
                loops_types = [f"{i}-{j}" for i in element1 for j in element2]
                for t in loops_types:
                    if "NA" not in t:
                        with open(f"{output_directory}/{t}.{f}", "a") as f1:
                            f1.write(line)
                with open(f"{output_directory}/annotated.{f}", "a") as f1:
                    f1.write(f"{line.strip()}\t{','.join(loops_types)}\n")

    os.system(f"rm {output_directory}/tmp1 {output_directory}/tmp2 {output_directory}/tmp3 {output_directory}/tmp4")

if __name__ == "__main__":
    main()
