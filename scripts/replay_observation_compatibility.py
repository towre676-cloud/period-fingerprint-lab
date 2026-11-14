"""Generate common weight-39 evidence and run checkers outside the package.

Run from the repository root:
    python -m scripts.replay_observation_compatibility --out /tmp/observation-replay
"""
import argparse
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

from periodlab.holonomic import holonomic_receipt
from periodlab.observation_design import design_exact_observations
from periodlab.observation_engine import analyze
from periodlab.weights import WeightedProjective as W


ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=[(1,1,1,1,1,5,5,24),(2,2,2,2,3,3,25)]


def replay(destination):
    destination.mkdir(parents=True, exist_ok=True)
    spaces=[W(w) for w in WEIGHTS]
    def spec(sensors, budget):
        return {"family":"weighted_projective", "universe":{
            "kind":"explicit", "weights":[list(w) for w in WEIGHTS]},
            "sensors":sensors, "budget":budget}
    planner=design_exact_observations(spaces, range(1,4), 1)
    prefix=analyze(spec([1,2,3], 2))
    receipts={
        "planner_prefix_collision":("bridge",design_exact_observations(spaces,[1,2],2)),
        "planner_minimum_panel":("bridge",planner),
        "engine_prefix_collision":("engine",prefix),
        "engine_zero_prefix_completion":("engine",analyze(spec([1,2,3],0))),
        "engine_selected_panel":("engine",analyze(spec([3,1,2],1))),
        "holonomic_left":("bridge",holonomic_receipt(spaces[0],3)),
        "holonomic_right":("bridge",holonomic_receipt(spaces[1],3)),
    }
    for example in sorted((ROOT/"examples").glob("observation_*.json")):
        receipts[example.stem]=("engine",analyze(json.loads(example.read_text())))
    bad=copy.deepcopy(planner)
    bad["all_allowed_signatures"][0][2]="0"
    corruptions={"invalid_planner_signature":("bridge",bad)}
    bad=copy.deepcopy(prefix)
    bad["result"]["pair_separator"]["left_value"]="0"
    corruptions["invalid_engine_separator"]=("engine",bad)
    bad=copy.deepcopy(receipts["holonomic_left"][1])
    bad["theta_polynomial_A_ascending"][0]="1"
    corruptions["invalid_holonomic_operator"]=("bridge",bad)
    checks=[]
    with tempfile.TemporaryDirectory(prefix="period-standalone-") as directory:
        isolated=Path(directory)
        for kind in ("bridge","engine"):
            shutil.copy2(ROOT/f"verify_observation_{kind}.py", isolated)
        for expected, batch in ((True,receipts),(False,corruptions)):
            for name,(kind,receipt) in batch.items():
                path=destination/f"{name}.json"
                path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
                proc=subprocess.run([sys.executable,"-I",str(isolated/f"verify_observation_{kind}.py"),
                                     str(path.resolve())],cwd=isolated,capture_output=True,text=True)
                if (proc.returncode==0)!=expected:
                    raise RuntimeError(f"Unexpected checker result for {name}: {proc.stdout} {proc.stderr}")
                checks.append({"receipt":path.name,"checker":kind,
                               "expected_valid":expected,"exit_code":proc.returncode,
                               "stdout":proc.stdout.strip(),"stderr":proc.stderr.strip()})
    sep=prefix["result"]["pair_separator"]
    ratio=Fraction(int(sep["left_value"]),int(sep["right_value"]))
    if planner["selected_supported_indices"]!=[3] or ratio!=Fraction(1080400,1002001):
        raise RuntimeError("Weight-39 compatibility invariant failed")
    summary={"weight_sum":39,"matching_supported_indices":[1,2],
             "separating_supported_index":3,"separating_ordinary_degree":117,
             "third_coefficient_ratio_left_over_right":str(ratio),
             "valid_standalone_receipts":len(receipts),"rejected_corruptions":len(corruptions),
             "isolation":"checkers copied without periodlab; python -I; temporary working directory",
             "checks":checks}
    (destination/"standalone_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    return {key:value for key,value in summary.items() if key!="checks"}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    print(json.dumps(replay(parser.parse_args().out),indent=2,sort_keys=True))
