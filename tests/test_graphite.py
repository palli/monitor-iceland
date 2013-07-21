#!/usr/bin/env python
#
# This script will run every executable in ../graphite.d folder and check if it outputs data
# in a graphite compatible format

import subprocess
import os

script_dir = "../graphite.d"

def run_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    stdout, stderr = proc.communicate('through stdin to stdout')
    result = proc.returncode, stdout, stderr
    return result


for dir,subdirs,files in os.walk(script_dir):
  for script in files:
    if script == 'README.md':
      continue
    full_path = dir + "/" + script
    print "Testing %30s ..." % script,
    return_code,stdout,stderr = run_command(full_path)
    output = stdout.splitlines()
    invalid_metrics = []
    if return_code != 0:
      print "Exited with error code", return_code
      break
    for i in output:
      if len(i.split()) != 3:
        invalid_metrics.append(i)
    print "ok .. total metrics: %s .. invalid metrics: %s" % (len(output), len(invalid_metrics))
