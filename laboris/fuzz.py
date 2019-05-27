"""
Python based fuzzy finder
"""

from math import inf

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1.lower() != c2.lower())
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def fuzz(src, data, dist=levenshtein, size=5):
    results = [(inf, "")] * size
    for string in data:
        distance = dist(src, string)
        for i, pos in enumerate(results):
            if pos[0] > distance:
                results.insert(i, (distance, string))
                results.pop()
                break
    return [x[1] for x in results]

def weighted_fuzz(src, data, dist=levenshtein, size=5):
    results = [(inf, "")] * size
    for string, weight in data:
        distance = dist(src, string) + weight
        for i, pos in enumerate(results):
            if pos[0] > distance:
                results.insert(i, (distance, string))
                results.pop()
                break
    return [x[1] for x in results]
