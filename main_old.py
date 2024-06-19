"""
from zkg_client import client
from time import time
import statistics as s
import matplotlib.pyplot as plt

username = ["adwaitg", "adwaitgondhalekar", "aayush", "aayushjain", "adwaitg7122", "aayushjain0083", "ajain083", "adwait", "adwaitg123", "aayushj"]
correct_pass = ["Adwaitg@72982", "adwaitg1@234", "aayushjain@083", "aayush@2012", "adwaitg20200", "aayush_1220", "aayush5678", "adwaitg77890", "Adwait@123", "aayush@2000"]
incorrect_pass = ["Adwaitg71543", "adwag1234", "aayushjn@083", "aayush@12", "adwaitg00", "aayh_1220", "aayh5678", "adwtg7782", "Adwait@12", "aayush000"]

zkp_correct_time = []
zkp_incorrect_time = []

trad_correct_time = []
trad_incorrect_time = []

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i]/2, "{:.4f}".format(y[i]), ha = 'center')

client.configure_server("http://127.0.0.1:5000")
for i in range(10):
    ok, response = client.register_user(username[i], correct_pass[i])
    ok, response = client.register_user_traditional(username[i], correct_pass[i])
    if not ok:
        print(response)
        exit(-1)

# zkp testing
for i in range(20):
    
    if i<10:
        start = time()
        ok, response = client.login(username[i], correct_pass[i])
        end = time()
        time_taken = end - start
        zkp_correct_time.append(time_taken)
        print("Correct Authentication-{} time ={} sec".format(i+1, time_taken))
        
    else:
        start = time()
        ok, response = client.login(username[i%10], incorrect_pass[i%10])
        end = time()
        time_taken = end - start
        zkp_incorrect_time.append(time_taken)
        print("Incorrect Authentication-{} time ={} sec".format(i+1, time_taken))

if not ok:
    print(response)
    # exit(-1)
print(response)

# traditional testing
for i in range(20):
    
    if i<10:
        start = time()
        ok, response = client.login_traditional(username[i], correct_pass[i])
        end = time()
        time_taken = end - start
        trad_correct_time.append(time_taken)
        print("Correct Authentication-{} time ={} sec".format(i+1, time_taken))
        
    else:
        start = time()
        ok, response = client.login_traditional(username[i%10], incorrect_pass[i%10])
        end = time()
        time_taken = end - start
        trad_incorrect_time.append(time_taken)
        print("Incorrect Authentication-{} time ={} sec".format(i+1, time_taken))

if not ok:
    print(response)
    # exit(-1)
print(response)

print("ZKP Correct times = ", zkp_correct_time)
print("ZKP Incorrect times = ", zkp_incorrect_time)
print("Trad correct times = ", trad_correct_time)
print("Trad incorrect times = ", trad_incorrect_time)

# X1 = ["ZKP", "Traditional"]
# Y1 = [s.mean(zkp_correct_time), s.mean(trad_correct_time)]

# fig = plt.figure(figsize = (7, 5))
# bar_zkp1 = plt.bar(X1, Y1, width= 0.6)
# bar_zkp1[0].set_color('maroon')
# bar_zkp1[1].set_color("green")
# addlabels(X1, Y1)
# plt.xlabel("Authentication Method", fontsize = 13)
# plt.ylabel("Time taken in seconds", fontsize = 13)
# plt.title("Time taken for successful Authentication", fontsize = 15)
# plt.savefig("correct_auth.png")
# plt.show()

X2 = ["ZKP", "Traditional"]
Y2 = [s.mean(zkp_incorrect_time), s.mean(trad_incorrect_time)]

fig2 = plt.figure(figsize = (7, 5))
bar_zkp2 = plt.bar(X2, Y2, width= 0.6)
bar_zkp2[0].set_color('green')
bar_zkp2[1].set_color("maroon")
addlabels(X2, Y2)
plt.xlabel("Authentication Method", fontsize = 13)
plt.ylabel("Time taken in seconds", fontsize = 13)
plt.title("Time taken for unsuccessful Authentication", fontsize = 15)
plt.savefig("incorrect_auth.png")
# plt.show()
"""

import tkinter as tk

from zkg_client import client

client.configure_server("http://127.0.0.1:5000")


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

    ok, response = client.register_user(username, password)
    # ok, response = client.register_user_traditional(username, password)
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

    ok, response = client.login(username, password)
    # ok, response = client.login_traditional(username, password)

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
