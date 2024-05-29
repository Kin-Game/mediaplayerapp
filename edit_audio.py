import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import librosa
import vlc
from datetime import timedelta
from eq import Equalizer
from music_manage import MusicManagementFrame
from spectro import AudioAnalyzer
from view import ViewTab

class EditAudioTab(tk.Frame):
    def __init__(self, parent, media_player_app):
        super().__init__(parent)
        self.parent = parent
        self.media_player_app = media_player_app
        self.current_audio_file = None

        # Передача media_player у ViewTab при створенні об'єкта
        self.view_tab = ViewTab(self)
        self.media_player = self.view_tab.media_player

        # Головний фрейм з вкладкою
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Панель керування аудіо (зверху зліва)
        self.control_panel_frame = tk.Frame(self.main_frame, bg="white")
        self.control_panel_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Виведення часу та прогресу
        self.current_time_label = ttk.Label(self.control_panel_frame, text="Current Time: 00:00")
        self.current_time_label.grid(row=0, column=0, pady=5)

        self.total_time_label = ttk.Label(self.control_panel_frame, text="Total Time: 00:00")
        self.total_time_label.grid(row=0, column=1, pady=5)

        # Додамо кнопки керування аудіо
        self.play_button = ttk.Button(self.control_panel_frame, text="Play", command=self.play_file)
        self.play_button.grid(row=1, column=0, pady=5)

        self.pause_button = ttk.Button(self.control_panel_frame, text="Pause", command=self.pause_file)
        self.pause_button.grid(row=1, column=1, pady=5)

        self.stop_button = ttk.Button(self.control_panel_frame, text="Stop", command=self.stop_file)
        self.stop_button.grid(row=1, column=2, pady=5)

        self.backward_button = ttk.Button(self.control_panel_frame, text="Backward", command=self.rewind)
        self.backward_button.grid(row=1, column=3, pady=5)

        self.forward_button = ttk.Button(self.control_panel_frame, text="Forward", command=self.forward)
        self.forward_button.grid(row=1, column=4, pady=5)

        self.volume_label = ttk.Label(self.control_panel_frame, text="Volume:")
        self.volume_label.grid(row=2, column=0, pady=5)

        self.volume_scale = ttk.Scale(self.control_panel_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(100)
        self.volume_scale.grid(row=2, column=1, pady=5)

        # Комбобокс зі швидкістю відтворення 
        self.playback_speed_var = tk.StringVar(value="1.0") 
        self.speed_options = ["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"]
        self.speed_menu = ttk.Combobox(self.control_panel_frame, values=self.speed_options, textvariable=self.playback_speed_var)
        self.speed_menu.grid(row=2, column=2, pady=5, padx=(0, 10))  
        self.speed_menu.bind("<<ComboboxSelected>>", self.set_playback_speed)  

        self.progress_scale = ttk.Scale(self.control_panel_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_file, length=400)
        self.progress_scale.grid(row=3, column=0, columnspan=7, pady=5)

        # Мітка для відображення назви аудіо
        self.audio_name_label = ttk.Label(self.main_frame, text="Audio Name: ")
        self.audio_name_label.grid(row=1, column=0, columnspan=3)

        # Кнопка "Choose Audio" для головного фрейму
        self.choose_audio_button = ttk.Button(self.main_frame, text="Choose Audio", command=self.choose_audio)
        self.choose_audio_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Спектрограма
        self.spectrogram_frame = tk.Frame(self.main_frame, bg="white")
        self.spectrogram_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        self.audio_analyzer = AudioAnalyzer(self.spectrogram_frame)
        self.audio_analyzer.pack(fill="both", expand=True)

        # Еквалайзер
        self.equalizer_frame = tk.Frame(self.main_frame, bg="white")
        self.equalizer_frame.grid(row=0, column=3, rowspan=4, padx=10, pady=10, sticky="nsew")

        self.equalizer_tab = Equalizer(self.equalizer_frame, self)
        self.equalizer_tab.pack(fill="both", expand=True)

        # Керування музикою
        self.music_management_frame = MusicManagementFrame(self.main_frame)
        self.music_management_frame.grid(row=0, column=4, rowspan=5, sticky="nsew")

        # Кнопка "Save Filtered Audio"
        self.save_audio_button = ttk.Button(self.main_frame, text="Save Filtered Audio", command=self.save_filtered_audio)
        self.save_audio_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Налаштування розширення колонок і рядків
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        self.update_time_and_progress()
    # Метод для вибору аудіо
    def choose_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])

        if file_path:
            self.current_audio_file = file_path
            media = self.view_tab.instance.media_new(self.current_audio_file)
            self.view_tab.media_player.set_media(media)
            self.update_audio_name()

            audio, _ = librosa.load(file_path)
            self.equalizer_tab.set_audio(audio)

            # Аналіз аудіо для побудови спектрограми
            self.audio_analyzer.audio_file = file_path
            self.audio_analyzer.analyze_audio()
    # Метод для оновленн назви аудіо
    def update_audio_name(self):
        if self.current_audio_file:
            audio_name = os.path.basename(self.current_audio_file)
            self.audio_name_label.config(text=f"Audio Name: {audio_name}")
    # Метод для регулювання звуку
    def set_volume(self, value):
        self.view_tab.set_volume(value)
    # Метод для початку відтворення
    def play_file(self):
        self.view_tab.play_file()
    # Метод для паузи відтворення
    def pause_file(self):
        self.view_tab.pause_file()
    # Метод для зупинки відтворення
    def stop_file(self):
        self.view_tab.stop_file()
    # Метод для перемотки назад
    def rewind(self):
        self.view_tab.rewind()
    # Метод для перемотки вперед
    def forward(self):
        self.view_tab.forward()

    # Метод для встановлення швидкості відтворення
    def set_playback_speed(self, event=None):
        selected_speed = float(self.playback_speed_var.get()[:-1])  
        self.media_player.set_rate(selected_speed)

    def update_time_and_progress(self):
        if self.current_audio_file:
            current_time = self.view_tab.media_player.get_time()
            total_time = self.view_tab.media_player.get_length()

            current_time_str = str(timedelta(milliseconds=current_time))[:-7]
            total_time_str = str(timedelta(milliseconds=total_time))[:-7]

            self.current_time_label.config(text=f"Current Time: {current_time_str}")
            self.total_time_label.config(text=f"Total Time: {total_time_str}")

            if not self.view_tab.manual_seek:  
                position = self.view_tab.media_player.get_position()
                self.progress_scale.set(int(position * 100))

        self.parent.after(100, self.update_time_and_progress)

    def save_filtered_audio(self):
        if self.current_audio_file:
            save_path = filedialog.asksaveasfilename(defaultextension=".wav",
                                                     filetypes=[("WAV files", "*.wav")])
            if save_path:
                self.equalizer_tab.save_filtered_audio(save_path)
        else:
            print("No audio file selected for saving!")

    def seek_file(self, value):
        self.view_tab.seek_file(value)

    