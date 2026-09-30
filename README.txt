NLHC Room Availability App
==========================
Run:
  pip install -r requirements.txt
  streamlit run app.py
or double-click run_app.bat on Windows.

For a new session, place the new Excel file in data/.
Required sheet: Timetable
Columns: session_year, sub_name, sub_code, sub_type, sub_category, ltp, day, slot, room_no

Room mapping:
LH-1 to LH-8  = Ground Floor
LH-9 to LH-16 = First Floor
CR-1 to CR-16  = Third Floor
CR-17          = source code NLHC-II-C19 = Fourth Floor
CR-18          = source code NLHC-II-C20 = Fourth Floor

The app uses the Excel selected in the sidebar, so the code does not need to be changed for a new session.
