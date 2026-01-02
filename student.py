import sqlite3
import streamlit as st
from time import sleep

# ---------- DATABASE ----------
db = sqlite3.connect("management.db", check_same_thread=False)
cur = db.cursor()

#--------lOGIN-FUNCTION--------
def login():
    st.subheader("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "Admin@123":
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")
            
#------------ADD-STUDENT--------------
            
def add_student():
    st.subheader("Add Student")

    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    dob = st.date_input("Date of Birth")
    gender = st.radio("Gender", ["male", "female"])
    address = st.text_area("Address")
    photo = st.file_uploader("Upload Photo", ["jpg", "png"])

    if st.button("Insert"):
        if photo is None:
            st.warning("Upload photo first")
            return

        try:
            cur.execute(
                "INSERT INTO student VALUES (NULL,?,?,?,?,?,?)",
                (name, phone, dob, gender, address, photo.read())
            )
            db.commit()
            st.success("Student added successfully 🎉")
        except Exception as e:
            st.error(e)
            
#----------REMOVE-STUDENT--------------
            
def remove_student():
    st.subheader("Remove Student")

    name = st.text_input("Name")
    phone = st.text_input("Phone Number")

    if st.button("Delete"):
        cur.execute(
            "DELETE FROM student WHERE sname=? AND phno=?",
            (name, phone)
        )
        db.commit()

        if cur.rowcount == 0:
            st.warning("Record not found ❗")
        else:
            st.success("Record deleted 🗑️")
            
#----------UPDATE-STUDENT-----------
def update_student():
    st.subheader("Update Student")

    name = st.text_input("Existing Name")
    phone = st.text_input("Existing Phone")

    if st.button("Find"):
        data = cur.execute(
            "SELECT * FROM student WHERE sname=? AND phno=?",
            (name, phone)
        ).fetchone()

        if data is None:
            st.error("Student not found ❌")
            return

        field = st.selectbox(
            "What to update?",
            ["Name", "Phone", "DOB", "Gender", "Address"]
        )

        new_value = st.text_input("New Value")

        column_map = {
            "Name": "sname",
            "Phone": "phno",
            "DOB": "dob",
            "Gender": "gender",
            "Address": "address"
        }

        if st.button("Update"):
            cur.execute(
                f"UPDATE student SET {column_map[field]}=? WHERE sname=? AND phno=?",
                (new_value, name, phone)
            )
            db.commit()
            st.success("Updated successfully ✨")
            
#-------DISPLAY-STUDENT-----------
            
def display_student():
    st.subheader("Display Student")

    name = st.text_input("Name")
    phone = st.text_input("Phone")

    if st.button("Show"):
        data = cur.execute(
            "SELECT * FROM student WHERE sname=? AND phno=?",
            (name, phone)
        ).fetchone()

        if data:
            st.success(f"""
            Name: {data[1]}
            Phone: {data[2]}
            DOB: {data[3]}
            Gender: {data[4]}
            Address: {data[5]}
            """)
        else:
            st.error("Record not found")

#-------------MAIN-FLOW-----------
            
            
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    menu = st.radio(
        "Choose option",
        ["Add", "Remove", "Update", "Display"]
    )

    if menu == "Add":
        add_student()
    elif menu == "Remove":
        remove_student()
    elif menu == "Update":
        update_student()
    else:
        display_student()
else:
    login()





