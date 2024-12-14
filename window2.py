import os
import shutil
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import time

MONITORED_DIRECTORY = r"C:\Users\Muzahir\OneDrive\Desktop\cllg project"
SCREENSHOT_DIRECTORY = r"C:\Users\Muzahir\OneDrive\Desktop\screenshots"
monitored_folders = [
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\recordings",
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\key_mouse_logs",
    r"C:\Users\Muzahir\OneDrive\Desktop\cllg project\screenshots"
]

logging_enabled = True
suspicious_extensions = ['.exe', '.dll', '.sys', '.py', '.wav', '.png']

class AlertWindow:
    def __init__(self, message):
        self.root = tk.Tk()
        self.root.title("Suspicious Activity Detected")
        self.message = message
        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text=self.message).pack(pady=20, padx=20)
        close_button = tk.Button(self.root, text="Close", command=self.on_close_clicked)
        close_button.pack(pady=10)
        self.root.mainloop()

    def on_close_clicked(self):
        global logging_enabled
        print("Deleting newly created files and folders...")
        self.delete_newly_created()
        logging_enabled = False
        self.root.destroy()

    def delete_newly_created(self):
        for item in os.listdir(MONITORED_DIRECTORY):
            full_path = os.path.join(MONITORED_DIRECTORY, item)
            if os.path.exists(full_path):
                try:
                    if os.path.isfile(full_path) or os.path.islink(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                except Exception as e:
                    print(f"Error deleting {full_path}: {e}")

        if os.path.exists(SCREENSHOT_DIRECTORY):
            try:
                shutil.rmtree(SCREENSHOT_DIRECTORY)
                print("Screenshot directory deleted successfully.")
            except Exception as e:
                print(f"Error deleting screenshot directory: {e}")
        else:
            print("...")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.previous_features = {folder: self.extract_features(folder) for folder in monitored_folders}

    def on_any_event(self, event):
        if event.is_directory and logging_enabled:
            try:
                for folder in monitored_folders:
                    current_features = self.extract_features(folder)
                    label = self.label_data(current_features, self.previous_features[folder])
                    self.previous_features[folder] = current_features
                    if label == 1:
                        print("Suspicious activity detected. Showing alert window...")
                        alert_window = AlertWindow("Suspicious activity detected.")
                        break
            except Exception as e:
                print(f"Error processing event: {e}")

    def extract_features(self, folder_path):
        try:
            files = os.listdir(folder_path)
            num_files = len(files)
            total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in files)
            avg_size = total_size / num_files if num_files > 0 else 0
            return [num_files, total_size, avg_size]
        except FileNotFoundError:
            print(f"Folder '{folder_path}' not found.")
            return [0, 0, 0]

    def label_data(self, current_features, previous_features):
        return 1 if current_features != previous_features else 0

def start_file_monitoring(handler):
    observer = Observer()
    observer.schedule(handler, MONITORED_DIRECTORY, recursive=True)
    observer.start()
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    handler = FileChangeHandler()
    start_file_monitoring(handler)

if __name__ == "__main__":
    main()
