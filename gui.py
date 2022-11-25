import tkinter as tk
from tkinter import ttk


# GUI for the application
class Window:

    def __init__(self, db, root):
        self.root = root
        self.root.title("Memory Trainer")
        self.root.geometry('1890x1000')

        self.db = db
        self.current_card = None

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0)

        # Add button
        self.add = ttk.Button(self.mainframe, text="add a question", command=self.add_mode)
        self.add.grid(column=1, row=1, padx=10, sticky=tk.EW)

        # Learn button
        self.learn = ttk.Button(self.mainframe, text="learn", command=self.load_question)
        self.learn.grid(column=2, row=1, padx=10, sticky=tk.EW)

        # Save button
        self.save_button = ttk.Button(self.mainframe, text="save", command=self.add_question)

        # Delete button
        self.delete_button = ttk.Button(self.mainframe, text="delete", command=self.delete_question)

        # Upper text frame
        self.upper_text = tk.Text(self.mainframe, width=188, height=25, font=('Arial', 16))
        self.upper_text.grid(column=1, columnspan=2, row=2, padx=10, sticky=tk.EW)

        # Lower text frame
        self.lower_text = tk.Text(self.mainframe, width=188, height=24, font=('Arial', 16))
        self.lower_text.grid(column=1, columnspan=2, row=3, padx=10, sticky=tk.EW)

        # Showing questions to learn
        self.load_question()

    # Turning on question/answer entry mode
    def add_mode(self):
        # Updating text in the upper text area
        self.upper_text.config(state=tk.NORMAL)
        self.upper_text.delete("1.0", tk.END)
        self.upper_text.insert(tk.END, "Enter a question")

        # Updating text in the lower text area
        self.lower_text.config(state=tk.NORMAL)
        self.lower_text.delete("1.0", tk.END)
        self.lower_text.insert(tk.END, "Enter an answer")

        # Updating learn button
        self.learn.configure(text='learn')

        # Showing the save button
        if self.delete_button.grid_info():
            self.delete_button.grid_remove()

        self.save_button.grid(column=1, columnspan=2, row=4, padx=10)

        # Clearing out text areas if they gain focus
        self.upper_text.bind('<FocusIn>', lambda e: self.upper_text.delete("1.0", tk.END))
        self.lower_text.bind('<FocusIn>', lambda e: self.lower_text.delete("1.0", tk.END))

        self.root.bind('<F5>', lambda e: self.add_question())

    # Adding new question/answer pair to database
    def add_question(self):
        # Collecting values from text areas
        question = self.upper_text.get("1.0", tk.END)
        answer = self.lower_text.get("1.0", tk.END)

        # Adding values to database
        if question not in ['Enter a question\n', '\n'] and answer not in ['Enter an answer\n', '\n']:
            self.db.add_card(question, answer)
            self.add_mode()

    # Turning on training mode
    def load_question(self):
        # Getting a question from database
        self.current_card = self.db.get_card()

        # Updating text in the upper text area
        self.upper_text.config(state=tk.NORMAL)
        self.upper_text.delete("1.0", tk.END)
        if self.current_card is not None:
            self.upper_text.insert(tk.END, self.current_card[1])
        else:
            self.upper_text.insert(tk.END, 'No questions in database')
        self.upper_text.config(state=tk.DISABLED)

        # Updating text in the lower text area
        self.lower_text.config(state=tk.NORMAL)
        self.lower_text.delete("1.0", tk.END)
        self.lower_text.insert(tk.END, "Enter the answer and hit Enter/Return")
        self.lower_text.bind('<FocusIn>', lambda e: self.lower_text.delete("1.0", tk.END))

        self.learn.configure(text='next question ->')

        # Hiding the save button
        if self.save_button.grid_info():
            self.save_button.grid_remove()

        if self.current_card is not None:
            self.delete_button.grid(column=1, columnspan=2, row=4, padx=10)

        # Adding answer to the question to the upper text area after the enter/return key was pressed
        self.lower_text.bind('<Return>', lambda e: self.show_answer())

    # Showing answer under the question
    def show_answer(self):
        if not self.save_button.grid_info() and 'Answer' not in self.upper_text.get("1.0", tk.END):
            self.upper_text.config(state=tk.NORMAL)
            self.upper_text.insert(tk.END, f'Answer:\n{self.current_card[2]}')
            self.upper_text.config(state=tk.DISABLED)
            self.lower_text.config(state=tk.DISABLED)

    # Deleting new question/answer pair to database
    def delete_question(self):
        self.db.delete_card(self.current_card[0])
        self.delete_button.grid_remove()
        self.load_question()


