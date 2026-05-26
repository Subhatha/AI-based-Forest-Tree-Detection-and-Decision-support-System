import os
import threading
import tkinter as tk
import subprocess
from tkinter import filedialog, messagebox
from frame_extractor import extract_frames
from tree_detector import detect_trees
from video_generator import create_video
from map_generator import create_3d_map
from stats_generator import generate_summary, save_summary
from tkinter import ttk
from interactive_map_generator import create_interactive_3d_map

video_path = ""

OUTPUT_DIR = "gui_output"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
DETECTED_DIR = os.path.join(OUTPUT_DIR, "detected_frames")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "detected_video.mp4")
OUTPUT_MAP = os.path.join(OUTPUT_DIR, "tree_3d_map.png")
OUTPUT_INTERACTIVE_MAP = os.path.join(OUTPUT_DIR, "interactive_3d_map.html")


def log(message):
    status_label.config(text=message)
    root.update_idletasks()


def select_video():
    global video_path
    video_path = filedialog.askopenfilename(
        title="Select Forest Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
    )

    if video_path:
        video_label.config(text=f"Selected: {video_path}")

def set_progress(value):
    progress_bar["value"] = value
    root.update_idletasks()


def run_pipeline():
    try:
        if not video_path:
            messagebox.showerror("Error", "Please select a video first.")
            return

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        log("Extracting frames...")
        set_progress(20)
        frame_count = extract_frames(video_path, FRAMES_DIR)

        log("Detecting trees and applying decisions...")
        set_progress(45)
        stats = detect_trees(FRAMES_DIR, DETECTED_DIR)

        summary = generate_summary(stats, frame_count)
        save_summary(summary, os.path.join(OUTPUT_DIR, "summary_report.txt"))

        stats_panel.config(
    text=(
        f"Frames: {summary['frames']} | "
        f"Trees: {summary['total']} | "
        f"CUT: {summary['cut']} | "
        f"KEEP: {summary['keep']}"
    )
)

        log("Creating detected video...")
        set_progress(70)
        create_video(DETECTED_DIR, OUTPUT_VIDEO)

        log("Creating 3D map...")
        set_progress(90)
        create_3d_map(FRAMES_DIR, OUTPUT_MAP)

        log("Creating interactive 3D map...")
        create_interactive_3d_map(FRAMES_DIR, OUTPUT_INTERACTIVE_MAP)

        set_progress(100)


        stats_text = (
            f"Completed successfully!\n\n"
            f"Frames extracted: {summary['frames']}\n"
            f"Total tree detections: {summary['total']}\n"
            f"Trees marked CUT: {summary['cut']} ({summary['cut_percent']}%)\n"
            f"Trees marked KEEP: {summary['keep']} ({summary['keep_percent']}%)\n\n"
            f"Output folder: {OUTPUT_DIR}"
        )

        log("Completed successfully!")
        messagebox.showinfo("System Results", stats_text)

    except Exception as e:
        log("Error occurred.")
        messagebox.showerror("Error", str(e))


def start_pipeline():
    threading.Thread(target=run_pipeline).start()


def open_output_folder():
    if os.path.exists(OUTPUT_DIR):
        subprocess.Popen(f'explorer "{OUTPUT_DIR}"')
    else:
        messagebox.showerror("Error", "Output folder does not exist yet.")


root = tk.Tk()
root.title("AI Forest Tree Detection System")
root.geometry("700x430")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="AI-Based Forest Tree Detection System",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Video → Tree Detection → Cut/Keep Decision → 3D Map",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
)
subtitle.pack(pady=5)

select_button = tk.Button(
    root,
    text="Select Video",
    font=("Arial", 12),
    command=select_video,
    width=25,
    bg="#2d7d46",
    fg="white",
    activebackground="#3fa65c",
    activeforeground="white"
)
select_button.pack(pady=10)

video_label = tk.Label(
    root,
    text="No video selected",
    wraplength=600,
    bg="#1e1e1e",
    fg="white"
)
video_label.pack(pady=10)

run_button = tk.Button(
    root,
    text="Run Full System",
    font=("Arial", 12, "bold"),
    command=start_pipeline,
    width=25,
    bg="#2d7d46",
    fg="white",
    activebackground="#3fa65c",
    activeforeground="white"
)
run_button.pack(pady=10)

open_button = tk.Button(
    root,
    text="Open Output Folder",
    font=("Arial", 11),
    command=open_output_folder,
    width=25,
    bg="#2d7d46",
    fg="white",
    activebackground="#3fa65c",
    activeforeground="white"
)
open_button.pack(pady=5)

status_label = tk.Label(
    root,
    text="Waiting...",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
)
status_label.pack(pady=20)

progress_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=500,
    mode="determinate"
)
progress_bar.pack(pady=10)
stats_panel = tk.Label(
    root,
    text="Frames: 0 | Trees: 0 | CUT: 0 | KEEP: 0",
    font=("Arial", 11, "bold"),
    bg="#1e1e1e",
    fg="#00ff88"
)
stats_panel.pack(pady=10)

footer = tk.Label(
    root,
    text="Green = CUT | Red = KEEP",
    font=("Arial", 11, "bold"),
    bg="#1e1e1e",
    fg="white"
)
footer.pack(pady=10)

root.mainloop()
