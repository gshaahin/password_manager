from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip  # For copying generated password to clipboard
import json  # For saving and loading password data

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    # Generate a random password and insert it into the password entry
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for n in range(randint(8, 10))]
    symbols_list = [choice(symbols) for n in range(randint(2, 4))]
    numbers_list = [choice(numbers) for n in range(randint(2, 4))]
    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # Copy to clipboard

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    # Save the website, email, and password to a JSON file and backup text file
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                # Try to update existing data
                with open("Password Manager.json", "r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
                with open("Password Manager.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
                # Also save to a plain text file for backup
                with open("Password Manager", "a") as data:
                    data.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)
            except FileNotFoundError:
                # Create the file if it doesn't exist
                with open("Password Manager.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def find_password():
    # Search for the website in the JSON file and show the credentials if found
    website = website_entry.get().title()
    try:
        with open("Password Manager.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No data file found")
    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password} \nNote: Access Data in 'Password Manager.txt'")
        else:
            messagebox.showinfo(title="Oops", message=f"{website} is not in your password manager data.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

lock_image = PhotoImage(file="image/logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=("Arial", 8))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=("Arial", 8))
email_label.grid(column=0, row=2)
password_label = Label(text="Password", font=("Arial", 8))
password_label.grid(column=0, row=3)

# Entry fields
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()  # Focus cursor here on start
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="search", width=14, command=find_password)
search_button.grid(column=2, row=1)

mainloop()
