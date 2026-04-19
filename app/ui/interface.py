import tkinter as tk  # Import Tkinter library to create the GUI
from app.core.deepdiff_comparator import compareJson, diff_parser  
# Import your custom functions:
# - compareJson: compares two JSON inputs
# - diff_parser: formats the comparison result into a readable output

def compare():
    # Function triggered when the "Compare" button is clicked

    before_json = before.get()  
    # Get the text entered in the "before" input field

    after_json = after.get()  
    # Get the text entered in the "after" input field

    diff_result = compareJson(before_json, after_json)  
    # Compare the two JSON strings and return raw differences

    diff_parsed = diff_parser(diff_result)  
    # Parse/format the raw diff result into a readable format

    diff.config(text=str(diff_parsed))  
    # Update the Label to display the result

# Create the main application window
window = tk.Tk()

window.title("JSONDiffTOOL")  
# Set the window title

window.geometry("400x300")  
# Set the window size

# Input field for the "before" JSON
before = tk.Entry(window)

# Input field for the "after" JSON
after = tk.Entry(window)

# Label used to display the comparison result
diff = tk.Label(window, text="Result will appear here", wraplength=350)

# Button that triggers the compare() function
compare_button = tk.Button(window, text="Compare", command=compare)

# Display widgets in the window
before.pack()
after.pack()
compare_button.pack()
diff.pack()

# Start the Tkinter event loop (keeps the window open)
window.mainloop()