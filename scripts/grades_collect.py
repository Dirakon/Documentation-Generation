#!/usr/bin/env python3

import os
import subprocess
import multiprocessing
from pathlib import Path
import sys
import time
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import json
from utils import *
import csv

def discard_version_if_present(name_with_potential_version: str):
    split_by_underscore = name_with_potential_version.split('_')
    if len(split_by_underscore) <= 1:
        return name_with_potential_version
    last_part = split_by_underscore[-1]
    if not last_part.isdigit():
        return name_with_potential_version
    return '_'.join(split_by_underscore[:-1])

def get_manual_graded_fields(file_content:str)->dict[str,str|float]:
    # Regular expression to match the key-value pairs
    pattern = r'(.*?): (.*?)\n'
    matches = re.findall(pattern, file_content)

    parsed_data = {}

    for key, value in matches:
        key = key.strip()
        value = value.strip().strip('"')
        if key not in ['Accuracy-note', 'Completeness-note', 'Relevance-note', 'Understandability-note', 'Formatting-note', 'General-note']:
            value = 0 if value == 'x' else float(value)
        parsed_data[key] = '' if value == 'x' else value
    return parsed_data

def main():
    results = []

    for model_dir_path in get_all_model_subdirectories():
        generated_mapping_file = model_dir_path / "mapping.json"
        generated_mapping_content:list[str] = json.loads(open(generated_mapping_file).read())

        for i, mapping in enumerate(generated_mapping_content):
            manual_grade_file = model_dir_path / str(i) / "grade" / "manual.txt"
            manual_grade_content = open(manual_grade_file).read()
            grades = get_manual_graded_fields(manual_grade_content)

            doctest_grade_file = model_dir_path / str(i) / "grade" / "doctest.txt"
            doctest_grade = float(open(doctest_grade_file).read().strip())
            grades['Model'] = model_dir_path.name
            grades['Doctest'] = doctest_grade
            grades['Answer'] = mapping
            grades['Prompt'] = discard_version_if_present(model_dir_path.parent.name)
            grades['Place'] = i

            results.append(grades)
    with open('grades.csv', 'w', newline='') as csvfile:
        fieldnames = ['Accuracy-note', 'Completeness-note', 'Relevance-note', 'Understandability-note', 'Formatting-note', 'Accuracy', 'Completeness', 'Relevance', 'Understandability', 'Formatting', 'General-note', 'Model', 'Answer', 'Prompt', 'Doctest', 'Place']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
