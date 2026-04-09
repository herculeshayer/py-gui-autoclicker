import random
import tkinter as tk

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def rand_function():
    return random.randint(1, 10)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 1. Run your terminal functions
    print_hi('PyCharm')
    x = rand_function()
    print(x)

    # 2. Initialize the main Tkinter window
    root = tk.Tk()
    root.title("Py GUI Autoclicker")
    root.geometry("300x200") # Sets the starting size of the window

    # 3. Create your frame and attach it to the root window
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # You can add a simple label to the frame just to see it working
    label = tk.Label(frame, text="Hello, Tkinter!")
    label.pack(pady=50)

    # 4. Start the Tkinter event loop (this keeps the window open)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/