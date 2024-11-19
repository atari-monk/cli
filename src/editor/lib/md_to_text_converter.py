import tkinter as tk
from tkinter import scrolledtext
from markdown import markdown
from bs4 import BeautifulSoup

def md_to_plain_text(md_content):
    """Convert Markdown to plain text."""
    html_content = markdown(md_content)
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def convert_md():
    """Convert the content of the Markdown input field to plain text."""
    md_content = md_input.get("1.0", tk.END).strip()
    plain_text = md_to_plain_text(md_content)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, plain_text)

def copy_text():
    """Copy the content of the output field to the clipboard."""
    plain_text = text_output.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(plain_text)
    root.update()  # Ensures the clipboard is updated

def clear_fields():
    """Clear both the input and output fields."""
    md_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)

# Create the main window
root = tk.Tk()
root.title("Markdown to Text Converter")

# Layout configuration for responsive design
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)  # Input field
root.rowconfigure(3, weight=1)  # Output field

# Markdown input field
md_label = tk.Label(root, text="Markdown Input:")
md_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
md_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
md_input.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, pady=10, padx=5, sticky="ew")
button_frame.columnconfigure((0, 1, 2), weight=1)  # Make buttons distribute evenly

convert_button = tk.Button(button_frame, text="Convert to Text", command=convert_md)
convert_button.grid(row=0, column=0, padx=5)

copy_button = tk.Button(button_frame, text="Copy Text", command=copy_text)
copy_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(button_frame, text="Clear Fields", command=clear_fields)
clear_button.grid(row=0, column=2, padx=5)

# Plain text output field
text_label = tk.Label(root, text="Plain Text Output:")
text_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_output.grid(row=4, column=0, pady=5, padx=5, sticky="nsew")

# Run the application
root.mainloop()
