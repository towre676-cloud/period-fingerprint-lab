"""Local-first, standard-library HTTP API and explorer.

Run: python -m periodlab.server --port 8765
Binds loopback ONLY by default. Not designed to be internet-facing.
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from .weights import WeightedProjective, terminal_report
from .periods import fingerprint
from .reconstruct import reconstruct_from_prefix, reconstruct_dense_prefix
from .certificates import collision_receipt
from .search import collision_scan
from verify_receipt import verify

MAX_BODY=1_000_000
WEB=Path(__file__).resolve().parent.parent/"web"/"index.html"


def _space(value):
    if not isinstance(value,list) or len(value)>32:
        raise ValueError("weights must be an array of 2-32 positive integers")
    space=WeightedProjective.from_weights(value)
    if space.total_weight>250:
        raise ValueError("total weight > 250 exceeds interactive safety limit")
    return space


def process(operation,data):
    if not isinstance(data,dict):
        raise ValueError("JSON object required")
    if operation=="analyze":
        space=_space(data.get("weights"))
        count=data.get("count",6)
        if type(count) is not int or not 1<=count<=32:
            raise ValueError("count must be 1..32")
        return {"weights":list(space.weights),"dimension":space.dimension,
                "total_weight":space.total_weight,
                "supported_coefficients":[str(x) for x in fingerprint(space,count)],
                "terminality":terminal_report(space)}
    if operation=="reconstruct":
        L=data.get("total_weight")
        coeff=data.get("coefficients")
        if type(L) is not int or not 2<=L<=100 or not isinstance(coeff,list):
            raise ValueError("total weight 2..100 and coefficient list required")
        if len(coeff)>150 or any(type(x) is not str or not x.isdecimal() for x in coeff):
            raise ValueError("coefficients must be decimal strings")
        return reconstruct_from_prefix(L,[int(x) for x in coeff])
    if operation=="reconstruct-dense":
        coeff=data.get("coefficients")
        if not isinstance(coeff,list) or len(coeff)>10000:
            raise ValueError("dense coefficient array must have <= 10,000 entries")
        if any(type(x) is not str or not x.isdecimal() for x in coeff):
            raise ValueError("dense coefficients must be decimal strings")
        return reconstruct_dense_prefix([int(x) for x in coeff])
    if operation=="certificate":
        left=_space(data.get("left"))
        right=_space(data.get("right"))
        n=data.get("matching",2)
        if type(n) is not int or not 1<=n<=20:
            raise ValueError("matching must be 1..20")
        return collision_receipt(left,right,n)
    if operation=="verify":
        return verify(data.get("certificate"))
    if operation=="search":
        limit=data.get("max_sum",30)
        prefix=data.get("prefix",2)
        if type(limit) is not int or not 2<=limit<=40 or type(prefix) is not int or not 1<=prefix<=4:
            raise ValueError("max_sum must be 2..40; prefix must be 1..4")
        result=collision_scan(limit,prefix,
            terminal_only=data.get("terminal_only") is True,
            only_dim_mismatch=data.get("different_dimensions") is True)
        return {"spaces_examined":result["spaces_examined"],"filters":result["filters"],
                "pairs":[{"left":list(a.weights),"right":list(b.weights),
                          "dimensions":[a.dimension,b.dimension]}
                         for a,b in result["collisions"]]}
    raise ValueError("unknown operation")


class Handler(BaseHTTPRequestHandler):
    def _json(self,status,body):
        raw=json.dumps(body,sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path=urlsplit(self.path).path
        if path in ("/","/index.html"):
            content=WEB.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(content)))
            self.send_header("X-Content-Type-Options","nosniff")
            self.end_headers()
            self.wfile.write(content)
        elif path=="/api/health":
            self._json(200,{"ok":True,"service":"periodlab","version":"0.2.0"})
        else:
            self._json(404,{"error":"not found"})

    def do_POST(self):
        path=urlsplit(self.path).path
        if not path.startswith("/api/"):
            return self._json(404,{"error":"not found"})
        try:
            length=int(self.headers.get("Content-Length","0"))
            if not 0 < length <= MAX_BODY:
                return self._json(413,{"error":"payload size out of range"})
            incoming=json.loads(self.rfile.read(length))
            result=process(path[len("/api/"):],incoming)
            self._json(200,result)
        except (ValueError,KeyError,TypeError,OverflowError,RecursionError) as e:
            self._json(400,{"error":str(e)})


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",type=int,default=8765)
    args=parser.parse_args(argv)
    if not 1<=args.port<=65535:
        parser.error("port out of range")
    address=("127.0.0.1",args.port)
    with ThreadingHTTPServer(address,Handler) as server:
        print(f"Period lab at http://127.0.0.1:{args.port}/",flush=True)
        server.serve_forever()


if __name__=="__main__":
    main()
