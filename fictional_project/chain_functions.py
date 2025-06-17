def function_four():
    return "This is function four!"

def function_three():
    return function_four()

def function_two():
    return function_three()

def function_one():
    return function_two()

if __name__ == "__main__":
    result = function_one()
    print(result)
