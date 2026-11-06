"""Secure, provenance-aware adapter for the published Zenodo rank-one dataset.

No network downloads performed. The source uses files rank_1_dim_N.txt;
each line is an array of N+1 positive integer weights. Files are audited
before use. Source: https://doi.org/10.5281/zenodo.5790079 (CC0).
"""
import ast
import hashlib
from pathlib import Path
from .weights import WeightedProjective, is_terminal


def read_zenodo_rank1(path, expected_dim=None, require_terminal=True,
                      expected_md5=None, reject_duplicates=True):
    path=Path(path)
    raw=path.read_bytes()
    checksum=hashlib.md5(raw).hexdigest()  # Published legacy MD5 metadata, not security authentication.
    if expected_md5 is not None and checksum.lower()!=expected_md5.lower():
        raise ValueError("file checksum disagrees with published Zenodo metadata")
    rows=[]
    seen=set()
    for line_number, line in enumerate(raw.decode("utf-8-sig").splitlines(),1):
        line=line.strip()
        if not line:
            continue
        try:
            parsed=ast.literal_eval(line)
        except (ValueError,SyntaxError,TypeError) as e:
            raise ValueError(f"invalid literal on line {line_number}") from e
        if not isinstance(parsed,(list,tuple)):
            raise ValueError(f"expected one weight list on line {line_number}")
        try:
            space=WeightedProjective.from_weights(tuple(parsed))
        except ValueError as e:
            raise ValueError(f"invalid WPS on line {line_number}: {e}") from e
        if expected_dim is not None and space.dimension!=expected_dim:
            raise ValueError(f"dimension mismatch on line {line_number}")
        if require_terminal and not is_terminal(space):
            raise ValueError(f"nonterminal space on line {line_number}")
        if reject_duplicates and space.weights in seen:
            raise ValueError(f"duplicate weights on line {line_number}")
        seen.add(space.weights)
        rows.append(space)
    return {"path":str(path), "sha256":hashlib.sha256(raw).hexdigest(),
            "md5":checksum, "rows":rows, "row_count":len(rows),
            "dimensions":sorted({s.dimension for s in rows}),
            "license":"CC0 1.0", "source_doi":"10.5281/zenodo.5790079"}


# File md5 checksums displayed on Zenodo v1.0 record; use as integrity
# metadata ONLY, not as proof of an authentic original source.
PUBLISHED_MD5={
  1:"5ef98f395ae61e9b0cb500f403e70b34",
  2:"cbb64bdaa78510af721a481ea5bcc7c4",
  3:"cef658a948f26145cfcfd1c5bfc1aa8d",
  4:"9b424f1e9608a3a0fa1800ff1f31aeb0",
  5:"3423dd60f3009232910be18af795437a",
  6:"b3cbf8fe9512a16768c4fd87fe17d790",
  7:"ce17817c7bbeb918b6d81b9149638d13",
  8:"f6cdd9be70ae4a032f81d6979c27d96e",
  9:"ba7f944d6018abaee90176d88c45f77b",
  10:"602a964b28031af41a7cba7614e655be"
}
