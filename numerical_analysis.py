import sympy as sp

x = sp.Symbol('x')
h = sp.Symbol('h')
f = sp.Function('f')

central_exp_first   = (f(x+h) - f(x-h)) / (2*h)
forward_exp_first   = (-3*f(x) + 4*f(x+h) - f(x+2*h)) / (2*h)
backward_exp_first  = (3*f(x) - 4*f(x-h) + f(x-2*h)) / (2*h)

central_exp_second  = (f(x+h) + f(x-h) - 2*f(x)) / h**2
forward_exp_second  = (2*f(x) - 5*f(x+h) + 4*f(x+2*h) - f(x+3*h)) / h**2
backward_exp_second = (2*f(x) - 5*f(x-h) + 4*f(x-2*h) - f(x-3*h)) / h**2

first_derivative_array   = [backward_exp_first,  central_exp_first,  forward_exp_first]
second_derivative_array  = [backward_exp_second, central_exp_second, forward_exp_second]


def first_derivative():
    print("""
INSTRUCTIONS:
    First Derivative has Three Equations:
        Press 0 for Backward Equation
        Press 1 for Central  Equation
        Press 2 for Forward  Equation
""")
    user_choice = int(input("Choose equation (0/1/2): "))
    x_val = float(input("Enter the value of x: "))
    h_val = float(input("Enter the value of h: "))

    if user_choice == 0:        
        fx     = float(input(f"Enter f({round(x_val, 4)})    = "))
        fx_mh  = float(input(f"Enter f({round(x_val - h_val, 4)})    = "))
        fx_m2h = float(input(f"Enter f({round(x_val - 2*h_val, 4)})    = "))
        
        expr = first_derivative_array[0].subs([(f(x), fx), (f(x-h), fx_mh), (f(x-2*h), fx_m2h)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f'({round(x_val, 4)}) = {round(float(result), 4)}\n")

    elif user_choice == 1:       
        fx_ph = float(input(f"Enter f({round(x_val + h_val, 4)})  = "))
        fx_mh = float(input(f"Enter f({round(x_val - h_val, 4)})  = "))
        
        expr = first_derivative_array[1].subs([(f(x+h), fx_ph), (f(x-h), fx_mh)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f'({round(x_val, 4)}) = {round(float(result), 4)}\n")

    elif user_choice == 2:        
        fx     = float(input(f"Enter f({round(x_val, 4)})    = "))
        fx_ph  = float(input(f"Enter f({round(x_val + h_val, 4)})    = "))
        fx_p2h = float(input(f"Enter f({round(x_val + 2*h_val, 4)})    = "))
        
        expr = first_derivative_array[2].subs([(f(x), fx), (f(x+h), fx_ph), (f(x+2*h), fx_p2h)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f'({round(x_val, 4)}) = {round(float(result), 4)}\n")

    else:
        print("Invalid choice! Please enter 0, 1, or 2.\n")


def second_derivative():
    print("""
INSTRUCTIONS:
    Second Derivative has Three Equations:
        Press 0 for Backward Equation
        Press 1 for Central  Equation
        Press 2 for Forward  Equation
""")
    user_choice = int(input("Choose equation (0/1/2): "))
    x_val = float(input("Enter the value of x: "))
    h_val = float(input("Enter the value of h: "))

    if user_choice == 0:          
        fx     = float(input(f"Enter f({round(x_val, 4)})    = "))
        fx_mh  = float(input(f"Enter f({round(x_val - h_val, 4)})    = "))
        fx_m2h = float(input(f"Enter f({round(x_val - 2*h_val, 4)})    = "))
        fx_m3h = float(input(f"Enter f({round(x_val - 3*h_val, 4)})    = "))   
        
        expr = second_derivative_array[0].subs([(f(x), fx), (f(x-h), fx_mh), (f(x-2*h), fx_m2h), (f(x-3*h), fx_m3h)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f''({round(x_val, 4)}) = {round(float(result), 4)}\n")

    elif user_choice == 1:        
        fx    = float(input(f"Enter f({round(x_val, 4)})    = "))
        fx_ph = float(input(f"Enter f({round(x_val + h_val, 4)})    = "))
        fx_mh = float(input(f"Enter f({round(x_val - h_val, 4)})    = "))
        
        expr = second_derivative_array[1].subs([(f(x), fx), (f(x+h), fx_ph), (f(x-h), fx_mh)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f''({round(x_val, 4)}) = {round(float(result), 4)}\n")

    elif user_choice == 2:        
        fx     = float(input(f"Enter f({round(x_val, 4)})    = "))
        fx_ph  = float(input(f"Enter f({round(x_val + h_val, 4)})    = "))
        fx_p2h = float(input(f"Enter f({round(x_val + 2*h_val, 4)})    = "))
        fx_p3h = float(input(f"Enter f({round(x_val + 3*h_val, 4)})    = "))
        
        expr = second_derivative_array[2].subs([(f(x), fx), (f(x+h), fx_ph), (f(x+2*h), fx_p2h), (f(x+3*h), fx_p3h)])
        result = expr.subs([(x, x_val), (h, h_val)])
        print(f"\nResult: f''({round(x_val, 4)}) = {round(float(result), 4)}\n")

    else:
        print("Invalid choice! Please enter 0, 1, or 2.\n")


print("""
******** Welcome To Numerical Analysis Problem Solver System (NAPSS) ********

    Which Order of the derivative do you want?
        Press 1 for First  Derivative
        Press 2 for Second Derivative
""")

while True:
    try:
        demanded_rank = int(input("Enter the order (1 or 2): "))
    except ValueError:
        print("Please enter an integer (1 or 2).\n")
        continue

    if demanded_rank == 1:
        first_derivative()
        break
    elif demanded_rank == 2:
        second_derivative()
        break
    else:
        print("Invalid input! Please enter 1 or 2.\n")