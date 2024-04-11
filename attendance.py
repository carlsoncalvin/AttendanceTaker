# -*- coding: utf-8 -*-
import pandas as pd
import attendance_functions as af

# check if attendance file exits
try:
    attendance = pd.read_csv("attendance.csv", dtype=str)
except Exception as e:
    print(f"Error: {e}\nPlease add a file attendance.csv.\n")
    exit()

done = False
while not done:
    print("Would you like to:\n"
          "[1] Take attendance\n"
          "[2] See an individual's absences\n"
          "[3] See who has too many absences\n"
          "[4] Exit\n")
    response = input()
    if response == "1":
        try:
            af.take_attendance(attendance)
        except Exception as e:
            print(f"Error: {e}")
    elif response == "2":
        try:
            af.see_absences(attendance)
        except Exception as e:
            print(f"Error: {e}")
    elif response == "3":
        try:
            af.check_attendance(attendance)
        except Exception as e:
            print(f"Error: {e}")
    elif response =="4":
        done = True
    else:
        print("Unrecognized Response\n")