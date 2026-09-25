import tkinter as tk

def on_slider_move(value):
    """Called when the slider moves; updates the variable + entry box."""
    current_number.set(round(float(value), 2))
    entry_var.set(str(current_number.get()))

def on_entry_change(event=None):
    """Called when you press Enter in the text box; updates the variable + slider."""
    try:
        value = float(entry_var.get())
        value = max(slider.cget("from"), min(slider.cget("to"), value))  # clamp to slider range
        current_number.set(value)
        slider.set(value)
        entry_var.set(str(value))
    except ValueError:
        entry_var.set(str(current_number.get()))  # reset if invalid

def save_number():
    """Example 'save' action -- just prints it, but you could write to a file, list, etc."""
    print(f"Saved number: {current_number.get()}")
    saved_label.config(text=f"Last saved: {current_number.get()}")

# --- GUI setup ---
root = tk.Tk()
root.title("Number Picker")
root.geometry("300x200")

# These variables hold the current number, kept in sync between
# the slider and the text entry box. They must be created AFTER
# root, since tkinter variables need a root window to attach to.
current_number = tk.DoubleVar(value=0)
entry_var = tk.StringVar(value="0")

tk.Label(root, text="Pick a number:").pack(pady=(15, 5))

# Slider (Scale widget)
slider = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    length=250,
    resolution=1,
    command=on_slider_move,
)
slider.pack()

# Text entry, linked via entry_var
entry = tk.Entry(root, textvariable=entry_var, justify="center")
entry.pack(pady=10)
entry.bind("<Return>", on_entry_change)  # press Enter to apply typed value

# Save button
tk.Button(root, text="Save Number", command=save_number).pack(pady=5)
saved_label = tk.Label(root, text="Last saved: (none yet)")
saved_label.pack()

root.mainloop()