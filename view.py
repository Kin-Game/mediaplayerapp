import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import vlc
from datetime import timedelta

class ViewTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Ініціалізація VLC та створення відтворювача медіа
        self.instance = vlc.Instance("--no-xlib")
        self.media_player = self.instance.media_player_new()
        self.current_file = None 
        self.manual_seek = True
        
        # Створення віджетів
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Кнопка для вибору медіафайлу
        self.choose_file_button = ttk.Button(self, text="Choose Media File", command=self.choose_file)
        self.choose_file_button.grid(row=0, column=0, pady=10)
        
        # Відео відтворення
        self.video_frame = ttk.Frame(self)
        self.video_frame.grid(row=1, column=0, sticky="nsew")
        
        # Підготовка відео відтворення
        self.video_canvas = tk.Canvas(self.video_frame)
        self.video_canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.video_canvas.bind("<Configure>", self.resize)
        
        # Шкала для перемотування відео
        self.seek_scale = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_file)
        self.seek_scale.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        # Виведення часу та прогресу під шкалою прогресу
        self.time_frame = ttk.Frame(self)
        self.time_frame.grid(row=3, column=0, pady=5, sticky="ew")

        self.current_time_label = ttk.Label(self.time_frame, text="Current Time: 00:00")
        self.current_time_label.grid(row=0, column=0, padx=5)

        self.total_time_label = ttk.Label(self.time_frame, text="Total Time: 00:00")
        self.total_time_label.grid(row=0, column=1, padx=5)
        
        # Кнопки управління відтворенням
        self.controls_frame = ttk.Frame(self)
        self.controls_frame.grid(row=4, column=0, pady=10, sticky="ew")

        self.play_button = ttk.Button(self.controls_frame, text="Play", command=self.play_file)
        self.play_button.grid(row=0, column=0, padx=10)
        
        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.pause_file)
        self.pause_button.grid(row=0, column=1, padx=10)
        
        self.stop_button = ttk.Button(self.controls_frame, text="Stop", command=self.stop_file)
        self.stop_button.grid(row=0, column=2, padx=10)
        
        self.rewind_button = ttk.Button(self.controls_frame, text="Rewind", command=self.rewind)
        self.rewind_button.grid(row=0, column=3, padx=10)
        
        self.forward_button = ttk.Button(self.controls_frame, text="Forward", command=self.forward)
        self.forward_button.grid(row=0, column=4, padx=10)
        
        # Шкала для регулювання гучності
        self.volume_scale = ttk.Scale(self.controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(100)  
        self.volume_scale.grid(row=0, column=5, padx=10)
        
        # Назва файлу
        self.file_label = ttk.Label(self, text="")
        self.file_label.grid(row=5, column=0, pady=5)
        
        # Список для вибору швидкості відтворення
        self.playback_speed_var = tk.StringVar(value="1.0")  
        self.speed_options = ["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"]
        self.speed_menu = ttk.Combobox(self, values=self.speed_options, textvariable=self.playback_speed_var)
        self.speed_menu.grid(row=6, column=0, pady=5)
        self.speed_menu.bind("<<ComboboxSelected>>", self.set_playback_speed)  
        
        # Оновлення параметрів
        self.update_time_and_progress()

    # Метод для зміни розміру відео
    def resize(self, event):
        self.media_player.set_hwnd(self.video_canvas.winfo_id())
        
    # Метод для вибору медіафайлу
    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Media files", "*.mp3;*.wav;*.mp4;*.avi;*.jpeg;*.jpg;*.png;*.gif")])

        if file_path:
            self.current_file = file_path
            media = self.instance.media_new(self.current_file)
            self.media_player.set_media(media)
            self.media_player.play()
            self.update_file_label()  

    # Метод для відтворення медіа
    def play_file(self):
        self.media_player.play()

    # Метод для паузи медіа
    def pause_file(self):
        self.media_player.pause()
        
    # Метод для зупинки медіа
    def stop_file(self):
        self.media_player.stop()
        
    # Метод для перемотування медіа назад
    def rewind(self):
        self.media_player.set_time(self.media_player.get_time() - 5000)
        
    # Метод для перемотування медіа вперед
    def forward(self):
        self.media_player.set_time(self.media_player.get_time() + 5000)
        
    # Метод для регулювання гучності медіа
    def set_volume(self, value):
        volume = float(value)
        self.media_player.audio_set_volume(int(volume))
        
    # Метод для перемотування медіа
    def seek_file(self, value):
        position = float(value) / 100.0
        self.media_player.set_position(position)
        
    # Метод для встановлення швидкості відтворення
    def set_playback_speed(self, event=None):
        selected_speed = float(self.playback_speed_var.get()[:-1]) 
        self.media_player.set_rate(selected_speed)
    
    # Метод для оновлення часу та прогресу відтворення   
    def update_time_and_progress(self):
        if self.current_file:
            current_time = self.media_player.get_time()
            total_time = self.media_player.get_length()

            current_time_str = str(timedelta(milliseconds=current_time))[:-7]
            total_time_str = str(timedelta(milliseconds=total_time))[:-7]

            self.current_time_label.config(text=f"Current Time: {current_time_str}")
            self.total_time_label.config(text=f"Total Time: {total_time_str}")

            if not self.manual_seek:
                position = self.media_player.get_position()
                self.seek_scale.set(int(position * 100))

        self.master.after(100, self.update_time_and_progress)
     
    # Метод для оновлення назви файлу
    def update_file_label(self):
        if self.current_file:
            file_name = os.path.basename(self.current_file)  
            self.file_label.config(text=f"Playing: {file_name}")


