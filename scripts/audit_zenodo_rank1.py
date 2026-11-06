#!/usr/bin/env python3
"""Audit downloaded Zenodo rank-one files without silently fetching them.

Usage: python scripts/audit_zenodo_rank1.py /path/to/downloaded/files
Only success after all 10 files validate and row count is 150,000.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from periodlab.datasets import read_zenodo_rank1, PUBLISHED_MD5


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--skip-terminality-recheck",action="store_true",
                        help="skip expensive age test (reported as incomplete)")
    args=parser.parse_args()
    reports=[]
    total=0
    global_seen=set()
    for dim in range(1,11):
        path=args.directory/f"rank_1_dim_{dim}.txt"
        report=read_zenodo_rank1(path,expected_dim=dim,
                  require_terminal=not args.skip_terminality_recheck,
                  expected_md5=PUBLISHED_MD5[dim])
        for space in report["rows"]:
            if space.weights in global_seen:
                raise ValueError(f"duplicate across dimension files: {space.weights}")
            global_seen.add(space.weights)
        total+=report["row_count"]
        reports.append({"filename":path.name,"rows":report["row_count"],
                        "md5":report["md5"],"sha256":report["sha256"]})
    if total!=150000:
        raise ValueError(f"expected 150000 weights, found {total}")
    print(json.dumps({"source":"10.5281/zenodo.5790079",
         "records_checked":total, "terminality_rechecked":
          not args.skip_terminality_recheck, "files":reports},
          indent=2,sort_keys=True))


if __name__=="__main__":
    main()
