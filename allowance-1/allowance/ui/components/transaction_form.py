from tkinter import Frame, Label, Entry, Button, StringVar, messagebox

class TransactionForm(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = Label(self, text="Amount:")
        self.amount_label.grid(row=0, column=0)

        self.amount_var = StringVar()
        self.amount_entry = Entry(self, textvariable=self.amount_var)
        self.amount_entry.grid(row=0, column=1)

        self.description_label = Label(self, text="Description:")
        self.description_label.grid(row=1, column=0)

        self.description_var = StringVar()
        self.description_entry = Entry(self, textvariable=self.description_var)
        self.description_entry.grid(row=1, column=1)

        self.submit_button = Button(self, text="Submit", command=self.submit_transaction)
        self.submit_button.grid(row=2, columnspan=2)

    def submit_transaction(self):
        amount = self.amount_var.get()
        description = self.description_var.get()
        
        if not amount or not description:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        # Here you would typically handle the transaction submission logic
        # For example, saving to a database or processing the transaction
        
        messagebox.showinfo("Success", f"Transaction submitted:\nAmount: {amount}\nDescription: {description}")
        self.amount_var.set("")
        self.description_var.set("")