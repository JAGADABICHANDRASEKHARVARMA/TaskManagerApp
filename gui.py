import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=50)
        self.listbox.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_tasks)
        self.refresh_button.pack()

        self.new_task_button = tk.Button(root, text="New Task", command=self.new_task)
        self.new_task_button.pack()

        self.edit_task_button = tk.Button(root, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack()

        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack()

        self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        tasks = self.get_tasks()
        for task in tasks:
            self.listbox.insert(tk.END, f"{task['id']}: {task['title']} (Due Date: {task['due_date']})")

    def get_tasks(self):
        response = requests.get('http://127.0.0.1:5000/tasks')
        return response.json().get('tasks', [])

    def new_task(self):
        title = simpledialog.askstring("New Task", "Enter the task title:")
        due_date = simpledialog.askstring("New Task", "Enter the due date (YYYY-MM-DD):")
        if title and due_date:
            response = requests.post('http://127.0.0.1:5000/tasks', json={'title': title, 'due_date': due_date})
            self.refresh_tasks()

    def edit_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_id = int(self.listbox.get(selected_index).split(':')[0])
            title = simpledialog.askstring("Edit Task", "Enter the new task title:")
            due_date = simpledialog.askstring("Edit Task", "Enter the new due date (YYYY-MM-DD):")
            if title and due_date:
                response = requests.put(f'http://127.0.0.1:5000/tasks/{task_id}', json={'title': title, 'due_date': due_date})
                self.refresh_tasks()

    def delete_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            task_id = int(self.listbox.get(selected_index).split(':')[0])
            response = requests.delete(f'http://127.0.0.1:5000/tasks/{task_id}')
            self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
