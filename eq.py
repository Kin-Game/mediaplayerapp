import tempfile
import tkinter as tk
from tkinter import ttk
import vlc 
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import threading

class Equalizer(tk.Frame):
    def __init__(self, parent, edit_audio_tab):
        super().__init__(parent)
        self.parent = parent
        self.edit_audio_tab = edit_audio_tab
        self.audio = None  

        # Ініціалізуємо VLC
        self.instance = vlc.Instance("--no-xlib")
        self.media_player = self.instance.media_player_new()

        # Головний фрейм еквалайзера
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Налаштування фільтрів
        self.filters_frame = ttk.LabelFrame(self.main_frame, text="Equalizer Filters")
        self.filters_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Створення повзунків для кожної частоти
        self.frequency_sliders = {}
        self.create_frequency_sliders()

        # Створення кнопок пресетів
        self.presets_frame = ttk.LabelFrame(self.main_frame, text="Presets")
        self.presets_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.create_presets_buttons()

    #Метод для створення списку частот та їх значень
    def create_frequency_sliders(self):
        frequencies = [("31 Hz", 0), ("62 Hz", 0), ("125 Hz", 0), ("250 Hz", 0), ("500 Hz", 0),
                    ("1 kHz", 0), ("2 kHz", 0), ("4 kHz", 0), ("8 kHz", 0), ("16 kHz", 0)]

        for freq, default_value in frequencies:
            frame = ttk.Frame(self.filters_frame)
            frame.pack(fill="x", pady=5)

            label = ttk.Label(frame, text=freq)
            label.pack(side="left", padx=5)

            slider = ttk.Scale(frame, from_=-12, to=12, orient="horizontal", length=200)
            slider.set(default_value)
            slider.pack(side="right", padx=5)

            slider.bind("<ButtonRelease-1>", lambda _: self.update_audio())

            self.frequency_sliders[freq] = slider
    
    # Метод для відтворення аудіо
    def play_audio(self, audio):
        audio_array = np.array(audio.get_array_of_samples())
        sd.play(audio_array, audio.frame_rate)
        sd.wait()
    
    # Метод створення кнопок пресетів еквалайзера
    def create_presets_buttons(self):
        presets = ["Flat", "Rock", "Pop", "Classical", "Bass Boost", "Treble Boost"]

        for preset in presets:
            button = ttk.Button(self.presets_frame, text=preset, command=lambda p=preset: self.apply_preset(p))
            button.pack(side="left", padx=10, pady=5)
    
    # Метод встановлення всіх повзунків на вказане значення
    def apply_preset(self, preset):
        if preset == "Flat":
            self.set_all_sliders_to(0)
        elif preset == "Rock":
            self.set_all_sliders_to(3)
            self.frequency_sliders["125 Hz"].set(6)
            self.frequency_sliders["500 Hz"].set(3)
            self.frequency_sliders["1 kHz"].set(-3)
            self.frequency_sliders["2 kHz"].set(-3)
        elif preset == "Pop":
            self.set_all_sliders_to(3)
            self.frequency_sliders["125 Hz"].set(3)
            self.frequency_sliders["1 kHz"].set(3)
            self.frequency_sliders["8 kHz"].set(3)
        elif preset == "Classical":
            self.set_all_sliders_to(0)
            self.frequency_sliders["125 Hz"].set(6)
            self.frequency_sliders["500 Hz"].set(3)
            self.frequency_sliders["2 kHz"].set(-3)
        elif preset == "Bass Boost":
            self.set_all_sliders_to(3)
            self.frequency_sliders["31 Hz"].set(6)
            self.frequency_sliders["62 Hz"].set(6)
            self.frequency_sliders["125 Hz"].set(3)
            self.frequency_sliders["250 Hz"].set(3)
        elif preset == "Treble Boost":
            self.set_all_sliders_to(3)
            self.frequency_sliders["4 kHz"].set(3)
            self.frequency_sliders["8 kHz"].set(6)
            self.frequency_sliders["16 kHz"].set(6)

        self.update_audio()
    
    # Метод для встановлення всіх повзунків на вказане значення
    def set_all_sliders_to(self, value):
        # Встановлення всіх повзунків на вказане значення
        for slider in self.frequency_sliders.values():
            slider.set(value)
    
    # Метод для застосування фільтрів аудіо
    def apply_equalizer(self, audio, gains):

        if audio is not None:
            sample_rate = sd.query_devices(None, 'input')['default_samplerate']

            audio = AudioSegment(audio.tobytes(), frame_rate=sample_rate, sample_width=audio.dtype.itemsize, channels=1)

            eq_audio = audio

            for freq, gain in zip(self.frequency_sliders.keys(), gains):
                freq_value = int(freq.split()[0])
                eq_audio = eq_audio.low_pass_filter(freq_value)
                if gain != 0:
                    eq_audio += gain
            return eq_audio
        else:
            return None
        
    def save_filtered_audio(self, file_path):
        if self.audio is not None:
            gains = [slider.get() for slider in self.frequency_sliders.values()]
            eq_audio = self.apply_equalizer(self.audio, gains)
            if eq_audio:
                eq_audio.export(file_path, format="wav")
                print(f"Filtered audio saved to {file_path}")
            else:
                print("No audio to save!")
        else:
            print("No audio provided for saving!")

    # Метод оновлення аудіо
    def update_audio(self):
        if self.audio is not None:
            print("Updating audio...")
            gains = [slider.get() for slider in self.frequency_sliders.values()]
            print("Gains:", gains)
            eq_audio = self.apply_equalizer(self.audio, gains)
            print("Equalized audio:", eq_audio)
            if eq_audio:
                print("Playing equalized audio...")
                threading.Thread(target=self.play_audio, args=(eq_audio,)).start()
            else:
                print("No audio to play!")
        else:
            print("No audio provided for equalization!")

    # Метод встановлення аудіо
    def set_audio(self, audio):
        
        self.audio = audio

    


