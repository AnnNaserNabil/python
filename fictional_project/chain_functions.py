def function_four(initial_task_description):
    return {
        'description': initial_task_description,
        'status': 'pending',
        'importance': 'normal'
    }

def function_three(task, action, value=None):
    if action == 'mark_done':
        task['status'] = 'completed'
    elif action == 'mark_important':
        task['importance'] = 'high'
    return task

def function_two(tasks_list, target_identifier, operation_details):
    if operation_details['type'] == 'add':
        new_task = function_four(target_identifier) # target_identifier is description
        tasks_list.append(new_task)
    elif operation_details['type'] == 'modify':
        task_to_modify = target_identifier # This is the actual task object
        action = operation_details['action']
        if task_to_modify in tasks_list: # Check if the object is in the list
            function_three(task_to_modify, action)
        else:
            # This case should ideally not be hit if target_identifier is obtained correctly from the list
            print(f"Warning: Task object to modify not found in list.")
    return tasks_list

def function_one(initial_task_descriptions, operations_to_perform):
    current_tasks = []

    # Initial task creation
    for desc in initial_task_descriptions:
        function_two(current_tasks, desc, {'type': 'add'})

    # Perform further operations
    for op in operations_to_perform:
        if op['type'] == 'add':
            function_two(current_tasks, op['description'], {'type': 'add'})
        elif op['type'] == 'modify':
            task_to_modify = None
            for task in current_tasks:
                if task['description'] == op['task_description_to_find']:
                    task_to_modify = task
                    break

            if task_to_modify:
                function_two(current_tasks, task_to_modify, {'type': 'modify', 'action': op['action']})
            else:
                print(f"Warning: Task with description '{op['task_description_to_find']}' not found for modification.")

    return current_tasks

if __name__ == "__main__":
    print("--- To-Do List Example ---")

    initial_tasks = [
        "Buy groceries",
        "Read a chapter of a book",
        "Go for a run"
    ]

    operations = [
        {'type': 'add', 'description': 'Schedule dentist appointment'},
        {'type': 'modify', 'task_description_to_find': 'Buy groceries', 'action': 'mark_important'},
        {'type': 'modify', 'task_description_to_find': 'Go for a run', 'action': 'mark_done'},
        {'type': 'modify', 'task_description_to_find': 'Read a chapter of a book', 'action': 'mark_important'},
        {'type': 'add', 'description': 'Pay bills'},
        {'type': 'modify', 'task_description_to_find': 'Pay bills', 'action': 'mark_important'},
    ]

    final_task_list = function_one(initial_tasks, operations)

    print("\n--- All Tasks ---")
    for task in final_task_list:
        print(f"- {task['description']} (Status: {task['status']}, Importance: {task['importance']})")

    print("\n--- Important Tasks ---")
    important_tasks = [task for task in final_task_list if task['importance'] == 'high']
    if important_tasks:
        for task in important_tasks:
            print(f"- {task['description']} (Status: {task['status']})")
    else:
        print("No important tasks.")

    print("\n--- Pending Tasks ---")
    pending_tasks = [task for task in final_task_list if task['status'] == 'pending']
    if pending_tasks:
        for task in pending_tasks:
            print(f"- {task['description']} (Importance: {task['importance']})")
    else:
        print("No pending tasks.")

    print("\n--- Completed Tasks ---")
    completed_tasks = [task for task in final_task_list if task['status'] == 'completed']
    if completed_tasks:
        for task in completed_tasks:
            print(f"- {task['description']} (Importance: {task['importance']})")
    else:
        print("No completed tasks yet.")
