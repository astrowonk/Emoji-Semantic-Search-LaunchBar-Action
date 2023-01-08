#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('item')

args = parser.parse_args()

subprocess.check_output([
    "/usr/bin/osascript", "-e",
    f'tell app "LaunchBar" to paste in frontmost application "{args.item}"'
])