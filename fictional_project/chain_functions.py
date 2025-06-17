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
    # value parameter is not used by these actions but kept for potential extensibility
    return task

def function_two(tasks_list, target_identifier, operation_details):
    # Note: This function was designed for function_one to call it.
    # For direct interactive use, we might simplify or bypass it,
    # but let's try to use it.
    # 'target_identifier' for 'add' is description.
    # 'target_identifier' for 'modify' is the task object.
    if operation_details['type'] == 'add':
        new_task = function_four(target_identifier)
        # If operation_details contains initial status/importance, apply them
        if 'initial_status' in operation_details and operation_details['initial_status'] == 'completed':
            function_three(new_task, 'mark_done')
        if 'initial_importance' in operation_details and operation_details['initial_importance'] == 'high':
            function_three(new_task, 'mark_important')
        tasks_list.append(new_task)
    elif operation_details['type'] == 'modify':
        task_to_modify = target_identifier
        action = operation_details['action']
        if task_to_modify in tasks_list:
            function_three(task_to_modify, action)
        else:
            print(f"Warning: Task object to modify not found in list.")
    return tasks_list

# function_one is not directly used by the interactive menu, but keep it.
def function_one(initial_task_descriptions, operations_to_perform):
    current_tasks = []
    for desc in initial_task_descriptions:
        function_two(current_tasks, desc, {'type': 'add'})
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
    tasks_list = []
    print("--- Interactive To-Do List ---")

    while True:
        print("\nMenu:")
        print("1. Add new task")
        print("2. View tasks")
        print("3. Mark task as important")
        print("4. Mark task as done")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            description = input("Enter task description: ")
            importance_input = input("Mark as important? (yes/no, default: no): ").lower()
            status_input = input("Mark as initially done? (yes/no, default: no): ").lower()

            op_details = {'type': 'add'}
            if importance_input == 'yes':
                op_details['initial_importance'] = 'high'
            if status_input == 'yes':
                op_details['initial_status'] = 'completed'

            function_two(tasks_list, description, op_details)
            print(f"Task '{description}' added.")

        elif choice == '2':
            if not tasks_list:
                print("No tasks to show.")
            else:
                print("\n--- Current Tasks ---")
                for i, task in enumerate(tasks_list):
                    print(f"{i+1}. {task['description']} (Status: {task['status']}, Importance: {task['importance']})")

        elif choice == '3' or choice == '4': # Mark important or Mark done
            if not tasks_list:
                print("No tasks to modify.")
                continue

            print("\n--- Current Tasks ---")
            for i, task in enumerate(tasks_list):
                print(f"{i+1}. {task['description']} (Status: {task['status']}, Importance: {task['importance']})")

            try:
                task_num_str = input(f"Enter the number of the task to mark as {'important' if choice == '3' else 'done'}: ")
                task_idx = int(task_num_str) - 1
                if 0 <= task_idx < len(tasks_list):
                    selected_task = tasks_list[task_idx]
                    action = 'mark_important' if choice == '3' else 'mark_done'
                    function_two(tasks_list, selected_task, {'type': 'modify', 'action': action})
                    print(f"Task '{selected_task['description']}' marked as {'important' if choice == '3' else 'done'}.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '5':
            print("Exiting To-Do List.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
