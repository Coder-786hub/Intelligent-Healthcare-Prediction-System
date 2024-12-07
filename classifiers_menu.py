from customtkinter import *
from PIL import Image

from breast_cancer import breast_cancer_gui
from Cervical_cancer import cervical_cancer_gui
from medicine_recommendation_system import medicine_recommendation

def cervical_cancer_window():
    cervical_cancer_gui()
    

def breast_cancer_window():
    breast_cancer_gui()

def medicine_recommendation_window():
    medicine_recommendation()
    

# Classifier Options GUI
def show_classifiers():
    # Create main window
    global classifiers_window
    classifiers_window = CTk()
    classifiers_window.geometry("930x478+100+200")
    classifiers_window.title("Classifier Options")
    classifiers_window.resizable(False, False)
    classifiers_window.config(bg = "white")


    image = CTkImage(Image.open(r"E:\Desktop\Project_folder\Images\thapar.jpeg"), size=(100,80))
    imageLabel = CTkLabel(classifiers_window, image=image, text="")
    imageLabel.place(x=40, y=10)

    try:
        # Set background image
        bg_image = CTkImage(Image.open(r"E:\Desktop\Project_folder\Images\OIP2.jpg"), size=(930, 478))
        bg_label = CTkLabel(classifiers_window, image=bg_image, text="")
        bg_label.place(x=120, y=0)
    except FileNotFoundError:
        print("Background image not found. Proceeding without it.")

    # Heading Label
    headinglabel = CTkLabel(classifiers_window, text="Medical Health Care System", bg_color="white",
                        font=("Goudy Old Style", 20, "bold"), text_color="dark blue")
    headinglabel.place(x=20, y=100)

    # Buttons for classifiers
    medicine_button = CTkButton(classifiers_window, text="Medicine Recommendation",
                                 font=("Arial", 14), fg_color="red", text_color="white",
                                 command = medicine_recommendation_window, width=189, height=40)
    medicine_button.place(x=130, y=170,anchor = CENTER)

    cervical_button = CTkButton(classifiers_window, text="Cervical Cancer Classifier",
                                 font=("Arial", 14), fg_color="red", text_color="white",
                                 command = cervical_cancer_window, width=180, height=40)
    cervical_button.place(x=130, y=220,anchor = CENTER)

    breast_button = CTkButton(classifiers_window, text="Breast Cancer Classifier",
                               font=("Arial", 14), fg_color="red", text_color="white",
                               command = breast_cancer_window, width=180, height=40)
    breast_button.place(x=130, y=270, anchor = CENTER)

    # Exit button
    exit_button = CTkButton(classifiers_window, text="Exit", font=("Arial", 14),
                            fg_color="gray", text_color="white", 
                            command=classifiers_window.destroy, width=180, height=40)
    exit_button.place(x=130, y=320, anchor=CENTER)

    classifiers_window.mainloop()

# show_classifiers()