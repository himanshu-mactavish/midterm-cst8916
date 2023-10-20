from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory database (a list of student dictionaries)
students = [
    {"id": 1, "name": "Himanshu", "grade": "B"},
]

# Pydantic model for Student data
class Student(BaseModel):
    id: int
    name: str
    grade: str

# Create a new student
@app.post("/students/", response_model=Student)
def create_student(student: Student):
    students.append(student)
    return student

# Read a student by ID
@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    student = next((s for s in students if s.id == student_id), None)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Update a student by ID
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for i, student in enumerate(students):
        if student.id == student_id:
            students[i] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

# Delete a student by ID
@app.delete("/students/{student_id}", response_model=Student)
def delete_student(student_id: int):
    for i, student in enumerate(students):
        if student.id == student_id:
            deleted_student = students.pop(i)
            return deleted_student
    raise HTTPException(status_code=404, detail="Student not found")

# Get a list of all students
@app.get("/students/", response_model=list[Student])
def get_students():
    return students
