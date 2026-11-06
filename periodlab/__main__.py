"""CLI for exact weighted-projective period investigations.

Use: python -m periodlab --help
"""
import argparse
import json
from .weights import WeightedProjective, terminal_report
from .periods import fingerprint
from .reconstruct import reconstruct_from_prefix, reconstruct_dense_prefix
from .certificates import collision_receipt
from .reconstruction_receipt import make_reconstruction_receipt
from verify_receipt import verify as independent_verify
from .search import collision_scan


def _space(s):
    return WeightedProjective.from_weights(tuple(int(x.strip()) for x in s.split(",")))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)

    one = commands.add_parser("analyze", help="exact coefficients and terminality")
    one.add_argument("--weights", required=True, help="e.g. 1,1,1,2")
    one.add_argument("--count", type=int, default=8)

    reconstruct = commands.add_parser("reconstruct", help="unique weights from known L and at least L coefficients")
    reconstruct.add_argument("--total-weight", type=int, required=True)
    reconstruct.add_argument("--coefficients", required=True,
                             help="comma-separated c_0,c_L,... including 1")

    dense = commands.add_parser("reconstruct-dense", help="recover weights from full degree coefficient JSON file")
    dense.add_argument("path",help="JSON array c0,...,cD (including all zero entries)")

    search = commands.add_parser("search", help="bounded collision census")
    search.add_argument("--max-sum", type=int, default=40)
    search.add_argument("--prefix", type=int, default=2)
    search.add_argument("--terminal-only", action="store_true")
    search.add_argument("--different-dimensions", action="store_true")
    search.add_argument("--max-dim", type=int, default=None)

    cert = commands.add_parser("certificate", help="emit exact pairwise collision certificate")
    cert.add_argument("--left", required=True)
    cert.add_argument("--right", required=True)
    cert.add_argument("--matching", type=int, default=2)

    rec = commands.add_parser("reconstruction-certificate", help="emit finite uniqueness receipt")
    rec.add_argument("--total-weight", type=int, required=True)
    rec.add_argument("--coefficients", required=True, help="comma-separated c_0,c_L,...")

    verify = commands.add_parser("verify", help="verify an external JSON certificate")
    verify.add_argument("path")

    args = parser.parse_args(argv)
    if args.action == "analyze":
        space = _space(args.weights)
        result = {"weights": list(space.weights), "dimension": space.dimension,
                  "total_weight": space.total_weight,
                  "coefficients_at_multiples_of_total": [
                      str(x) for x in fingerprint(space, args.count)],
                  "terminality": terminal_report(space)}
    elif args.action == "reconstruct":
        result = reconstruct_from_prefix(args.total_weight, [
            int(t.strip()) for t in args.coefficients.split(",")])
    elif args.action == "reconstruct-dense":
        with open(args.path,encoding="utf-8") as stream:
            result = reconstruct_dense_prefix(json.load(stream))
    elif args.action == "search":
        scan = collision_scan(args.max_sum, args.prefix, args.terminal_only,
                              args.max_dim, args.different_dimensions)
        result = {"spaces_examined": scan["spaces_examined"],
                  "spaces_per_total_weight": scan["spaces_per_total_weight"],
                  "filters": scan["filters"],
                  "pair_count": len(scan["collisions"]),
                  "pairs": [
                      {"left": list(a.weights), "right": list(b.weights),
                       "dimensions": [a.dimension,b.dimension]}
                      for a,b in scan["collisions"]]}
    elif args.action == "certificate":
        result = collision_receipt(_space(args.left), _space(args.right),
                                   args.matching)
    elif args.action == "reconstruction-certificate":
        result = make_reconstruction_receipt(args.total_weight, [
            int(s.strip()) for s in args.coefficients.split(",")])
    else:
        with open(args.path, encoding="utf-8") as stream:
            result = independent_verify(json.load(stream))
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
