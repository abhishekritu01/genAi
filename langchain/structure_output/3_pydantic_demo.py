from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Student(BaseModel):
    name: str = 'Abhishek'
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(..., gt=0.0, lt=10.0, description="CGPA must be between 0 and 10")


new_student = Student(name="Abhishek", age=25, email="abhishek@gmail.com", cgpa=8.5)

student = Student(**new_student.model_dump())

print(student)