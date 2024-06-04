from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ('Arial', 15, 'normal')
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]

    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    password = f"{''.join(password_list)}"

    # print(f"Your password is: {password}")
    password_input.delete(0, END)
    password_input.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_input.get()

    if len(website) == 0:
        messagebox.showerror(title="Field Empty", message="Please enter the website name before search.")
    else:
        try:
            with open("passwords.json", 'r') as f:
                data = json.load(f)
                website_detail = data[website]
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No data file found.")
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title="Error", message="The data file is empty.")
        except KeyError:
            messagebox.showerror(title="Error", message="No details for the website exist.")
        else:
            email = website_detail['email']
            password = website_detail['password']
            messagebox.showinfo(title=website, message=f"The entered details are:\nEmail: {email}\n"
                                                       f"Password: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_entry():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    if len(website) > 0 and len(email) > 0 and len(password) > 0:
        can_add = True
    else:
        can_add = False

    if can_add:

        is_ok = messagebox.askokcancel(title=website, message=f"The entered details are:\nEmail: {email}\n"
                                                              f"Password: {password}\nIs this okay?")

        if is_ok:

            new_data = {
                website: {
                    "email": email,
                    "password": password
                }
            }
            try:
                with open("passwords.json", 'r') as f:
                    data = json.load(f)
                    data.update(new_data)
            except(FileNotFoundError, json.decoder.JSONDecodeError):
                data = new_data
            finally:
                with open("passwords.json", 'w') as f:
                    json.dump(data, f, indent=4)

                website_input.delete(0, END)
                website_input.focus()
                email_input.delete(0, END)
                email_input.insert(END, "cpdprivate007@gmail.com")
                password_input.delete(0, END)

    else:
        messagebox.showwarning(title="Field Empty", message="Please don't leave any field(s) empty.")


def clear_fields():
    website_input.delete(0, END)
    website_input.focus()
    email_input.delete(0, END)
    email_input.insert(END, "cpdprivate007@gmail.com")
    password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", font=FONT)
website_label.grid(row=1, column=0)

website_input = Entry(width=35)
website_input.focus()
website_input.grid(row=1, column=1, sticky="EW")

search_button = Button(text="Search", width=35, command=find_password, bd=0, bg="light grey")
search_button.grid(row=1, column=2)

email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(row=2, column=0)

email_input = Entry(width=35)
email_input.insert(END, "cpdprivate007@gmail.com")
email_input.grid(row=2, column=1, columnspan=2, sticky="EW")

password_label = Label(text="Password:", font=FONT)
password_label.grid(row=3, column=0)

password_input = Entry(width=21)
password_input.grid(row=3, column=1, sticky="EW")

generate_button = Button(text="Generate Password", width=21, bd=0, command=generate_password, bg="light grey")
generate_button.grid(row=3, column=2)

clear_button = Button(text="Clear", width=36, bd=0, command=clear_fields, bg="light grey")
clear_button.grid(row=4, column=0)

add_button = Button(text="Add", width=36, bd=0, command=add_entry, bg="light grey")
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
