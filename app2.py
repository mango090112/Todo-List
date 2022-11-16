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

titles = []
with open('titles.txt', 'r', encoding="UTF-8") as f:
    for line in f.readlines():
        titles.append(line.strip())
print(titles)

todos = []
next_id = 1
for title in titles:
    todos.append(Todo(next_id, title))
    next_id += 1

def write_file():
    with open('titles.txt', 'w', encoding="UTF-8") as f:
        for todo in todos:
            f.write(todo.title + '\n')

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
    write_file()
    return redirect('/')

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    global next_id
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            next_id -= 1
            break
    write_file()
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
    write_file()
    return redirect('/')

@app.route('/complate_all')
def complate_all():
    for todo in todos:
        todo.is_completed = True
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
