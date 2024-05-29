import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, font
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

from view import ViewTab

class EditVideoTab(ViewTab):
    def __init__(self, master, media_player_app=None):
        super().__init__(master)
        
        # Ініціалізація властивостей
        self.current_video_file = self.select_video_file()  
        self.current_audio_file = None  
        self.video_duration = self.get_video_duration(self.current_video_file)

        self.create_additional_widgets()
    
    # Метод для створення додаткових віджетів
    def create_additional_widgets(self):
        
        # Налаштування рядків сітки
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

# Створення елементів інтерфейсу для керування часом, аудіо, текстом
        self.start_time_label = ttk.Label(self, text="Start Time: 00:00")
        self.start_time_label.grid(row=10, column=0, pady=5, sticky='e')

        self.start_time_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_start_time_label)
        self.start_time_scale.grid(row=10, column=1, pady=5, sticky='w')

        self.end_time_label = ttk.Label(self, text="End Time: 00:00")
        self.end_time_label.grid(row=10, column=2, pady=5, sticky='e')

        self.end_time_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_end_time_label)
        self.end_time_scale.grid(row=10, column=3, pady=5, sticky='w')

        self.audio_label = ttk.Label(self, text="Select Audio File:")
        self.audio_label.grid(row=10, column=4, pady=5, sticky='e')

        self.audio_button = ttk.Button(self, text="Browse", command=self.select_audio_file)
        self.audio_button.grid(row=10, column=5, pady=5, sticky='w')

        self.music_start_label = ttk.Label(self, text="Music Start Time: 00:00")
        self.music_start_label.grid(row=11, column=0, pady=5, sticky='e')

        self.music_start_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_music_start_label)
        self.music_start_scale.grid(row=11, column=1, pady=5, sticky='w')

        self.music_end_label = ttk.Label(self, text="Music End Time: 00:00")
        self.music_end_label.grid(row=11, column=2, pady=5, sticky='e')

        self.music_end_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_music_end_label)
        self.music_end_scale.grid(row=11, column=3, pady=5, sticky='w')

        self.text_label = ttk.Label(self, text="Text to add:")
        self.text_label.grid(row=11, column=4, pady=5, sticky='e')

        self.text_entry = tk.Entry(self)
        self.text_entry.grid(row=11, column=5, pady=5, sticky='w')

        self.font_label = ttk.Label(self, text="Font:")
        self.font_label.grid(row=12, column=0, pady=5, sticky='e')

        self.font_var = tk.StringVar()
        self.font_dropdown = ttk.Combobox(self, textvariable=self.font_var)
        self.font_dropdown['values'] = font.families()
        self.font_dropdown.grid(row=12, column=1, pady=5, sticky='w')

        self.size_label = ttk.Label(self, text="Size:")
        self.size_label.grid(row=12, column=2, pady=5, sticky='e')

        self.size_var = tk.IntVar(value=20)
        self.size_spinbox = tk.Spinbox(self, from_=8, to=72, textvariable=self.size_var)
        self.size_spinbox.grid(row=12, column=3, pady=5, sticky='w')

        self.color_label = ttk.Label(self, text="Color:")
        self.color_label.grid(row=12, column=4, pady=5, sticky='e')

        self.color_var = tk.StringVar(value='#FFFFFF')
        self.color_button = ttk.Button(self, text="Choose Color", command=self.choose_color)
        self.color_button.grid(row=12, column=5, pady=5, sticky='w')

        self.position_label = ttk.Label(self, text="Position (x, y):")
        self.position_label.grid(row=13, column=0, pady=5, sticky='e')

        self.position_entry = tk.Entry(self)
        self.position_entry.grid(row=13, column=1, pady=5, sticky='w')
        self.position_entry.insert(0, "10, 10")

        self.text_start_label = ttk.Label(self, text="Text Start Time: 00:00")
        self.text_start_label.grid(row=13, column=2, pady=5, sticky='e')

        self.text_start_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_text_start_label)
        self.text_start_scale.grid(row=13, column=3, pady=5, sticky='w')

        self.text_end_label = ttk.Label(self, text="Text End Time: 00:00")
        self.text_end_label.grid(row=13, column=4, pady=5, sticky='e')

        self.text_end_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_text_end_label)
        self.text_end_scale.grid(row=13, column=5, pady=5, sticky='w')

        self.save_button = ttk.Button(self, text="Save Trimmed Video", command=self.save_trimmed_video)
        self.save_button.grid(row=14, column=0, columnspan=6, pady=10)

    # Метод для вибору кольору тексту
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        self.color_var.set(color_code)

    # Метод для вибору відеофайлу
    def select_video_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            return file_path
        else:
            messagebox.showerror("Error", "No video file selected.")
            return None

    # Метод для вибору аудіофайлу
    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        if file_path:
            self.current_audio_file = file_path
        else:
            messagebox.showerror("Error", "No audio file selected.")

    # Методи для оновлення міток часу
    def update_start_time_label(self, value):
        if self.video_duration > 0:
            start_time = float(value) * self.video_duration / 100
            self.start_time_label.config(text=f"Start Time: {self.format_time(start_time)}")

    def update_end_time_label(self, value):
        if self.video_duration > 0:
            end_time = float(value) * self.video_duration / 100
            self.end_time_label.config(text=f"End Time: {self.format_time(end_time)}")

    def update_music_start_label(self, value):
        if self.video_duration > 0:
            start_time = float(value) * self.video_duration / 100
            self.music_start_label.config(text=f"Music Start Time: {self.format_time(start_time)}")

    def update_music_end_label(self, value):
        if self.video_duration > 0:
            end_time = float(value) * self.video_duration / 100
            self.music_end_label.config(text=f"Music End Time: {self.format_time(end_time)}")

    def update_text_start_label(self, value):
        if self.video_duration > 0:
            start_time = float(value) * self.video_duration / 100
            self.text_start_label.config(text=f"Text Start Time: {self.format_time(start_time)}")

    def update_text_end_label(self, value):
        if self.video_duration > 0:
            end_time = float(value) * self.video_duration / 100
            self.text_end_label.config(text=f"Text End Time: {self.format_time(end_time)}")

    # Метод для форматування часу
    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"

    # Метод для збереження відеофайлу з використанням заданих параметрів
    def save_trimmed_video(self):
        if not self.current_video_file:
            messagebox.showerror("Error", "No video file selected.")
            return

        if self.current_audio_file is None:
            messagebox.showerror("Error", "No audio file selected.")
            return

        start_time = self.start_time_scale.get() * self.video_duration / 100
        end_time = self.end_time_scale.get() * self.video_duration / 100

        music_start_time = self.music_start_scale.get() * self.video_duration / 100
        music_end_time = self.music_end_scale.get() * self.video_duration / 100

        text_start_time = self.text_start_scale.get() * self.video_duration / 100
        text_end_time = self.text_end_scale.get() * self.video_duration / 100

        text = self.text_entry.get()
        font_name = self.font_var.get()
        font_size = self.size_var.get()
        color = self.color_var.get()
        position = tuple(map(int, self.position_entry.get().split(',')))

        try:
            video_clip = VideoFileClip(self.current_video_file).subclip(start_time, end_time)
            original_audio_clip = video_clip.audio

            # Створення нового аудіо кліпу
            new_audio_clip = AudioFileClip(self.current_audio_file).subclip(music_start_time, music_end_time)
            new_audio_clip = new_audio_clip.set_start(music_start_time - start_time)
            
            # З'єднання оригінального звуку із новим
            final_audio_clip = CompositeAudioClip([original_audio_clip, new_audio_clip])
            final_audio_clip = final_audio_clip.set_duration(video_clip.duration)

            # Встановалення аудіо до відео
            video_clip = video_clip.set_audio(final_audio_clip)

            # Створення тексту
            img = Image.new('RGBA', (video_clip.w, video_clip.h), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            pil_font_path = os.path.join("C:/Windows/Fonts", font_name + ".ttf")  # Ensure the correct path
            pil_font = ImageFont.truetype(pil_font_path, font_size)
            draw.text(position, text, font=pil_font, fill=color)

            txt_img = np.array(img)
            text_clip = ImageClip(txt_img, duration=video_clip.duration)

            # З'єднння відео та тексту
            final_video_clip = CompositeVideoClip([video_clip, text_clip.set_start(text_start_time).set_end(text_end_time)])

            save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if save_path:
                final_video_clip.write_videofile(save_path, codec="libx264", fps=24)
                messagebox.showinfo("Success", "Video successfully trimmed and saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Error trimming video: {e}")

    # Метод для отримання тривалості відеофайлу
    def get_video_duration(self, file_path):
        try:
            video_clip = VideoFileClip(file_path)
            return video_clip.duration
        except Exception as e:
            messagebox.showerror("Error", f"Error getting video duration: {e}")
            return 0
