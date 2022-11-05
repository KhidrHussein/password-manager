from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    final_list = password_letters + password_symbols + password_numbers
    shuffle(final_list)

    password = "".join(final_list)

    global password_entry
    password_entry.insert(0, password)

    pyperclip.copy(password)

# ---------------------------- SEARCH FUNCTIONALITY ------------------------- #


def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as file:
            data_file = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found!")
    else:
        if website in data_file:
            email = data_file[website]["email"]
            password = data_file[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for the {website} exists!")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any field empty.")
    else:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.minsize(width=500, height=500)
window.config(pady=20, padx=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, columnspan=2, row=1)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=3, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=53)
email_entry.insert(0, "khidr@gmail.com")
email_entry.grid(column=1, columnspan=3, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=35)
password_entry.grid(column=1, columnspan=2, row=3)

generate_password = Button(text="Generate Password", command=password_generator)
generate_password.grid(column=3, row=3)

add_button = Button(text="Add", width=30, command=save)
add_button.grid(column=1, columnspan=2, row=4)

window.mainloop()
