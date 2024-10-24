# -*- coding: utf-8 -*-
"""python_section_1.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MAsZqFUN4cW02YBpKTYJnEA19BGn_1rg

Q1. Problem Statement:

Write a function that takes a list and an integer n, and returns the list with every group of n elements reversed. If there are fewer than n elements left at the end, reverse all of them.

Requirements:

You must not use any built-in slicing or reverse functions to directly reverse the sublists.

The result should reverse the elements in groups of size n.
"""

def reverse_in_groups(lst, n):
    for i in range(0, len(lst), n):
        left = i
        right = min(i + n - 1, len(lst) - 1)
        while left < right:
            lst[left], lst[right] = lst[right], lst[left]
            left += 1
            right -= 1
    return lst

print(reverse_in_groups([1, 2, 3, 4, 5, 6, 7, 8], 3))
print(reverse_in_groups([1, 2, 3, 4, 5], 2))
print(reverse_in_groups([10, 20, 30, 40, 50, 60, 70], 4))

"""Q2. Problem Statement:

Write a function that takes a list of strings and groups them by their length. The result should be a dictionary where:

The keys are the string lengths.

The values are lists of strings that have the same length as the key.


Requirements:

Each string should appear in the list corresponding to its length.

The result should be sorted by the lengths (keys) in ascending order.
"""

def group_strings_by_length(strings):
    length_dict = {}
    for string in strings:
        length = len(string)
        if length in length_dict:
            length_dict[length].append(string)
        else:
            length_dict[length] = [string]
    return dict(sorted(length_dict.items()))

print(group_strings_by_length(["apple", "bat", "car", "elephant", "dog", "bear"]))
print(group_strings_by_length(["one", "two", "three", "four"]))

"""Q3. You are given a nested dictionary that contains various details (including lists and sub-dictionaries). Your task is to write a Python function that flattens the dictionary such that:

Nested keys are concatenated into a single key with levels separated by a dot (.).

List elements should be referenced by their index, enclosed in square brackets (e.g., sections[0]).



Requirements:

Nested Dictionary: Flatten nested dictionaries into a single level, concatenating keys.

Handling Lists: Flatten lists by using the index as part of the key.

Key Separator: Use a dot (.) as a separator between nested key levels.

Empty Input: The function should handle empty dictionaries gracefully.

Nested Depth: You can assume the dictionary has a maximum of 4 levels of nesting.
"""

def flatten_dict(d, parent_key=''):
    items = {}

    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.update(flatten_dict(item, f"{new_key}[{i}]"))
        else:
            items[new_key] = v
    return items

nested_dict = {"road": {"name": "Highway 1","length": 350,"sections": [{"id": 1, "condition": {"pavement": "good","traffic": "moderate"}}]}}

print(flatten_dict(nested_dict))

"""Q4. Problem Statement:

You are given a list of integers that may contain duplicates. Your task is to generate all unique permutations of the list. The output should not contain any duplicate permutations.
"""

def unique_permutations(nums):
    def backtrack(path, visited):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if visited[i] or (i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]):
                continue
            visited[i] = True
            path.append(nums[i])
            backtrack(path, visited)
            path.pop()
            visited[i] = False
    nums.sort()
    result = []
    visited = [False] * len(nums)
    backtrack([], visited)
    return result

print(unique_permutations([1, 1, 2]))

"""Q5. Problem Statement:

You are given a string that contains dates in various formats (such as "dd-mm-yyyy", "mm/dd/yyyy", "yyyy.mm.dd", etc.). Your task is to identify and return all the valid dates present in the string.

You need to write a function find_all_dates that takes a string as input and returns a list of valid dates found in the text. The dates can be in any of the following formats:

dd-mm-yyyy

mm/dd/yyyy

yyyy.mm.dd

You are required to use regular expressions to identify these dates.
"""

import re

def find_all_dates(text):
    pattern = r'\b(\d{2}-\d{2}-\d{4})\b|' \
              r'\b(\d{2}/\d{2}/\d{4})\b|' \
              r'\b(\d{4}\.\d{2}\.\d{2})\b'
    matches = re.findall(pattern, text)
    valid_dates = [date for group in matches for date in group if date]
    return valid_dates

