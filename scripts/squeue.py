#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/chazeon/.pyenv/shims/python3

import sys
from fabric import Connection
from typing import NamedTuple
from collections import defaultdict

import sys, re, urllib.parse
from pathlib import Path
import textwrap
import dateutil.parser
from io import StringIO

sys.path.append(str(Path(__file__).parent.parent / "libs"))

import bitbar

user = "USER"
server = "example.com"
prefix = ""


color = {
    "RUNNING": "green",
    "COMPLETED": "blue",
    "FAILED": "red",
    "TIMEOUT": "red",
    "PENDING": "gray"
}

def get_queue(sout: str):
    lines = sout.splitlines()
    def yield_results():
        field_names = tuple(field.strip().lower() for field in lines[0].split("|"))
        for line in lines[1:]:
            field_values = tuple(field.strip() for field in line.split("|"))
            if len(field_values) == 0: continue
            yield dict(zip(field_names, field_values))
    return list(yield_results())

conn = Connection(f"{user}@{server}")
result = conn.run("squeue -u {user} -o \"%A|%P|%T|%M|%L|%Z\"", hide=True)

#queue = result.stdout.strip().split("\n")
queue = get_queue(result.stdout)
queue.sort(key=lambda x: x["partition"])

pkg = bitbar.BitBarMessagePack(f"📺{len([j for j in queue if j['state'] == 'RUNNING'])}/{len([j for j in queue if j['state'] == 'PENDING'])}")
pkg.append("SDSC Comet", {"href": "http://sdsc.edu/support/user_guides/comet.html"})
pkg.append("---")
for job_info in queue:
    parent = bitbar.BitBarMessageParent(f"[{job_info['partition']}] {job_info['jobid']} ({job_info['time']} / {job_info['time_left']})")
    if job_info["state"] in color.keys():
        parent.attrs["color"] = color[job_info['state']]
    dir = job_info['work_dir'].replace(prefix, '')
    parent.children.append(dir)
    pkg.append(parent)
print(str(pkg))
