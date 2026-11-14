# ai-generated: 95% - Codex implemented the published Lab 5 SARIF matching and counting rules P-14 through P-24.
"""Compute per-tool confusion matrices from SARIF and the course's defect labels."""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import unquote


CLASS_CWES = {
    "secret": {259, 260, 321, 798},
    "injection": {74, 77, 78, 79, 80, 88, 89, 90, 91, 94, 95, 96, 611, 776, 917, 943, 1336},
    "deserialization": {502},
    "weak-crypto": {261, 326, 327, 328, 330, 331, 338, 759, 760, 916},
    "insecure-transport": {295, 297, 319, 322, 757},
    "path-traversal": {22, 23, 35, 36, 73},
    "ssrf": {918},
    "vulnerable-dependency": {937, 1035, 1104, 1395},
    "misconfiguration": {16, 215, 250, 489, 668, 732, 1188},
    "access-control": {284, 285, 639, 862, 863},
}
CWE_PATTERN = re.compile(r"(?<![A-Za-z0-9])CWE-([0-9]+)", re.IGNORECASE)
PACKAGE_TOKEN = re.compile(r"[A-Za-z0-9._-]+")
SEMGREP_NAMES = {"semgrep", "semgrep oss", "semgrep ce", "semgrep community edition", "semgrep pro"}


def object_value(value):
    return value if isinstance(value, dict) else {}


def array_value(value):
    return value if isinstance(value, list) else []


def tool_id(run):
    driver = object_value(object_value(run.get("tool")).get("driver"))
    name = driver.get("name")
    if not isinstance(name, str):
        return "unknown"
    name = name.strip().lower()
    if name in SEMGREP_NAMES:
        return "semgrep"
    return re.sub(r"[^a-z0-9]+", "-", name).strip("-") or "unknown"


def tags(item):
    values = object_value(item.get("properties")).get("tags")
    return [tag for tag in array_value(values) if isinstance(tag, str)]


def result_classes(result, rule, tool):
    explicit = object_value(result.get("properties")).get("class")
    if isinstance(explicit, str) and explicit in CLASS_CWES:
        return {explicit}
    if tool == "gitleaks":
        return {"secret"}
    if tool in {"grype", "osv-scanner"}:
        return {"vulnerable-dependency"}
    if tool == "trivy":
        trivy_classes = {
            "vulnerability": "vulnerable-dependency",
            "secret": "secret",
            "misconfiguration": "misconfiguration",
        }
        classes = {trivy_classes[tag.lower()] for tag in tags(rule) if tag.lower() in trivy_classes}
        if classes:
            return classes
    cwes = {int(match.group(1)) for tag in tags(result) + tags(rule) for match in CWE_PATTERN.finditer(tag)}
    return {cls for cls, numbers in CLASS_CWES.items() if numbers & cwes} or {"other"}


def normalized_package(name):
    return re.sub(r"[-_.]+", "-", name.lower())


def findings(run, root, tool):
    driver = object_value(object_value(run.get("tool")).get("driver"))
    rules = [rule for rule in array_value(driver.get("rules")) if isinstance(rule, dict)]
    for result in array_value(run.get("results")):
        if not isinstance(result, dict):
            continue
        kind = result.get("kind")
        if (kind is not None and kind != "fail") or result.get("suppressions"):
            continue
        locations = array_value(result.get("locations"))
        first = object_value(locations[0]) if locations else {}
        physical = object_value(first.get("physicalLocation"))
        uri = object_value(physical.get("artifactLocation")).get("uri")
        if not isinstance(uri, str) or not uri:
            continue
        path = unquote(uri)
        if path[:7].lower() == "file://":
            path = path[7:]
        if path.startswith("./"):
            path = path[2:]
        parts = path.split("/")
        indexes = [index for index, part in enumerate(parts) if part == root]
        if not indexes:
            continue
        file = "/".join(parts[indexes[-1]:])
        region = object_value(physical.get("region"))
        start = region.get("startLine")
        end = region.get("endLine")
        if type(start) is not int or start < 1:
            start = end = None
        else:
            end = max(start, end) if type(end) is int else start
        rule = next((rule for rule in rules if rule.get("id") == result.get("ruleId")), {})
        rule_id = result.get("ruleId")
        rule_id = rule_id if isinstance(rule_id, str) else None
        text = object_value(result.get("message")).get("text")
        packages = {normalized_package(token.strip("._-")) for token in PACKAGE_TOKEN.findall(text)} if isinstance(text, str) else set()
        yield {
            "file": file,
            "start": start,
            "end": end,
            "classes": result_classes(result, rule, tool),
            "packages": packages,
            "key": (rule_id, file, start, end),
        }


def matches(finding, defect):
    if finding["file"] != defect["file"] or defect["class"] not in finding["classes"]:
        return False
    if defect["class"] == "vulnerable-dependency":
        return normalized_package(defect["package"]) in finding["packages"]
    return (finding["start"] is not None and finding["start"] <= defect["end_line"]
            and defect["start_line"] <= finding["end"])


def ratio(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else None


def confusion_matrix(labels, documents):
    by_tool = {}
    for document in documents:
        for run in array_value(object_value(document).get("runs")):
            if not isinstance(run, dict):
                continue
            tool = tool_id(run)
            found, false_positives = by_tool.setdefault(tool, (set(), set()))
            for finding in findings(run, labels["set"], tool):
                matched = {defect["id"] for defect in labels["defects"] if matches(finding, defect)}
                found.update(matched)
                if not matched:
                    false_positives.add(finding["key"])
    tools = {}
    for tool, (found, false_positives) in sorted(by_tool.items()):
        tp = len(found)
        fp = len(false_positives)
        fn = len(labels["defects"]) - tp
        tools[tool] = {"tp": tp, "fp": fp, "fn": fn, "precision": ratio(tp, tp + fp),
                       "recall": ratio(tp, tp + fn), "f1": ratio(2 * tp, 2 * tp + fp + fn)}
    return {"set": labels["set"], "defects": len(labels["defects"]), "tools": tools}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labels", required=True)
    parser.add_argument("sarif", nargs="+")
    args = parser.parse_args()
    with open(args.labels, encoding="utf-8") as stream:
        labels = json.load(stream)
    documents = []
    for path in args.sarif:
        with open(path, encoding="utf-8") as stream:
            documents.append(json.load(stream))
    json.dump(confusion_matrix(labels, documents), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
