import tkinter as tk
from tkinter import messagebox
import random
import winsound
import time

class HairdryerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Hairdryer App")
        self.root.geometry("300x200")

        # Start with login window
        self.create_login_window()

    def create_login_window(self):
        # Create login window
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        
        tk.Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.login_window, text="Login", command=self.login).pack(pady=10)

        self.username = None

    def login(self):
        # Simple login check
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # For demo purposes, any non-empty login is considered valid
        if username and password:
            self.username = username
            self.login_window.destroy()
            self.setup_main_window()
        else:
            messagebox.showwarning("Login Failed", "Invalid username or password")

    def setup_main_window(self):
        # Create and show the main window
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Hairdryer Control")
        self.main_window.geometry("400x300")

        # Create and place widgets
        tk.Label(self.main_window, text=f"Welcome, {self.username}!", font=("Helvetica", 16)).pack(pady=10)

        self.start_button = tk.Button(self.main_window, text="Start", command=self.start_therapy)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.main_window, text="Stop", command=self.stop_therapy, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.status_label = tk.Label(self.main_window, text="Status: Inactive", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.temp_label = tk.Label(self.main_window, text="Temperature: -- °C", font=("Helvetica", 12))
        self.temp_label.pack(pady=5)

        self.speed_label = tk.Label(self.main_window, text="Fan Speed: -- RPM", font=("Helvetica", 12))
        self.speed_label.pack(pady=5)

        self.timer_label = tk.Label(self.main_window, text="Timer: 0 sec", font=("Helvetica", 12))
        self.timer_label.pack(pady=5)

        self.therapy_active = False
        self.start_time = None
        self.usage_data = []

    def start_therapy(self):
        if not self.therapy_active:
            self.therapy_active = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Therapy Active")
            self.start_time = time.time()
            self.usage_data = []
            self.simulate_therapy()
        else:
            messagebox.showinfo("Info", "Therapy is already active.")

    def stop_therapy(self):
        if self.therapy_active:
            self.therapy_active = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Therapy Stopped")
            self.generate_report()
        else:
            messagebox.showinfo("Info", "Therapy is not active.")

    def simulate_therapy(self):
        if self.therapy_active:
            # Simulate temperature and speed changes
            temperature = random.randint(20, 80)
            speed = random.randint(1000, 3000)

            # Update labels
            self.temp_label.config(text=f"Temperature: {temperature} °C")
            self.speed_label.config(text=f"Fan Speed: {speed} RPM")

            # Record usage data
            self.usage_data.append((temperature, speed))

            # Check for overheating
            if temperature > 70:
                temperature = max(20, temperature - 10)  # Decrease temperature, don't go below 20°C
                self.beep()
                self.status_label.config(text="Status: Overheating! Adjusting Temperature...")
            else:
                self.status_label.config(text="Status: Therapy Active")

            # Update every second
            self.root.after(1000, self.simulate_therapy)

    def beep(self):
        # Play a beep sound
        duration = 1000
        frequency = 440
        winsound.Beep(frequency, duration)

    def generate_report(self):
        if self.start_time:
            end_time = time.time()
            total_time = end_time - self.start_time
            average_temp = sum(temp for temp, _ in self.usage_data) / len(self.usage_data)
            average_speed = sum(speed for _, speed in self.usage_data) / len(self.usage_data)

            report = (
                f"User: {self.username}\n"
                f"Total Time: {total_time:.2f} seconds\n"
                f"Average Temperature: {average_temp:.2f} °C\n"
                f"Average Fan Speed: {average_speed:.2f} RPM\n"
            )

            messagebox.showinfo("Usage Report", report)

# Create the main root window
root = tk.Tk()
root.withdraw()  # Hide the root window initially
app = HairdryerApp(root)
root.mainloop()
