# Published external data: source and ingestion contract

**Source:** Coates, Kasprzyk and Veneziale, *A dataset of 150000
terminal weighted projective spaces*, Zenodo v1.0 (2022):
https://doi.org/10.5281/zenodo.5790079 (CC0).

The original archive contains `rank_1_dim_1.txt` through
`rank_1_dim_10.txt`, one Python-style list of N+1 weights per line
in file `rank_1_dim_N.txt`. It also includes the author's Magma
source. The published description includes the sample row
`[1,2,5,14,21]` for dimension 4.

To audit your own *original* download, leave the ten text files
unmodified and run:

```sh
python scripts/audit_zenodo_rank1.py path/to/downloaded
```

This verifies each displayed published MD5 digest, file syntax,
well-formedness, canonicality, dimension, terminality via the exact
published criterion, duplicate weights, and total row count 150000.
A SHA-256 digest of each local original file is also reported.
Optional `--skip-terminality-recheck` explicitly downgrades the audit.

**Status:** Dataset adapter and source citation are implemented and
the source's displayed example is tested. The complete 150000-row
dataset has NOT been downloaded or audited in this repository; a full
audit is not claimed until the command runs successfully against the
original files and its output is preserved. The exact source data must
not be confused with synthetic fixtures.

Other relevant dataset: 200000 terminal Picard-rank-two toric varieties,
also from the same authors; its schema requires separate validation
before import. The present `toric2.py` coefficient experiment does not
replace such validation.

The published Zenodo checksums are copied for integrity checking,
but a matching MD5 alone is not strong cryptographic authentication.
The source URL and license remain the primary provenance anchors.
