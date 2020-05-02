#!/usr/bin/env python

import os, json, sys, argparse, glob, shutil
from pathlib import Path

target = "out/target/product/"
update_repo = "evox_devices/unofficial"
indents = 3


parser = argparse.ArgumentParser(
    description="Update change log. Call with: \n update_changelog --url upload_url --build path_to_json --changelog path_to_changelog"
)

parser.add_argument("--url", action="store", dest="url", required=True)
parser.add_argument("--changelog", action="store", dest="changelog", required=True)
parser.add_argument("--device", action="store", dest="device", required=True)


def get_latest_zip(d):
    zip_list = glob.glob(f"{d}/*.zip")
    built_zip = max(zip_list, key=os.path.getmtime)

    return built_zip


def main():
    options = parser.parse_args()
    device_code = options.device
    out_zipdir = Path(target) / device_code

    # There maybe old artifacts files in custom servers.
    out_zip = get_latest_zip(out_zipdir)

    print(f"Using zip {out_zip}")
    out_bjson = Path(f"{out_zip}.json")
    old_djson = Path(update_repo) / f"builds/{device_code}.json"

    newdata = ""

    with open(out_bjson) as bj, open(old_djson) as dj:
        bdata = json.load(bj)
        odata = json.load(dj)

        bdata["url"] = options.url

        newdata = {**odata, **bdata}
        newfname = newdata["filename"]

    with open(old_djson, "w") as nj:
        json.dump(newdata, nj, indent=indents, ensure_ascii=False, sort_keys=True)

    # Update changelog.
    sfile = options.changelog
    dfile = Path(update_repo) / f"changelogs/{device_code}/{newfname}.txt"
    shutil.copy2(sfile, dfile)


if __name__ == "__main__":
    main()
