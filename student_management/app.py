import os
import csv
import streamlit as st

from models import Student

def main():
    st.set_page_config(page_title="Student Management System", page_icon="📚")
    
    st.title("Students: ")
    
    if "students" not in st.session_state:
        st.session_state.students = read_students()
    
    if "roll_no" not in st.session_state:
        st.session_state.roll_no = st.session_state.students[-1].roll_no + 1 if len(st.session_state.students) > 0 else 1
    
    with st.sidebar:
        st.header("Add Student")
        
        roll_no = st.number_input("Roll No", value=st.session_state.roll_no, disabled=True)
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=17, max_value=100)
        branch = st.selectbox("Branch", [branch.value for branch in Student.BranchEnum]).strip()
        
        if st.button("Add Student"):
            try:
                add_student(roll_no, name, age, branch)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    for student in st.session_state.students:
        with st.expander(f"**Student Roll No: {student.roll_no}**", expanded=True):
            st.write(f"**Name:** {student.name}")
            st.write(f"**Age:** {student.age}")
            st.write(f"**Branch:** {student.branch.value}")

def add_student(roll_no, name, age, branch):
    try:
        if not name:
            raise ValueError("Name cannot be empty")
        student = Student(  
            roll_no=roll_no,
            name=name,
            age=age,
            branch=branch
        )
        
        st.session_state.students.append(student)
        
        with open("students.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["roll_no", "name", "age", "branch"])
            
            writer.writerow({
                "roll_no": student.roll_no,
                "name": student.name,
                "age": student.age,
                "branch": student.branch
            })
        
        st.session_state.roll_no += 1
    except Exception as e:
        st.error(f"Failed to add student: {e}")
        
def read_students():
    students = []
    
    if os.path.exists("students.csv"):
        with open("students.csv", "r") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                student = Student(
                    roll_no=int(row["roll_no"]),
                    name=row["name"],
                    age=int(row["age"]),
                    branch=Student.BranchEnum(row["branch"])
                )
                
                students.append(student)
    else:
        with open("students.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=["roll_no", "name", "age", "branch"])
            writer.writeheader()
    
    return students
    
if __name__ == "__main__":
    main()