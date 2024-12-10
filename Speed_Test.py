import tkinter as tk
from tkinter import ttk
import os
import time
from threading import Thread

class SSDSpeedTester(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SSD/HDD Speed Test - TheZ")
        self.configure(bg='black')
        self.geometry("600x400")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")
        
        style = ttk.Style()
        style.configure("Hacker.TLabel", foreground="lime", background="black")
        style.configure("Hacker.TButton", foreground="lime", background="black")
        
        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.size_label = tk.Label(self.main_frame, text="File Size (MB):", fg="lime", bg="black")
        self.size_label.pack()
        self.size_var = tk.StringVar(value="500")
        self.size_entry = tk.Entry(self.main_frame, bg="black", fg="lime", insertbackground="lime")
        self.size_entry.insert(0, "500")
        self.size_entry.pack()
        
        self.iter_label = tk.Label(self.main_frame, text="Retry:", fg="lime", bg="black")
        self.iter_label.pack()
        self.iter_var = tk.StringVar(value="3")
        self.iter_entry = tk.Entry(self.main_frame, bg="black", fg="lime", insertbackground="lime")
        self.iter_entry.insert(0, "3")
        self.iter_entry.pack()
        
        self.result_text = tk.Text(self.main_frame, height=10, bg="black", fg="lime")
        self.result_text.pack(pady=10, fill='both', expand=True)
        
        self.start_button = tk.Button(self.main_frame, text="START TEST", 
                                    command=self.start_test,
                                    bg="black", fg="lime", activebackground="green")
        self.start_button.pack(pady=10)
        
    def log(self, message):
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        
    def test_ssd_speed(self):
        try:
            file_size_mb = int(self.size_entry.get())
            iterations = int(self.iter_entry.get())
            
            test_file = "test_file.tmp"
            file_size_bytes = file_size_mb * 1024 * 1024
            data = os.urandom(file_size_bytes)
            
            total_write = 0
            total_read = 0
            
            for i in range(iterations):
                self.log(f"Test {i+1}/{iterations}")
                
                start_time = time.time()
                with open(test_file, "wb") as f:
                    f.write(data)
                write_time = time.time() - start_time
                write_speed = file_size_mb / write_time
                total_write += write_speed
                self.log(f"Write: {write_speed:.2f} MB/s")
                
                start_time = time.time()
                with open(test_file, "rb") as f:
                    f.read()
                read_time = time.time() - start_time
                read_speed = file_size_mb / read_time
                total_read += read_speed
                self.log(f"Read: {read_speed:.2f} MB/s")
            
            if os.path.exists(test_file):
                os.remove(test_file)
            
            avg_write = total_write / iterations
            avg_read = total_read / iterations
            self.log(f"\nAVG Write: {avg_write:.2f} MB/s")
            self.log(f"AVG Read: {avg_read:.2f} MB/s")
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
        finally:
            self.start_button.config(state="normal")
    
    def start_test(self):
        self.result_text.delete(1.0, tk.END)
        self.start_button.config(state="disabled")
        Thread(target=self.test_ssd_speed, daemon=True).start()

if __name__ == "__main__":
    app = SSDSpeedTester()
    app.mainloop()
