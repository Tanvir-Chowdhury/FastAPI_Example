from fastapi import FastAPI

api = FastAPI()

all_todos = [
    {'todo_id':1, 'todo_name':'Buy groceries', 'todo_description':'Milk, Bread, Eggs'},
    {'todo_id':2, 'todo_name':'Walk the dog', 'todo_description':'Take the dog to the park'},   
    {'todo_id':3, 'todo_name':'Read a book', 'todo_description':'Finish reading "1984" by George Orwell'},
    {'todo_id':4, 'todo_name':'Exercise', 'todo_description':'Go for a run or hit the gym'},
    {'todo_id':5, 'todo_name':'Learn a new skill', 'todo_description':'Start learning Python programming'},
]

@api.get("/api")
def index():
    return {"message": "Hello, World!"}  


@api.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return todo
    return {"error": "Todo not found"}, 404

@api.get("/todos")
async def get_todos(n: int = None):
    if n:
        return all_todos[:n]
    else:
        return all_todos

@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1
    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(new_todo)
    return new_todo


@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo: dict):
    for index, existing_todo in enumerate(all_todos):
        if existing_todo['todo_id'] == todo_id:
            all_todos[index] = {
                'todo_id': todo_id,
                'todo_name': todo['todo_name'],
                'todo_description': todo['todo_description']
            }
            return all_todos[index]
    return {"error": "Todo not found"}, 404


@api.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index, existing_todo in enumerate(all_todos):
        if existing_todo['todo_id'] == todo_id:
            del all_todos[index]
            return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}, 404


