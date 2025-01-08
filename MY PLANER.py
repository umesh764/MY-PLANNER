import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import datetime

# DailyAssistant Class for Family Planner
class DailyAssistant:
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.tasks = []
        self.preferences = {
            "wake_up_time": "5:30 AM",  # Wake-up time
            "water_intake": "2 Liters",
            "exercise": "30 minutes",
        }
        
        # Create Notebook (Tab System)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, expand=True)

        # Create Tabs
        self.create_tabs()

    def create_tabs(self):
        # Task Tab
        self.tasks_frame = tk.Frame(self.notebook, bg="#E0F7FA")
        self.tasks_tab = tk.Label(self.tasks_frame, text="टास्क", font=("Arial", 24), bg="#E0F7FA", fg="#00796B")
        self.tasks_tab.pack(pady=20)
        
        # Add Task Button in Task Tab
        self.add_task_button = tk.Button(self.tasks_frame, text="टास्क जोड़ें", font=("Arial", 14), bg="#00796B", fg="white", command=self.add_task)
        self.add_task_button.pack(pady=10)
        
        # Task Listbox in Task Tab
        self.task_listbox = tk.Listbox(self.tasks_frame, width=50, height=10, font=("Arial", 12), bg="#FFFFFF", fg="#00796B")
        self.task_listbox.pack(pady=20)
        
        self.notebook.add(self.tasks_frame, text="टास्क")

        # Reminder Tab
        self.reminder_frame = tk.Frame(self.notebook, bg="#FFEBEE")
        self.reminder_tab = tk.Label(self.reminder_frame, text="रिमाइंडर", font=("Arial", 24), bg="#FFEBEE", fg="#FF4081")
        self.reminder_tab.pack(pady=20)

        self.reminder_button = tk.Button(self.reminder_frame, text="रिमाइंडर सेट करें", font=("Arial", 14), bg="#FF9800", fg="white", command=self.set_reminder)
        self.reminder_button.pack(pady=10)
        
        self.notebook.add(self.reminder_frame, text="रिमाइंडर")

        # Profile Tab
        self.profile_frame = tk.Frame(self.notebook, bg="#FFF3E0")
        self.profile_tab = tk.Label(self.profile_frame, text="प्रोफ़ाइल", font=("Arial", 24), bg="#FFF3E0", fg="#FF5722")
        self.profile_tab.pack(pady=20)

        # Profile Info
        self.profile_info = tk.Label(self.profile_frame, text=f"नाम: {self.name}\nजागने का समय: {self.preferences['wake_up_time']}\nपानी पीने की मात्रा: {self.preferences['water_intake']}\nव्यायाम का समय: {self.preferences['exercise']}",
                                     font=("Arial", 14), bg="#FFF3E0", fg="#FF5722")
        self.profile_info.pack(pady=10)

        self.notebook.add(self.profile_frame, text="प्रोफ़ाइल")

        # Start Day Button
        self.start_day_button = tk.Button(self.root, text="अपना दिन शुरू करें", font=("Arial", 14), bg="#FF4081", fg="white", command=self.start_day)
        self.start_day_button.pack(pady=10)

        # Default Schedule
        self.schedule = [
            ("जागना", "5:30 AM", 0),
            ("गार्डन जाएं", "6:10 AM", 40),
            ("घर लौटें", "6:35 AM", 25),
            ("चाय पिएं", "6:45 AM", 10),
            ("देवांश की तैयारी करें", "7:00 AM", 15),
            ("देवांश को स्कूल बस तक भेजें", "7:30 AM", 30),
            ("ऑफिस के लिए तैयार हो जाएं", "8:00 AM", 45),
            ("ऑफिस के लिए निकलें", "9:00 AM", 30),
            ("ऑफिस पहुंचें", "9:30 AM", 0),
            ("पानी पिएं", "9:30 AM", 5),
            ("वाशरूम जाएं", "9:35 AM", 5),
            ("ऑफिस का काम करें", "9:45 AM", 45),
            ("बिल बुकिंग करें", "10:30 AM", 5),
            ("छोटा ब्रेक लें", "10:35 AM", 5),
            ("लंच ब्रेक", "1:30 PM", 60),
            ("ऑफिस से बाहर निकलें", "6:00 PM", 0),
            ("गौरवी को फोन करें", "6:15 PM", 15),
            ("देवांश को ट्यूशन से घर लाएं", "7:00 PM", 45),
            ("देवांश को खाना खिलाएं", "9:00 PM", 45),
            ("रात का खाना खाएं", "9:45 PM", 15)
        ]

    def add_task(self):
        task = simpledialog.askstring("टास्क जोड़ें", "अपना टास्क दर्ज करें:", parent=self.root)
        if task:
            time_str = simpledialog.askstring("समय सेट करें", "इस टास्क के लिए समय मिनटों में दर्ज करें:", parent=self.root)
            try:
                task_time = int(time_str)
                self.tasks.append((task, task_time))
                self.update_task_list()
            except ValueError:
                messagebox.showerror("गलत इनपुट", "कृपया समय के लिए एक सही संख्या दर्ज करें।")
        
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task, time in self.tasks:
            self.task_listbox.insert(tk.END, f"{task} - {time} मिनट")

    def start_day(self):
        tasks = "\n".join([f"{task[0]} at {task[1]}" for task in self.schedule]) if self.schedule else "कोई टास्क नहीं जोड़ा गया है।"
        suggestion_message = f"आज के लिए आपके टास्क:\n{tasks}"
        messagebox.showinfo("अपना दिन शुरू करें", suggestion_message)

        # Start reminder threads
        for task, time_str, _ in self.schedule:
            threading.Thread(target=self.set_timer, args=(task, time_str)).start()

    def set_timer(self, task, time_str):
        # Convert string time like '5:30 AM' to time object
        task_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
        current_time = datetime.datetime.now().time()
        time_difference = datetime.datetime.combine(datetime.date.today(), task_time) - datetime.datetime.combine(datetime.date.today(), current_time)
        
        # If the time has passed for today, schedule it for the next day
        if time_difference.total_seconds() < 0:
            time_difference = datetime.timedelta(days=1) + time_difference

        time.sleep(time_difference.total_seconds())
        self.reminder(task)

    def reminder(self, task):
        messagebox.showinfo("रिमाइंडर", f"अब आपका टास्क है: {task}")

    def set_reminder(self):
        task = simpledialog.askstring("रिमाइंडर", "अपना रिमाइंडर टास्क दर्ज करें:", parent=self.root)
        if task:
            time_str = simpledialog.askstring("रिमाइंडर सेट करें", "इस रिमाइंडर के लिए समय मिनटों में दर्ज करें:", parent=self.root)
            try:
                reminder_time = int(time_str)
                threading.Thread(target=self.set_timer, args=(task, reminder_time)).start()
                messagebox.showinfo("रिमाइंडर सेट", f"{task} के लिए {reminder_time} मिनट में रिमाइंडर सेट किया गया है।")
            except ValueError:
                messagebox.showerror("गलत इनपुट", "कृपया समय के लिए एक सही संख्या दर्ज करें।")

# Main function to run the application
def main():
    name = input("अपना नाम दर्ज करें: ")

    # Set up Tkinter root window
    root = tk.Tk()
    assistant = DailyAssistant(root, name)
    
    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()