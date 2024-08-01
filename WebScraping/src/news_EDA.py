#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog

#%%
# Initialize Tkinter
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open file explorer and ask the user to select a file
file_path = filedialog.askopenfilename()

# Save the selected file path to a variable
path = file_path

# Print the file path (optional)
print("Selected file:", path)


# %%
df = pd.read_csv(path)
df = df.drop('Unnamed: 0', axis=1)

# %%
