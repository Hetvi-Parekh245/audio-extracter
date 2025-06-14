import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import threading
from PIL import Image, ImageTk

def select_file():
    file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4"), ("All files", "*.*")])
    if file:
        video_file.set(file)
        lbl_file.config(text=f"Selected: {os.path.basename(file)}")

def extract_audio():
    file = video_file.get()
    fmt = format_var.get()
    if not file:
        messagebox.showwarning("Warning", "Please select a video first.")
        return
    
    output_file = filedialog.asksaveasfilename(defaultextension=f".{fmt}",
                                             filetypes=[("Audio files", f"*.{fmt}")],
                                             title="Save Audio As")
    if not output_file:
        return
    
    progress_var.set(0)

    def process():
        try:
            clip = VideoFileClip(file)
            audio = clip.audio
            audio.write_audiofile(output_file, logger=None, fps=44100)

            for i in range(0, 100, 20):
                progress_var.set(i)
                root.update()
                
            progress_var.set(100)
            messagebox.showinfo("Success", f"Audio successfully extracted to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            extract_button.config(state='normal')

    extract_button.config(state='disabled')
    thread = threading.Thread(target=process)
    thread.start()


def on_enter(e):
    extract_button.config(bg="#9b59b6")

def on_leave(e):
    extract_button.config(bg="#8e44ad")

def on_select_file_hover(e):
    select_file_btn.config(bg="#9b59b6")

def on_select_file_leave(e):
    select_file_btn.config(bg="#8e44ad")

# Main application
root = tk.Tk()

img = Image.open("logo.png")
img.save("logo.ico")

root.iconbitmap("logo.ico")
root.title("Audio Extractor")
root.config(bg="#8f0439")
root.geometry("500x500")
root.minsize(400, 400)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.columnconfigure(0, weight=1)

# Title label
title = tk.Label(root, text="🎥 Audio Extractor Tool", font=('Helvetica', 20, 'bold'), fg="#ffffff", bg="#8f0439")
title.grid(row=0, column=0, pady=20, sticky='ew')

# File picker button
select_file_btn = tk.Button(root, text="Select Video File", command=select_file, font=('Helvetica', 14), 
                            bg="#8e44ad", fg="#ffffff", relief='flat')
select_file_btn.grid(row=1, column=0, pady=10, ipadx=20, ipady=10)

select_file_btn.bind("<Enter>", on_select_file_hover)
select_file_btn.bind("<Leave>", on_select_file_leave)

# Display selected file
video_file = tk.StringVar()
lbl_file = tk.Label(root, text="", font=('Helvetica', 14), fg="#ffffff", bg="#8f0439")
lbl_file.grid(row=2, column=0, pady=10)

# File format options
frame = tk.Frame(root, bg="#8f0439")
frame.grid(row=3, column=0, pady=10)

tk.Label(frame, text="Select Format :", font=('Helvetica', 18, 'bold'), fg="#ffffff", bg="#8f0439").pack(side='left')

format_var = tk.StringVar()
format_menu = ttk.Combobox(frame, textvariable=format_var, values=['mp3', 'wav'], state='readonly')
format_menu.pack(side='left', padx=10)
format_menu.set('mp3')

# Extract button
extract_button = tk.Button(root, text="Extract Audio", command=extract_audio, font=('Helvetica', 14), 
                           bg="#8e44ad", fg="#ffffff", relief='flat')
extract_button.grid(row=4, column=0, pady=10, ipadx=20, ipady=10)

extract_button.bind("<Enter>", on_enter)
extract_button.bind("<Leave>", on_leave)

# Progress bar
progress_var = tk.IntVar()
style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", troughcolor="#8f0439", background='#37dc2e')
progress = ttk.Progressbar(root, orient='horizontal', length=400, variable=progress_var, maximum=100, style="TProgressbar")
progress.grid(row=5, column=0, pady=20)

# Animated logo (optional, if you have a logo.png in directory)
try:
    img = Image.open("logo.png")
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)

    lbl_img = tk.Label(root, image=photo, bg="#8f0439")
    lbl_img.image = photo
    lbl_img.grid(row=6, column=0, pady=20)
except FileNotFoundError:
    pass

root.mainloop()
