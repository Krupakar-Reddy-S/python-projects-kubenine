from pydantic import BaseModel
from enum import Enum

class Student(BaseModel):
    roll_no: int = None
    name: str
    age: int
    
    class BranchEnum(str, Enum):
        CSE = "Computer Science"
        ECE = "Electronics and Communication"
        ME = "Mechanical"
        CE = "Civil"

    branch: BranchEnum