text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
print(find_all_dates(text))

"""Q6. You are given a polyline string, which encodes a series of latitude and longitude coordinates. Polyline encoding is a method to efficiently store latitude and longitude data using fewer bytes. The Python polyline module allows you to decode this string into a list of coordinates.

Write a function that performs the following operations:

Decode the polyline string using the polyline module into a list of (latitude, longitude) coordinates.

Convert these coordinates into a Pandas DataFrame with the following columns:

latitude: Latitude of the coordinate.

longitude: Longitude of the coordinate.

distance: The distance (in meters) between the current row's coordinate and the previous row's one. The first row will have a distance of 0 since there is no previous point.

Calculate the distance using the Haversine formula for points in successive rows.
"""

pip install polyline

import polyline
import pandas as pd
from math import radians, cos, sin, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def decode_polyline_to_dataframe(polyline_str):
    coordinates = polyline.decode(polyline_str)
    df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
    distances = [0]  # First row distance is 0

    for i in range(1, len(df)):
        lat1, lon1 = df.iloc[i - 1][['latitude', 'longitude']]
        lat2, lon2 = df.iloc[i][['latitude', 'longitude']]
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        distances.append(distance)

    df['distance'] = distances
    return df

polyline_str = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
df = decode_polyline_to_dataframe(polyline_str)
print(df)

"""Q7: Write a function that performs the following operations on a square matrix (n x n):

Rotate the matrix by 90 degrees clockwise.

After rotation, for each element in the rotated matrix, replace it with the sum of all elements in the same row and column (in the rotated matrix), excluding itself.

The function should return the transformed matrix.
"""

def rotate_and_transform_matrix(matrix):
    n = len(matrix)

    rotated = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            rotated[j][n - 1 - i] = matrix[i][j]

    transformed = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated[i]) - rotated[i][j]
            col_sum = sum(rotated[k][j] for k in range(n)) - rotated[i][j]
            transformed[i][j] = row_sum + col_sum

    return transformed

# Example usage
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = rotate_and_transform_matrix(matrix)

for row in result:
    print(row)

"""Q8. You are given a dataset, dataset-1.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

Create a function that accepts dataset-1.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).
"""

import pandas as pd
df = pd.read_csv('dataset-1.csv')
print(df.head())
print(df.info())

WEEKDAY_MAP = {"Monday": 0, "Tuesday": 1, "Wednesday": 2,"Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

def check_timestamp_completeness(df):
    reference_date = pd.Timestamp('2024-01-01')
    df['start_date'] = df['startDay'].map(lambda x: reference_date + pd.Timedelta(days=WEEKDAY_MAP[x]))
    df['end_date'] = df['endDay'].map(lambda x: reference_date + pd.Timedelta(days=WEEKDAY_MAP[x]))
    df['start_datetime'] = pd.to_datetime(df['start_date'].astype(str) + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['end_date'].astype(str) + ' ' + df['endTime'])
    df.set_index(['id', 'id_2'], inplace=True)

    def check_group(group):
        all_days = set(group['start_datetime'].dt.date).union(group['end_datetime'].dt.date)
        expected_days = {reference_date.date() + pd.Timedelta(days=i) for i in range(7)}
        if not all_days.issuperset(expected_days):
            return True
        for day in expected_days:
            day_timestamps = group[
                (group['start_datetime'].dt.date <= day) &
                (group['end_datetime'].dt.date >= day)]
            full_day_hours = pd.date_range(start=f"{day} 00:00:00", end=f"{day} 23:59:59", freq='H')
            if not all(any(start <= hour <= end for start, end in zip(
                    day_timestamps['start_datetime'], day_timestamps['end_datetime']))
                    for hour in full_day_hours):
                return True
        return False

    result = df.groupby(level=[0, 1]).apply(check_group)
    return result

result_series = check_timestamp_completeness(df)
print(result_series)