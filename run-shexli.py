#!/usr/bin/python3
import os
import shexli

#Process the environment
extensionPath = os.environ.get("EXTENSION_PATH", "")

#Verify the extension bundle path
if (extensionPath == ""):
  print("No extension bundle path specified")
  exit(1)
elif (not os.path.isfile(extensionPath)):
  print(f"'{extensionPath}' isn't an extension bundle")
  exit(1)

#Analyse the extension bundle
results = shexli.analyze_path(extensionPath)

#TODO: Process the results, handling exceptions, warnings, errors and return codes
print(results)
