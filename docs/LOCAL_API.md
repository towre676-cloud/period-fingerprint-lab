# Local HTTP API and exact explorer

Run on the user's own computer (Python 3.11+):

```sh
python -m periodlab.server --port 8765
```

Open http://127.0.0.1:8765/ to use the dependency-free exact
BigInt comparison explorer. The server **only binds to localhost**.

The browser explorer calculates coefficients in JavaScript and does
not claim to be the independent Python verifier; use the JSON endpoints
to generate and verify exact receipts in the Python implementation.

Example requests:

```sh
curl -s -X POST http://127.0.0.1:8765/api/analyze \
  -H 'Content-Type: application/json' \
  -d '{"weights":[1,1,1,2],"count":6}'

curl -s -X POST http://127.0.0.1:8765/api/reconstruct \
  -H 'Content-Type: application/json' \
  -d '{"total_weight":3,"coefficients":["1","6","90"]}'

curl -s -X POST http://127.0.0.1:8765/api/reconstruct-dense \
  -H 'Content-Type: application/json' \
  -d '{"coefficients":["1","0","0","6","0","0","90"]}'
```

Endpoints:

| Path | Action |
|---|---|
| `GET /api/health` | Local health and version |
| `POST /api/analyze` | Weighted space, exact prefix and terminality |
| `POST /api/reconstruct` | Known-L coefficient reconstruction |
| `POST /api/reconstruct-dense` | Infer L from full series and reconstruct |
| `POST /api/certificate` | Collision receipt |
| `POST /api/verify` | Independent receipt verification |
| `POST /api/search` | Bounded finite candidate scan |

The service imposes input-size, coefficient-count and total-weight
bounds to reduce accidental resource exhaustion, but it is not a
production internet-facing service. It has no authentication, database,
accounts, remote compute isolation, or hosted deployment. **Do not**
bind it to a publicly reachable network address without a separate
security design and resource-management review.

To persist a result, save the JSON response; the Python CLI and
standalone `verify_receipt.py` can reproduce certificates offline.
