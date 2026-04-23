import pandas as pd
from datetime import datetime
import time

print(" (Simulating)")
time.sleep(2)
print("[SUCCESS] ")

try:
    attendance_df = pd.read_csv('Attendance_Log.csv')
except:
    attendance_df = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])

now = datetime.now()
dateString = now.strftime('%Y-%m-%d')
timeString = now.strftime('%H:%M:%S')

attendance_df.loc[len(attendance_df)] = ["999", "Prakhar (Live Capture)", dateString, timeString]


attendance_df.to_csv('Attendance_Log.csv', index=False)
print("")