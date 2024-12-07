from tkinter import *
from tkinter import messagebox, ttk
import numpy as np
import joblib
from lime import lime_tabular
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the model for cervical cancer
model = joblib.load(
    r"E:\Desktop\Project_Folder\models\cervical_cancermodel.joblib"
)

# Define feature names for cervical cancer
feature_names = [
    "Age", "Number of sexual partners", "First sexual intercourse", "Num of pregnancies", "Smokes",
    "Smokes (years)", "Smokes (packs/year)", "Hormonal Contraceptives", "Hormonal Contraceptives (years)",
    "IUD", "IUD (years)", "STDs", "STDs (number)", "STDs:condylomatosis", "STDs:cervical condylomatosis",
    "STDs:vaginal condylomatosis", "STDs:vulvo-perineal condylomatosis", "STDs:syphilis",
    "STDs:pelvic inflammatory disease", "STDs:genital herpes", "STDs:molluscum contagiosum", "STDs:AIDS",
    "STDs:HIV", "STDs:Hepatitis B", "STDs:HPV", "STDs: Number of diagnosis", "STDs: Time since first diagnosis",
    "STDs: Time since last diagnosis", "Dx:Cancer", "Dx:CIN", "Dx:HPV", "Dx", "Hinselmann", "Schiller", "Citology"
]

# Placeholder for Lime Explainer
lime_explainer = None


def initialize_lime_explainer():
    """Initialize the LIME explainer with a representative dataset."""
    global lime_explainer
    sample_data = np.random.rand(100, model.n_features_in_)  # Replace with actual representative data
    lime_explainer = lime_tabular.LimeTabularExplainer(
        sample_data,
        mode='classification',
        feature_names=feature_names[:model.n_features_in_],
        class_names=['Not Cancerous', 'Cancerous'],
        discretize_continuous=True
    )


def predict_cervical_cancer():
    """Predict whether cervical cancer is cancerous or not."""
    input_text = entryfield.get()  # Retrieve the text entered by the user

    try:
        input_text = input_text.replace('\n', '').replace(' ', '')  # Preprocess input
        input_features = np.fromstring(input_text, sep=',')  # Parse as comma-separated values

        if input_features.size != model.n_features_in_:
            raise ValueError(f"Expected {model.n_features_in_} features, but got {input_features.size}.")

        prediction = model.predict(input_features.reshape(1, -1))
        print(prediction)
        prediction_text = "Cancerous" if prediction[0] == 1 else "Not Cancerous"
        output_label.config(text=prediction_text, fg="red" if prediction[0] == 1 else "green")

        explain_prediction(input_features, prediction_text)

    except ValueError as e:
        output_label.config(text=f"Error: {e}", fg="yellow")


def explain_prediction(input_features, prediction_text):
    """Generate a LIME explanation for the prediction and display it in the GUI."""
    if lime_explainer is None:
        messagebox.showerror("Error", "LIME explainer is not initialized.")
        return

    # Generate LIME explanation
    explanation = lime_explainer.explain_instance(
        input_features,
        model.predict_proba,
        num_features=12
    )

    # Textual Explanation
    feature_contributions = explanation.as_list()
    explanation_text = "Top Contributing Features:\n"
    for feature, weight in feature_contributions:
        explanation_text += f"{feature}: {weight:.4f}\n"

    explanation_label.config(text=f"{explanation_text}\n", fg="white", bg="black")

    # Visual Explanation: Generate LIME graph
    fig = explanation.as_pyplot_figure()
    fig.tight_layout()  # Adjust layout for better appearance

    # Render the graph in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=cervical_cancer_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=700, y=310)  # Adjust position as needed
    canvas.draw()


def logout_to_login():
    """Logout action to close the application."""
    cervical_cancer_window.destroy()


def cervical_cancer_gui():
    """Opens the Cervical Cancer Prediction GUI."""
    global cervical_cancer_window
    cervical_cancer_window = Tk()
    cervical_cancer_window.geometry("1270x750+20+40")
    cervical_cancer_window.title("Cervical Cancer Predictor")
    cervical_cancer_window.config(bg="black")

    heading = Label(cervical_cancer_window, text="Cervical Cancer Prediction Model", font=("Roboto", 34, "bold"), fg="green", bg="black")
    heading.pack(pady=30)

    lbl = Label(cervical_cancer_window, text="Input Cervical Cancer Features (comma-separated)", font=("Roboto", 15, "bold"), fg="white", bg="black")
    lbl.place(x=100, y=120)

    global entryfield, output_label, explanation_label

    # ComboBox to select test cases
    test_cases = {
    "Test 1": ", ".join(map(str, [41, 3, 17, 4, 0, 0, 0, 1, 10, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 21, 21, 0, 0, 0, 0, 0])),
    "Test 2": ", ".join(map(str, [40, 1, 18, 1, 0, 0, 0, 1, 0.25, 0, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1])),
    "Test 3": ", ".join(map(str, [42, 3, 23, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
    "Test 4": ", ".join(map(str, [45, 4, 14, 6, 0, 0, 0, 1, 10, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
    "Test 5": ", ".join(map(str, [40, 1, 20, 2, 0, 0, 0, 1, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0])),
    "Test 6": ", ".join(map(str, [39, 2, 17, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])),
    "Test 7": ", ".join(map(str, [37, 2, 18, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0])),
    "Test 8": ", ".join(map(str, [36, 5, 17, 3, 0, 0, 0, 1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
}



    entryfield = ttk.Combobox(cervical_cancer_window, values = list(test_cases.values()),width=120, font=(19))
    entryfield.set("Please Select Your Test : ")
    entryfield.place(x=100, y=170)

    predict_btn = Button(cervical_cancer_window, text="Predict", font=("Roboto", 25, "bold"), fg="white", bg="green", command=predict_cervical_cancer)
    predict_btn.place(x=100, y=220)

    logout_btn = Button(cervical_cancer_window, text="Logout", font=("Roboto", 25, "bold"), fg="white", bg="red", command=logout_to_login)
    logout_btn.place(x=1280, y=220)

    output_label = Label(cervical_cancer_window, font=("Roboto", 25), bg="black")
    output_label.place(x=100, y=310)

    explanation_label = Label(cervical_cancer_window, font=("Roboto", 15), bg="black", justify="left", wraplength=500)
    explanation_label.place(x=100, y=400)

    cervical_cancer_window.mainloop()


# Initialize the LIME explainer
initialize_lime_explainer()

# Launch the GUI
# cervical_cancer_gui()
