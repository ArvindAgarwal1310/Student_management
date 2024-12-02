from fastapi import FastAPI, HTTPException, Query, Response
from typing import Optional
from utils import get_unique_id
from database import Database_ops
from models import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse


database_obj = Database_ops()
students_collection = database_obj.students_collection

app = FastAPI(
    title="Backend Intern Hiring Task",
    description="APIs to manage student data using FastAPI and MongoDB.",
    version="1.0.0",
)

#Base
@app.head("/")
async def head_root(response: Response):
    response.headers["X-App-Info"] = "APIs to manage student data using FastAPI and MongoDB."
    return Response(status_code=200)
# Route to add a new student
@app.post("/students", status_code=201)
async def create_student(student: StudentCreate):
    try:
        student_dict = student.dict()
        custom_id = get_unique_id(length=8)  # Unique ID for student of length 8
        student_dict["id"] = custom_id
        result = students_collection.insert_one(
            student_dict
        )  # Stores the _id after insertion
        return {"id": str(custom_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Route to get a student by ID
@app.get("/students/{id}", response_model=StudentResponse)
async def fetch_student(id: str):
    try:
        student = students_collection.find_one({"id": id})
        if not student:
            # Return a 204 response with no content
            return Response(status_code=204)
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Route to get all students
@app.get("/students", response_model=StudentListResponse)
async def list_students(
    country: Optional[str] = Query(None), age: Optional[int] = Query(None)
):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}

        students = list(students_collection.find(query))
        # Transform the students to match the desired structure
        response_data = [
            {"name": student.get("name"), "age": student.get("age")}
            for student in students
        ]

        return {"data": response_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Route to update a student
@app.patch("/students/{id}")
async def update_student(id: str, student_update: StudentUpdate):
    try:
        # Retrieve the existing student document
        existing_student = students_collection.find_one({"id": id})
        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Convert Pydantic model to a dictionary
        update_data = student_update.dict(exclude_unset=True)

        # Handle nested updates for `address`
        if "address" in update_data and existing_student.get("address"):
            # Merge existing `address` with the new updates
            update_data["address"] = {
                **existing_student["address"],
                **update_data["address"],
            }

        # Perform the update
        result = students_collection.update_one({"id": id}, {"$set": update_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete a student
@app.delete("/students/{id}", status_code=204)
async def delete_student(id: str):
    try:
        result = students_collection.delete_one({"id": id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
