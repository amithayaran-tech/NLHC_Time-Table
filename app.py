import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="NLHC Room Availability",page_icon="🏫",layout="wide")
DATA=Path(__file__).parent/"data"

ROOMS=[]
for i in range(1,17):
    ROOMS.append({"display_room":f"LH-{i}","floor":"Ground Floor" if i<=8 else "First Floor","source_room_no":f"NLHC-II-G{i}"})
for i in range(1,17):
    ROOMS.append({"display_room":f"CR-{i}","floor":"Third Floor","source_room_no":f"NLHC-II-C{i}"})
ROOMS += [{"display_room":"CR-17","floor":"Fourth Floor","source_room_no":"NLHC-II-C19"},
          {"display_room":"CR-18","floor":"Fourth Floor","source_room_no":"NLHC-II-C20"}]

@st.cache_data
def load(path):
    t=pd.read_excel(path,sheet_name="Timetable",dtype=str).fillna("")
    r=pd.read_excel(path,sheet_name="Rooms",dtype=str).fillna("")
    return t,r

st.title("🏫 NLHC Class-Room Availability Dashboard")
st.caption("Time-Table checker — made by:- Amit Hayaran.")

files=sorted(DATA.glob("*.xlsx"))
if not files:
    st.error("No Excel file found in data/")
    st.stop()
names=[x.name for x in files]
choice=st.sidebar.selectbox("Session / Excel",names)
tt,rm=load(DATA/choice)

days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day=st.sidebar.selectbox("Day",days,index=1)
slots=sorted(tt["slot"].unique(),key=lambda x:str(x))
slot=st.sidebar.selectbox("Slot",slots)

rtype=st.sidebar.selectbox("Room Type",["All Rooms","LH Only","CR Only"])
floor=st.sidebar.selectbox("Floor",["All Floors","Ground Floor","First Floor","Third Floor","Fourth Floor"])

r=rm.copy()
if rtype=="LH Only": r=r[r.display_room.str.startswith("LH-")]
if rtype=="CR Only": r=r[r.display_room.str.startswith("CR-")]
if floor!="All Floors": r=r[r.floor.eq(floor)]

m=tt[(tt.day.eq(day))&(tt.slot.eq(slot))]
occ=set(m.room_no)
r["status"]=r.source_room_no.map(lambda x:"Occupied" if x in occ else "Available")

a=r[r.status.eq("Available")]
o=r[r.status.eq("Occupied")]

x,y,z=st.columns(3)
x.metric("Total Rooms",len(r)); y.metric("Available",len(a)); z.metric("Occupied",len(o))
st.subheader(f"{day} • {slot}")

t1,t2,t3=st.tabs(["🟢 Available","🔴 Occupied","📋 Full Chart"])
with t1:
    st.dataframe(a[["display_room","floor"]].rename(columns={"display_room":"Room","floor":"Floor"}),use_container_width=True,hide_index=True)
with t2:
    details=m[["room_no","sub_name","sub_code"]].drop_duplicates("room_no")
    o2=o.merge(details,left_on="source_room_no",right_on="room_no",how="left")
    st.dataframe(o2[["display_room","floor","sub_name","sub_code"]].rename(columns={"display_room":"Room","floor":"Floor","sub_name":"Class / Subject","sub_code":"Code"}),use_container_width=True,hide_index=True)
with t3:
    st.dataframe(r[["display_room","floor","status"]].rename(columns={"display_room":"Room","floor":"Floor","status":"Status"}),use_container_width=True,hide_index=True)

st.divider()
st.subheader("📅 Room-wise weekly schedule")
room=st.selectbox("Select Room",r.display_room.tolist())
source=dict(zip(rm.display_room,rm.source_room_no))[room]
sch=tt[tt.room_no.eq(source)][["day","slot","sub_name","sub_code"]]
st.dataframe(sch.rename(columns={"day":"Day","slot":"Slot","sub_name":"Class / Subject","sub_code":"Code"}),use_container_width=True,hide_index=True)
st.caption("Available = no academic timetable entry for the selected day/slot. Exams, administrative bookings and other allotments are not included unless entered in Excel.")
