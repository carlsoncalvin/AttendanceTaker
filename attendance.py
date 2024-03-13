# -*- coding: utf-8 -*-

import glob
import numpy as np
import pandas as pd
from itertools import islice

# make lists for input responses
yes = ["y", "Y", "", "Yes", "yes"]
no = ["n", "N", "No", "no"]

# check if attendance file exits
try:
    attendance = pd.read_csv("attendance.csv", dtype=str)
except Exception as e:
    print(f"Error: {e}\nCreate File 'attendance.csv'? [Y/n]")
    if input() in yes:
        with open('attendance.csv', 'w') as file:
            pass
        attendance = pd.read_csv("attendance.csv", dtype=str)
    else:
        print("\nNo File Created\nTerminating")
        exit()

# get names columns
names = attendance["First name"] + " " + attendance["Last name"]

# create new column for date
file = glob.glob("*.txt")
if len(file) > 1:
    print("Multiple files found. Delete old files")
    exit()
elif len(file) == 0:
    print("No file found. Please include text file")
    exit()

error = 0

with open(file[0], "r") as f:
    for line in f:
        if line.startswith("Wednesday"):
            date = line.split()[2] + " " + line.split()[1]
            break

print(f"Date found: {date}. Is this correct? [Y/n]")
if input() in yes:
    pass
else:
    print("Terminating Program. Check file integrity")
    exit()

attendance[date] = np.zeros_like(names)

with open(file[0], "r") as f:
    f_iter = iter(f)
    for count, line in enumerate(f):
        name = line.strip()
        if name in names.values:
            print(name)
            date_line = next(islice(f_iter, 4, 5), '')
            if date_line.startswith("Wednesday"):
                bool_of_names = names.str.contains(name)
                name_count = bool_of_names.sum()
                if name_count == 1:
                    print(f"Name Found. Attendance logged for {names[names.str.contains(name)].values[0]}\n")
                    attendance.loc[bool_of_names, date] = 1
                elif name_count == 0:
                    print("\nNo hits on that name. Try again.")
                    error += 1
                elif name_count > 1:
                    print(f"Multiple hits ({name_count}) on that name. Try again.")
                    error += 1
            else:
                print(f"{name} submitted outside of class on {date}. Attendance not logged.\n")

# save CSV
if error == 0:
    print("\nNo Errors")
else:
    print(f"\nWARNING: {error} errors during runtime.\n")

print(attendance)

print("\nSave Modified attendance record? [Y,n]")
result = None
while result is None:
    try:    
        response = input()
        if response in yes:
            attendance.to_csv("attendance.csv", index=False)
            print("\nCSV saved. Exiting.")
            result = 1
        elif response in no:
            print("\nCSV not saved. Exiting.")
            result = 1
        else:
            print("Invalid response. Try again.")
            raise Exception
    except:
        pass
