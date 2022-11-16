from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class Todo():
    id = 1
    title = ''
    is_completed = False

    def __init__(self, id, title, is_completed=False):
        self.id = id
        self.title = title
        self.is_completed = is_completed
    
    def __str__(self):
        return f'id:{self.id}, title:{self.title}, is_completed:{self.is_completed}'

todo = Todo(1, '수학숙제', False)
todos = [todo, Todo(2, '배드민턴 치기', False), Todo(3, '코딩공부')]
next_id = len(todos) + 1

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    global next_id
    title = request.form.get('title')
    new_todo = Todo(next_id, title)
    todos.append(new_todo)
    next_id += 1
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    global next_id
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            next_id -= 1
            break
    return redirect('/')

@app.route('/change_state/<int:todo_id>')
def change_state(todo_id):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index].is_completed = not todos[index].is_completed
            break
    return redirect('/')

@app.route('/delete_all')
def delete_all():
    global next_id, todos
    todos = []
    next_id = 1
    return redirect('/')

@app.route('/complate_all')
def complate_all():
    for todo in todos:
        todo.is_completed = True
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)