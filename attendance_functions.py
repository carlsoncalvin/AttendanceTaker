# -*- coding: utf-8 -*-

import glob
import numpy as np
import pandas as pd
from itertools import islice

# make lists for input responses
yes = ["y", "Y", "", "Yes", "yes"]
no = ["n", "N", "No", "no"]

def check_attendance(attendance_df):
    all_names = attendance_df["First name"] + " " + attendance_df["Last name"]
    attend = attendance_df.iloc[:, 6:].astype(int)
    attend_totals = attend.sum(axis=1)
    attend_pct = attend_totals / attend_totals.max()

    num_absences = np.sum(attend == 0, axis=1)

    people_at_risk = all_names[num_absences > 2]

    att_check = pd.DataFrame({
        "People at Risk"    : people_at_risk,
        "Number of Absences": num_absences[num_absences > 2]
    })

    print(att_check, "\n")

def take_attendance(attendance):
    # get names columns
    names = attendance["First name"] + " " + attendance["Last name"]

    # create new column for date
    file = glob.glob("*.txt")
    if len(file) > 1:
        raise Exception("Multiple files found. Delete old")
    elif len(file) == 0:
        raise Exception("No file found. Please include text file")

    error = 0

    with open(file[0], "r") as f:
        for line in f:
            if line.startswith("Wednesday"):
                date = line.split()[2] + " " + line.split()[1]
                break

    print(f"Date found: {date}. Is this correct? [Y]/n")
    if input() in yes:
        pass
    else:
        raise Exception("Wrong date identified. Check file integrity")

    attendance[date] = np.zeros_like(names)

    with open(file[0], "r") as f:
        f_iter = iter(f)
        for count, line in enumerate(f):
            name = line.strip()
            if name in names.values:
                date_line = next(islice(f_iter, 4, 5), '')
                if date_line.startswith(f"Wednesday, {date.split()[1]} {date.split()[0]}"):
                    bool_of_names = names.str.contains(name)
                    name_count = bool_of_names.sum()
                    if name_count == 1:
                        print(f"Name Found. Attendance logged for {names[names.str.contains(name)].values[0]}")
                        attendance.loc[bool_of_names, date] = 1
                    elif name_count == 0:
                        print("\nNo hits on that name. Try again.")
                        error += 1
                    elif name_count > 1:
                        print(f"Multiple hits ({name_count}) on that name. Try again.")
                        error += 1
                else:
                    print(f"{name} submitted outside of class on {date_line}. Attendance not logged.")

    # save CSV
    if error == 0:
        print("\nNo Errors")
    else:
        print(f"\nWARNING: {error} errors during runtime.\n")

    print(attendance)

    print("\nSave Modified attendance record? [Y],n")
    result = None
    while result is None:
        try:
            response = input()
            if response in yes:
                attendance.to_csv("attendance.csv", index=False)
                print("\nCSV saved. Exiting.")
                check_attendance(attendance)
                result = 1
            elif response in no:
                print("\nCSV not saved. Exiting.\n")
                check_attendance(attendance)
                result = 1
            else:
                print("Invalid response. Try again.")
                raise Exception
        except:
            pass


def see_absences(attendance):
    # get names columns
    full_names = attendance["First name"] + " " + attendance["Last name"]
    first_names = pd.Series([name.split()[0] for name in attendance["First name"]])

    print("Please input student's name:")
    name = input()
    print("\n")
    if name in full_names.values:
        names = full_names
    elif name in first_names.values:
        names = first_names
    else:
        raise Exception("Name not found\n")

    bool_of_names = names.str.contains(name)
    name_count = bool_of_names.sum()
    if name_count == 1:
        name_line = attendance.loc[bool_of_names, :]
        # cut out student info
        name_line = pd.concat([name_line.iloc[:, 0:2], name_line.iloc[:, 6:]], axis=1)

        absent_dates = name_line.columns[name_line.eq("0").all()].values

        if len(absent_dates) == 0:
            print(f"{name} has not been registered as absent\n")
        else:
            print(f"{name} has been absent on {absent_dates}")

        print()
    elif name_count == 0:
        print("No hits on that name. Try again.\n")
    elif name_count > 1:
        print(f"Multiple hits ({name_count}) on that name. Try again.\n")
