import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import time

def extract_features(folder_path):
    try:
        files = os.listdir(folder_path)
        num_files = len(files)
        total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in files)
        avg_size = total_size / num_files if num_files > 0 else 0
        return [num_files, total_size, avg_size]
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
        return [0, 0, 0]

def label_data(current_features, previous_features):
    if current_features != previous_features:
        return 1
    return 0 

monitored_folders = [
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\recordings",
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\key_mouse_logs",
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\screenshots"
]
previous_features = {folder: extract_features(folder) for folder in monitored_folders}
while True:
    for folder in monitored_folders:
        current_features = extract_features(folder)
        label = label_data(current_features, previous_features[folder])
        print(f"Label for monitored folder '{folder}':", label)
        previous_features[folder] = current_features
    time.sleep(5)
