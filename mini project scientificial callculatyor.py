

from tkinter import *
import math


root = Tk()
root.title("Scientific Calculator")
root.geometry("400x600")
root.resizable(False, False)


equation = StringVar()
entry = Entry(root, textvariable=equation, font=('Arial', 20), bg="lightgray", bd=10, justify="right")
entry.grid(row=0, column=0, columnspan=5, pady=10)


def press(num):
    current = equation.get()
    equation.set(current + str(num))

def clear():
    equation.set("")

def equal():
    try:
        result = eval(equation.get())
        equation.set(result)
    except:
        equation.set("Error")


def sci_op(op):
    try:
        val = float(equation.get())
        if op == "sqrt":
            result = math.sqrt(val)
        elif op == "log":
            result = math.log10(val)
        elif op == "ln":
            result = math.log(val)
        elif op == "sin":
            result = math.sin(math.radians(val))
        elif op == "cos":
            result = math.cos(math.radians(val))
        elif op == "tan":
            result = math.tan(math.radians(val))
        elif op == "pi":
            result = math.pi
        elif op == "e":
            result = math.e
        equation.set(str(result))
    except:
        equation.set("Error")


buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sqrt', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('log', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('ln', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3), ('pi', 4, 4),
    ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('e', 5, 3), ('C', 5, 4),
]

for (text, row, col) in buttons:
    if text in ['sqrt', 'log', 'ln', 'sin', 'cos', 'tan', 'pi', 'e']:
        Button(root, text=text, width=6, height=2, font=('Arial', 14), command=lambda t=text: sci_op(t)).grid(row=row, column=col, padx=5, pady=5)
    elif text == 'C':
        Button(root, text=text, width=6, height=2, font=('Arial', 14), bg="red", fg="white", command=clear).grid(row=row, column=col, padx=5, pady=5)
    else:
        Button(root, text=text, width=6, height=2, font=('Arial', 14), command=lambda t=text: press(t)).grid(row=row, column=col, padx=5, pady=5)


Button(root, text='=', width=32, height=2, font=('Arial', 14), bg="green", fg="white", command=equal).grid(row=6, column=0, columnspan=5, pady=10)

root.mainloop()

