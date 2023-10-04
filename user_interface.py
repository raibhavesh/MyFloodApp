import pickle
import tkinter as tk
import numpy as np
from tkinter import messagebox
from sklearn.preprocessing import MinMaxScaler

monthly_rainfall = np.array([])

floods_dict = {
    0: 'NO FLOODS',
    1: 'FLOODS'
}


# Loading the model
with open("./Best Model/best_model.pkl", 'rb') as pickle_file:
    best_model = pickle.load(pickle_file)
    
# Loading the MinMax Scaler
with open("./Best Model/scaler.pkl", 'rb') as pickle_file:
    scaler = pickle.load(pickle_file)
    

def validate_input(index, value):
    # Check if the input value is a valid integer or float
    try:
        float(value)
        return True
    except ValueError:
        return False

def submit():
    global monthly_rainfall, scaler
    # Get the values from each input widget and print them
    for i, input_widget in enumerate(inputs):
        value = input_widget.get()
        if validate_input(i, value):
            monthly_rainfall = np.concatenate([monthly_rainfall, [float(value)]])
        else:
            # monthly_rainfall.clear()
            monthly_rainfall = np.array([])
            messagebox.showerror("Invalid input", f"Invalid input for {months[i]}: {value}")
            return
    
    # Making predictions based on the user input
    if len(monthly_rainfall) == 12:
        monthly_rainfall = np.array(monthly_rainfall)
        monthly_rainfall_scaled = scaler.transform(monthly_rainfall.reshape(1, -1))
        prediction = best_model.predict(monthly_rainfall_scaled)[0]
        predicted_value.configure(text=f"{floods_dict[prediction]}")
        
        # Clear input values and reset monthly_rainfall
        for input_widget in inputs:
            input_widget.delete(0, 'end')
        # monthly_rainfall.clear()
        monthly_rainfall = np.array([])
    else:
        messagebox.showerror("Incomplete input", "Please enter rainfall amounts for all 12 months.")


root = tk.Tk()
root.title("Flood Prediction")
# root.geometry("350x440")

# Set the background color of the frame
root.configure(bg="#ccc")

# Add a text label above the input widgets
text_label = tk.Label(root, text="Enter the rainfall amounts for each month:")
text_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
text_label.configure(bg="white", fg="black", width=40)

# Define the labels and inputs for each month
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
labels = []
inputs = []
for i, month in enumerate(months):
    label = tk.Label(root, text=month, anchor="w")
    label.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
    label.configure(bg="white", fg="black", width=10)
    input_var = tk.StringVar()
    input_widget = tk.Entry(root, textvariable=input_var)
    input_widget.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
    input_var.trace("w", lambda name, index, mode, sv=input_var: validate_input(i, sv.get()))
    labels.append(label)
    inputs.append(input_widget)
    

prediction_text = tk.Label(root, text="PREDICTION")
prediction_text.grid(row=0, column=2, columnspan=2, padx=5, pady=10)

predicted_value = tk.Label(root, text="")
predicted_value.grid(row=1, column=2, columnspan=2, padx=5, pady=10)

# Add a button to submit the input values
submit_button = tk.Button(root, text="Submit", anchor=tk.CENTER, command=submit)
submit_button.grid(row=len(months)+1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Center the button within the window
root.grid_rowconfigure(len(months)+2, weight=1)
root.grid_columnconfigure(0, weight=1)
submit_button.grid(sticky="nsew")

root.mainloop()
