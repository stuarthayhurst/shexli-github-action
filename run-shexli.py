#!/usr/bin/python3
import os
import shexli

#Reformat extensions analysis results
def processResults(results, ignoredChecksList):
  processedResults = {}
  processedResults["findings"] = []

  errorCount = 0
  warningCount = 0

  #Process reported findings into a simplified form
  for finding in results.findings:
    #Skip ignored rules
    if finding.rule_id in ignoredChecksList:
      continue

    processedFinding = {}

    #Merge the rule ID and title, record the message
    processedFinding["title"] = f"[{finding.rule_id}]: {finding.title}"
    processedFinding["message"] = finding.message

    #Record and track severity
    processedFinding["severity"] = finding.severity
    if processedFinding["severity"] == "error":
      errorCount += 1
    elif processedFinding["severity"] == "warning":
      warningCount += 1
    else:
      print(f"Unknown finding type '{finding.severity}'")

    #Process instances of the finding in the source code
    processedFinding["instances"] = []
    for evidence in finding.evidence:
      instance = {}
      instance["entry"] = f"{evidence.path}:{evidence.line}"
      instance["sourceCode"] = evidence.snippet
      processedFinding["instances"].append(instance)

    #Process check details
    processedFinding["ruleUrl"] = finding.source_url

    processedResults["findings"].append(processedFinding)

  processedResults["errors"] = errorCount
  processedResults["warnings"] = warningCount

  return processedResults

#Print formatted results
def printResults(processedResults):
  for finding in processedResults["findings"]:
    #Print finding title and message
    print(f"{finding['severity'].capitalize()}: {finding['title']}")
    print(f" - Message: {finding['message']}")

    #Show code violations
    for evidence in finding["instances"]:
      indented = False
      if (len(evidence['sourceCode']) > 0):
        indented = evidence['sourceCode'][0].isspace()
      if indented:
        print(f" - Code:\n{evidence['sourceCode']} ({evidence['entry']})")
      else:
        print(f" - Code: {evidence['sourceCode']} ({evidence['entry']})")

    #Print rule information
    print(f" - URL: {finding['ruleUrl']}\n")

def checkViolations(processedResults, violationType, threshold):
  #Fail if too many violations are reported
  violationCount = processedResults[f"{violationType}s"]
  failed = (threshold >= 0 and violationCount > threshold)

  if failed:
    print(f"{violationCount} {violationType}(s) detected, greater than allowed limit of {threshold}")
  else:
    if (violationCount > 0):
      print(f"{violationCount} {violationType}(s) detected (non-fatal)")
    else:
      print(f"{violationCount} {violationType}(s) detected")

  return (not failed)

#Fetch the environment
extensionPath = os.environ.get("EXTENSION_PATH", "")
maxErrors = os.environ.get("MAX_ERRORS", "0")
maxWarnings = os.environ.get("MAX_WARNINGS", "-1")
ignoredChecks = os.environ.get("IGNORE_CHECKS", "")

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

#Split ignored checks
ignoredChecksList = [check for check in ignoredChecks.split(" ") if check != ""]

#Analyse the extension bundle
results = shexli.analyze_path(extensionPath)
processedResults = processResults(results, ignoredChecksList)

#Display the processed results
printResults(processedResults)

#Fail if too many errors or warnings were found
passed = checkViolations(processedResults, "error", maxErrors)
passed &= checkViolations(processedResults, "warning", maxWarnings)
if not passed:
  exit(1)
