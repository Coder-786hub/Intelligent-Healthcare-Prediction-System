from customtkinter import *
from PIL import Image
from tkinter import messagebox
import threading
from classifiers_menu import show_classifiers

def classifier():
    show_classifiers()

def open_ems():
    """Function to open the external script safely."""
    try:
        classifier()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the file: {e}")

def login_id():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error", "All fields are required")
    elif usernameEntry.get() == "admin" and passwordEntry.get() == "1234":  # Ensure password is string
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()
        threading.Thread(target=open_ems).start()  # Use thread to avoid event loop blocking
    else:
        messagebox.showerror("Error", "Invalid credentials")

# Main window
root = CTk()
root.geometry("930x478+100+200")
root.title("Login Page")
root.resizable(False, False)
root.config(background="white")

# Load and set image
image = CTkImage(Image.open(r"E:\Desktop\Project_folder\Images\OIP2.jpg"), size=(930, 478))
imageLabel = CTkLabel(root, image=image, text="")
imageLabel.place(x=110, y=0)

image = CTkImage(Image.open(r"E:\Desktop\Project_folder\Images\thapar.jpeg"), size=(100,80))
imageLabel = CTkLabel(root, image=image, text="")
imageLabel.place(x=40, y=20)

# UI elements
headinglabel = CTkLabel(root, text="Medical Health Care System", bg_color="white",
                        font=("Goudy Old Style", 20, "bold"), text_color="dark blue")
headinglabel.place(x=30, y=120)

usernameEntry = CTkEntry(root, placeholder_text="Enter Your Username", width=180)
usernameEntry.place(x=50, y=170)

passwordEntry = CTkEntry(root, placeholder_text="Enter Your Password", width=180, show="*")
passwordEntry.place(x=50, y=220)

loginButton = CTkButton(root, text="Login", cursor="hand2", command=login_id)
loginButton.place(x=70, y=270)

root.mainloop()
