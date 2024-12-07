from tkinter import *
from tkinter import messagebox, ttk
import numpy as np
import joblib
from lime import lime_tabular
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def logout_window():
    """Logout and close the GUI."""
    breast_cancer_window.destroy()

# Load the breast cancer prediction model
model = joblib.load(
    r"E:\Desktop\Project_folder\models\breast_cancermodel.joblib"
)

# Define feature names
feature_names = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"
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

def predict_breast_cancer():
    """Predicts whether the breast cancer is cancerous or not."""
    try:
        input_text = entryfield.get().strip()  # Retrieve the text entered by the user
        if input_text.startswith('[') and input_text.endswith(']'):
            input_text = input_text[1:-1]  # Remove brackets if they exist
        
        input_features = np.fromstring(input_text, sep=',')  # Parse as comma-separated values

        if input_features.size != model.n_features_in_:
            raise ValueError(f"Expected {model.n_features_in_} features, but got {input_features.size}.")

        prediction = model.predict(input_features.reshape(1, -1))
        prediction_text = "Cancerous" if prediction[0] == 1 else "Not Cancerous"
        output_label.config(text=f"Prediction: {prediction_text}", fg="red" if prediction[0] == 1 else "green")

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
    explanation_text = f"Prediction: {prediction_text}\n\nTop Contributing Features:\n"
    for feature, weight in feature_contributions:
        explanation_text += f"{feature}: {weight:.4f}\n"

    explanation_label.config(text=explanation_text, fg="white", bg="black")

    # Visual Explanation: Generate LIME graph
    fig = explanation.as_pyplot_figure()
    fig.tight_layout()  # Adjust layout for better appearance

    # Render the graph in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=breast_cancer_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=700, y=330)  # Adjust position as needed
    canvas.draw()

def breast_cancer_gui():
    """Opens the Breast Cancer Prediction GUI."""
    global breast_cancer_window, entryfield, output_label, explanation_label
    breast_cancer_window = Tk()
    breast_cancer_window.geometry("1270x700+20+40")
    breast_cancer_window.title("Breast Cancer Predictor")
    breast_cancer_window.config(bg="black")

    heading = Label(breast_cancer_window, text="Breast Cancer Prediction Model", font=("Roboto", 34, "bold"), fg="blue", bg="black")
    heading.pack(pady=30)

    lbl = Label(breast_cancer_window, text="Input Breast Cancer Features (comma-separated)", font=("Roboto", 15, "bold"), fg="white", bg="black")
    lbl.place(x=100, y=120)

    values = {
    "Test 1": ", ".join(map(str, [-0.2777981, 1.38675049, -0.15271249, -0.20744775, -0.1204959, -0.24418955, 1.56699527, 0.52933988, 0.52360246, 0.84768473, 1.07059038, 0.74107692, -0.38727381, -0.60163771, -0.45178885, -0.34150771, -0.131571, -0.07504, -0.11877088, 0.12765177, -0.3705341, -0.05637496, 0.00474085, 0.29104938, 0.006882, -0.10934112, 1.98697956, 1.19777674, 1.13618125, 1.59775828])),
    "Test 2": ", ".join(map(str, [20.57, 17.77, 132.9, 1326, 0.08474, 0.07864, 0.0869, 0.07017, 0.1812, 0.05667, 0.5435, 0.7339, 3.398, 74.08, 0.005225, 0.01308, 0.0186, 0.0134, 0.01389, 0.003532, 24.99, 23.41, 158.8, 1956, 0.1238, 0.1866, 0.2416, 0.186, 0.275, 0.08902])),
    "Test 3": ", ".join(map(str, [19.69, 21.25, 130, 1203, 0.1096, 0.1599, 0.1974, 0.1279, 0.2069, 0.05999, 0.7456, 0.7869, 4.585, 94.03, 0.00615, 0.04006, 0.03832, 0.02058, 0.0225, 0.004571, 23.57, 25.53, 152.5, 1709, 0.1444, 0.4245, 0.4504, 0.243, 0.3613, 0.08758])),
    "Test 4": ", ".join(map(str, [15.67, 18.45, 120.3, 1105, 0.0965, 0.0857, 0.0972, 0.0683, 0.1764, 0.0503, 0.5487, 0.7092, 3.735, 64.11, 0.006749, 0.01286, 0.0173, 0.0157, 0.01435, 0.002839, 21.55, 22.11, 142.6, 1864, 0.1103, 0.1612, 0.2034, 0.159, 0.220, 0.08321])),
    "Test 5": ", ".join(map(str, [13.17, 18.66, 85.98, 534.6, 0.1158, 0.1231, 0.1226, 0.0734, 0.2128, 0.06777, 0.2871, 0.8937, 1.897, 24.25, 0.006532, 0.02336, 0.02905, 0.01215, 0.01743, 0.003643, 15.67, 27.95, 102.8, 759.4, 0.1786, 0.4166, 0.5006, 0.2088, 0.39, 0.1179])),
    "Test 6": ", ".join(map(str, [8.196, 16.84, 51.71, 201.9, 0.086, 0.05943, 0.01588, 0.005917, 0.1769, 0.06503, 0.1563, 0.9567, 1.094, 8.205, 0.008968, 0.01646, 0.01588, 0.005917, 0.02574, 0.002582, 8.964, 21.96, 57.26, 242.2, 0.1297, 0.1357, 0.0688, 0.02564, 0.3105, 0.07409])),
    "Test 7": ", ".join(map(str, [16.6, 28.08, 108.3, 858.1, 0.08455, 0.1023, 0.09251, 0.05302, 0.159, 0.05648, 0.4564, 1.075, 3.425, 48.55, 0.005903, 0.03731, 0.0473, 0.01557, 0.01318, 0.003892, 18.98, 34.12, 126.7, 1124, 0.1139, 0.3094, 0.3403, 0.1418, 0.2218, 0.0782])),
    "Test 8": ", ".join(map(str, [11.13, 22.44, 71.49, 378.4, 0.09566, 0.08194, 0.04824, 0.02257, 0.203, 0.06552, 0.28, 1.467, 1.994, 17.85, 0.003495, 0.03051, 0.03445, 0.01024, 0.02912, 0.004723, 12.02, 28.26, 77.8, 436.6, 0.1087, 0.1782, 0.1564, 0.06413, 0.3169, 0.08032]))
}

# Set the Combobox options
    entryfield = ttk.Combobox(breast_cancer_window, values=list(values.values()), width=120, font=(19), state = "readonly")
    entryfield.set("Please Select Your test : ")
    entryfield.place(x=100, y=170)

    predict_btn = Button(breast_cancer_window, text="Predict", font=("Roboto", 25, "bold"), fg="white", bg="blue", command=predict_breast_cancer)
    predict_btn.place(x=100, y=220)

    logout_btn = Button(breast_cancer_window, text="Logout", font=("Roboto", 25, "bold"), fg="white", bg="red", command=logout_window)
    logout_btn.place(x=1000, y=220)

    output_label = Label(breast_cancer_window, font=("Roboto", 25), bg="black")
    output_label.place(x=100, y=290)

    explanation_label = Label(breast_cancer_window, font=("Roboto", 15), bg="black", justify="left", wraplength=600)
    explanation_label.place(x=100, y=350)

    breast_cancer_window.mainloop()

# Initialize the LIME explainer
initialize_lime_explainer()

# Launch the GUI
# breast_cancer_gui()
