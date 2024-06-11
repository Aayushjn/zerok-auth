import tkinter as tk
from zerok.client.client import Client

client = Client()

def hide_buttons():
    register_btn.pack_forget()
    login_btn.pack_forget()


def switch_to_register():
    hide_buttons()
    clear_previous_contents()
    register_frame.place(relx=0.5, rely=0.5, anchor="center")


def switch_to_login():
    hide_buttons()
    clear_previous_contents()
    login_frame.place(relx=0.5, rely=0.5, anchor="center")


def clear_previous_contents():
    status_label_reg.config(text="")
    username_entry_reg.delete(0, tk.END)
    password_entry_reg.delete(0, tk.END)
    status_label_login.config(text="")
    username_entry_login.delete(0, tk.END)
    password_entry_login.delete(0, tk.END)


def register():
    global status_label_reg
    username = username_entry_reg.get()
    password = password_entry_reg.get()

    if not username or not password:
        status_label_reg.config(text="Please enter the details", fg="red")
        return

    hide_buttons()
    register_btn_reg.config(state=tk.DISABLED)
    back_btn_reg.config(state=tk.DISABLED)

    ok, response = client.user_registration(username, password)
    
    if ok:
        status_label_reg.config(text=response["message"], fg="green")
        root.after(1000, switch_to_login)
        # Disable the buttons again after successful registration
        root.after(1000, enable_register_back_buttons)
    else:
        status_label_reg.config(text=response["message"], fg="red")
        register_btn_reg.config(state=tk.NORMAL)
        back_btn_reg.config(state=tk.NORMAL)


def enable_register_back_buttons():
    register_btn_reg.config(state=tk.NORMAL)
    back_btn_reg.config(state=tk.NORMAL)


def login():
    global status_label_login
    username = username_entry_login.get()
    password = password_entry_login.get()

    if not username or not password:
        status_label_login.config(text="Please enter the details", fg="red")
        return

    hide_buttons()
    login_btn_login.config(state=tk.DISABLED)
    back_btn_login.config(state=tk.DISABLED)

    
    ok, response = client.user_login(username, password)
    
    
    if ok:
        status_label_login.config(text=response["message"], fg="green")
        root.after(1000, lambda: redirect_to_main_from_login(username))
    else:
        status_label_login.config(text=response["message"], fg="red")
        login_btn_login.config(state=tk.NORMAL)
        back_btn_login.config(state=tk.NORMAL)


def redirect_to_main_from_login(username):
    back_to_main_from_login()
    switch_to_main()


def show_buttons():
    register_btn.config(state=tk.NORMAL)
    login_btn.config(state=tk.NORMAL)
    register_btn.place(relx=0.5, rely=0.5, anchor="center")
    login_btn.place(relx=0.5, rely=0.6, anchor="center")


def back_to_main():
    show_buttons()
    login_frame.place_forget()
    register_frame.place_forget()
    clear_previous_contents()
    register_btn_reg.config(state=tk.NORMAL)
    back_btn_reg.config(state=tk.NORMAL)


# Function to handle back button press in the login page
def back_to_main_from_login():
    hide_buttons()
    login_frame.place_forget()
    register_frame.place_forget()
    show_buttons()
    clear_previous_contents()
    login_btn_login.config(state=tk.NORMAL)
    back_btn_login.config(state=tk.NORMAL)


def switch_to_main():
    hide_buttons()
    clear_previous_contents()
    show_buttons()


root = tk.Tk()
root.title("Client Interface")  # Set title bar

# Main page buttons
register_btn = tk.Button(root, text="Register", command=switch_to_register)
login_btn = tk.Button(root, text="Login", command=switch_to_login)
show_buttons()

# Register Frame
register_frame = tk.Frame(root)
tk.Label(register_frame, text="Register", font=("Helvetica", 18)).pack(pady=10)
tk.Label(register_frame, text="Username:").pack()
username_entry_reg = tk.Entry(register_frame)
username_entry_reg.pack()
tk.Label(register_frame, text="Password:").pack()
password_entry_reg = tk.Entry(register_frame, show="*")
password_entry_reg.pack()
register_btn_reg = tk.Button(register_frame, text="Register", command=register)
register_btn_reg.pack(pady=10)
back_btn_reg = tk.Button(register_frame, text="Back", command=back_to_main)
back_btn_reg.pack(pady=10)
status_label_reg = tk.Label(register_frame, text="", fg="black")
status_label_reg.pack()

# Login Frame
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Login", font=("Helvetica", 18)).pack(pady=10)
tk.Label(login_frame, text="Username:").pack()
username_entry_login = tk.Entry(login_frame)
username_entry_login.pack()
tk.Label(login_frame, text="Password:").pack()
password_entry_login = tk.Entry(login_frame, show="*")
password_entry_login.pack()
login_btn_login = tk.Button(login_frame, text="Login", command=login)
login_btn_login.pack(pady=10)
back_btn_login = tk.Button(login_frame, text="Back", command=back_to_main_from_login)
back_btn_login.pack(pady=10)
status_label_login = tk.Label(login_frame, text="", fg="black")
status_label_login.pack()

root.mainloop()
