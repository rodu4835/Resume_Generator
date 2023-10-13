import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import sys
from tkinter import *
from src import generateResume as gR  # Import the generateResume file as gR

def main():
    create_main_gui()
    
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.config(state="normal")
        self.widget.insert("end", str)
        self.widget.see("end")
        self.widget.config(state="disabled")

def create_main_gui():
    global section_frame

    root = tk.Tk()
    
    main_monitor_width = 5250
    main_monitor_height = 1700
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    position_right = int(main_monitor_width / 2 - window_width / 2)
    position_down = int(main_monitor_height / 2 - window_height / 2)
    root.geometry("+{}+{}".format(position_right, position_down))
    
    root.title("Resume Generator")

    tk.Label(root, text="What would you like to do?", pady=5).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(root, text="Generate Resume and Cover Letter", pady=5, command=show_generate_resume).grid(row=1, column=0, padx=10, pady=10)

    section_frame = tk.Frame(root)
    section_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

    root.mainloop()

def show_generate_resume():
    global output_text

    for widget in section_frame.winfo_children():
        widget.grid_forget()

    tk.Label(section_frame, text="Enter Job Description:").grid(row=0, column=0)
    
    # Add a label for displaying the "Processing..." message
    processing_label = tk.Label(section_frame, text="Processing...", fg="red")
    
    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(section_frame)
    scrollbar.grid(row=2, column=1, sticky="ns")
    
    # Moved the OK button to row 1
    tk.Button(section_frame, text="OK", command=lambda: on_ok_click_with_status(job_description, processing_label)).grid(row=1, column=0)

    # Moved the Text widget to row 2
    job_description = tk.Text(section_frame, wrap="word", height=5, width=80, yscrollcommand=scrollbar.set)
    job_description.grid(row=2, column=0)
    
    # Link scrollbar to Text widget
    scrollbar.config(command=job_description.yview)
    
    job_description.bind("<KeyRelease>", lambda event: adjust_textbox_height(job_description))
    
    # Bind the Enter key to the same function as the OK button
    job_description.bind("<Return>", lambda event: on_ok_click_with_status(job_description, processing_label))

def adjust_textbox_height(text_widget):
    # Check if Text widget is empty
    if text_widget.index('end-1c') == '1.0':
        return

    # Get the height of a single line in the Text widget
    line_info = text_widget.dlineinfo('1.0')
    
    if line_info:  # Check if line_info is not None
        single_line_height = line_info[3]
        
        # Get the screen height and calculate the maximum number of lines
        screen_height = text_widget.winfo_screenheight()
        max_lines = int(screen_height // single_line_height) - 2  # Deducting some lines for buffer space and taskbar

        # Get the current number of lines in the Text widget
        current_lines = int(text_widget.index('end-1c').split('.')[0])

        # Set the height of the Text widget, capped at the maximum number of lines
        text_widget.config(height=min(current_lines, max_lines))



def on_ok_click_with_status(job_description, processing_label):
    for widget in section_frame.winfo_children():
        widget.grid_forget()
    # Show the processing label
    processing_label.grid(row=0, column=0)
    
    job = job_description.get("1.0", tk.END).strip()
    develop_thread = threading.Thread(target=gR.main, args=(job,))
    develop_thread.start()
    section_frame.after(100, check_thread, develop_thread, on_content_complete, processing_label)

def check_thread(thread, callback, processing_label):
    if thread.is_alive():
        section_frame.after(100, check_thread, thread, callback, processing_label)
    else:
        # Hide the processing label
        processing_label.grid_forget()
        callback()

def on_content_complete():
    for widget in section_frame.winfo_children():
        widget.grid_forget()

    tk.Label(section_frame, text="Resume Generated!").grid(row=0, column=0)

if __name__ == "__main__":
    main()
