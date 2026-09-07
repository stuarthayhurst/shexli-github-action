#!/usr/bin/python3
import os
import shexli

#Fetch the environment
extensionPath = os.environ.get("EXTENSION_PATH", "")
maxErrors = os.environ.get("MAX_ERRORS", "0")
maxWarnings = os.environ.get("MAX_WARNINGS", "-1")

#Verify the extension bundle path
if (extensionPath == ""):
  print("No extension bundle path specified")
  exit(1)
elif (not os.path.isfile(extensionPath)):
  print(f"'{extensionPath}' isn't an extension bundle")
  exit(1)

#Verify error and warning limits
try:
  maxErrors = int(maxErrors)
except ValueError:
  print("Maximum error count threshold must be numerical")
  exit(1)
try:
  maxWarnings = int(maxWarnings)
except ValueError:
  print("Maximum warning count threshold must be numerical")
  exit(1)

#Analyse the extension bundle
results = shexli.analyze_path(extensionPath)

#TODO: Process the results, handling exceptions, warnings, errors and return codes
print(results)

#Fail if too many errors are reported
errorCount = results.summary["severity_counts"]["error"]
if (maxErrors >= 0 and errorCount > maxErrors):
  print(f"{errorCount} error(s) detected, greater than allowed limit of {maxErrors}")
  exit(1)

#Fail if too many warnings are reported
warningCount = results.summary["severity_counts"]["warning"]
if (maxWarnings >= 0 and warningCount > maxWarnings):
  print(f"{warningCount} warnings(s) detected, greater than allowed limit of {maxWarnings}")
  exit(1)
