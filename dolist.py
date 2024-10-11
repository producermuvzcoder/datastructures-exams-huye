todo_list = ["Buy groceries", "Clean the house", "Finish project", "Read a book"]
print("To-Do List before completing tasks:")
print(todo_list)
task_to_complete = "Clean the house"
if task_to_complete in todo_list:
    todo_list.remove(task_to_complete)
    print(f"\n'{task_to_complete}' has been completed and removed from the list.")
else:
    print(f"\n'{task_to_complete}' is not in the to-do list.")
print("\nTo-Do List after completing tasks:")
print(todo_list)