"""Exact finite reconstruction certificates verifiable by verify_receipt.py."""
from .weights import WeightedProjective, is_terminal
from .periods import fingerprint
from .reconstruct import reconstruct_weights, polynomial_from_prefix


def make_reconstruction_receipt(total_weight, coeffs):
    space = reconstruct_weights(total_weight, coeffs)
    poly = polynomial_from_prefix(total_weight, coeffs)
    return {"schema":"periodlab/reconstruction/v1",
            "total_weight": total_weight,
            "supported_coefficients": [str(x) for x in coeffs],
            "denominator_polynomial_ascending": [str(q) for q in poly],
            "reconstructed_weights": list(space.weights),
            "dimension": space.dimension,
            "terminal": is_terminal(space),
            "uniqueness_assumption": "Known total weight L; well-formed WPS class",
            "source": "Finite rational interpolation and root-multiplicity inversion"}


def receipt_for_weights(weights, extra=0):
    space=WeightedProjective.from_weights(weights)
    if type(extra) is not int or extra < 0:
        raise ValueError("extra must be nonnegative integer")
    return make_reconstruction_receipt(space.total_weight,
                                       fingerprint(space,space.total_weight+extra))
