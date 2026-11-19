import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Record Management System")
st.title("Student Record Management System")

# Default 3 students (sirf pehli baar load hote hain)
if "students" not in st.session_state:
    st.session_state.students = [
        {"Roll No": 101, "Name": "Aman Sharma", "Course": "B.Tech CSE", "Marks": 85},
        {"Roll No": 102, "Name": "Simran Kaur", "Course": "BCA", "Marks": 78},
        {"Roll No": 103, "Name": "Rohit Verma", "Course": "B.Tech IT", "Marks": 92},
    ]

students = st.session_state.students


def find_student(roll):
    for s in students:
        if s["Roll No"] == roll:
            return s
    return None


tab_add, tab_update, tab_delete, tab_view = st.tabs(
    ["➕ Add Student", "✏️ Update Student", "🗑️ Delete Student", "📋 View Students"]
)

# ---------- ADD ----------
with tab_add:
    st.subheader("Add New Student")
    with st.form("add_form", clear_on_submit=True):
        roll = st.number_input("Roll No", min_value=1, step=1, key="add_roll")
        name = st.text_input("Name", key="add_name")
        course = st.text_input("Course", key="add_course")
        marks = st.number_input("Marks", min_value=0, max_value=100, step=1, key="add_marks")
        submitted = st.form_submit_button("Add Student")

    if submitted:
        if not name.strip() or not course.strip():
            st.error("Name aur Course khali nahi ho sakte.")
        elif find_student(int(roll)):
            st.error(f"Roll No {int(roll)} pehle se maujood hai.")
        else:
            students.append(
                {"Roll No": int(roll), "Name": name.strip(),
                 "Course": course.strip(), "Marks": int(marks)}
            )
            st.success(f"{name} add ho gaya!")

# ---------- UPDATE ----------
with tab_update:
    st.subheader("Update Student")
    if not students:
        st.info("Update karne ke liye koi student nahi hai.")
    else:
        rolls = [s["Roll No"] for s in students]
        sel = st.selectbox("Roll No chuno", rolls, key="upd_select")
        current = find_student(sel)

        with st.form("update_form"):
            new_name = st.text_input("Name", value=current["Name"], key=f"upd_name_{sel}")
            new_course = st.text_input("Course", value=current["Course"], key=f"upd_course_{sel}")
            new_marks = st.number_input(
                "Marks", min_value=0, max_value=100, step=1,
                value=int(current["Marks"]), key=f"upd_marks_{sel}",
            )
            upd = st.form_submit_button("Update Student")

        if upd:
            if not new_name.strip() or not new_course.strip():
                st.error("Name aur Course khali nahi ho sakte.")
            else:
                current["Name"] = new_name.strip()
                current["Course"] = new_course.strip()
                current["Marks"] = int(new_marks)
                st.success(f"Roll No {sel} update ho gaya!")

# ---------- DELETE ----------
with tab_delete:
    st.subheader("Delete Student")
    if not students:
        st.info("Delete karne ke liye koi student nahi hai.")
    else:
        options = {f'{s["Roll No"]} - {s["Name"]}': s["Roll No"] for s in students}
        choice = st.selectbox("Student chuno", list(options.keys()), key="del_select")
        if st.button("Delete Student", type="primary"):
            roll_to_delete = options[choice]
            st.session_state.students = [
                s for s in students if s["Roll No"] != roll_to_delete
            ]
            st.toast(f"{choice} delete ho gaya!")
            st.rerun()

# ---------- VIEW ----------
with tab_view:
    st.subheader("All Students")
    if not students:
        st.info("Abhi koi student nahi hai.")
    else:
        df = pd.DataFrame(students)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.caption(f"Total students: {len(students)}")