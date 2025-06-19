from enum import IntEnum
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 

api = FastAPI()


class Priority(IntEnum):
    low = 3
    medium = 2
    high = 1
    
class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo item")
    todo_description: str = Field(..., description="Description of the todo item")
    priority: Priority = Field(default=Priority.low, description="Priority of the todo item")
    
class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier for the todo item")
    
class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo item")
    todo_description: Optional[str] = Field(None, description="Description of the todo item")
    priority: Optional[Priority] = Field(None, description="Priority of the todo item")
    

all_todos = [
    Todo(todo_id=1, todo_name='Buy groceries', todo_description='Milk, Bread, Eggs', priority=Priority.low),
    Todo(todo_id=2, todo_name='Walk the dog', todo_description='Take the dog to the park', priority=Priority.medium),
    Todo(todo_id=3, todo_name='Read a book', todo_description='Finish reading "1984" by George Orwell', priority=Priority.high),
    Todo(todo_id=4, todo_name='Exercise', todo_description='Go for a run or hit the gym', priority=Priority.low),
    Todo(todo_id=5, todo_name='Learn a new skill', todo_description='Start learning Python programming', priority=Priority.medium),
]

@api.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
        
@api.get("/todo", response_model=List[Todo])
def get_todos(n: int= None):
    if n:
        return all_todos[:n]
    return all_todos

@api.post("/todo", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos)+1
    
    new_todo = Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    
    all_todos.append(new_todo)
    return new_todo
    
@api.put("/todos/{todo_id}", response_model = Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail="Todo not found")
                