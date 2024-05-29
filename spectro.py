import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import librosa.display
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AudioAnalyzer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.audio_file = None
        self.fig, self.ax = plt.subplots()
        
        # Створення віджету для відображення графіку
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_canvas.get_tk_widget().pack()

    # Метод для аналізу аудіо
    def analyze_audio(self):
        self.ax.clear()
        audio_data, sample_rate = librosa.load(self.audio_file, sr=None)
        spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
        librosa.display.specshow(spectrogram, sr=sample_rate, x_axis='time', y_axis='log', ax=self.ax)
        self.plot_canvas.draw()

    # Метод для початку відтворення аудіо
    def start_audio_thread(self):
        if self.audio_thread is None or not self.audio_thread.is_alive():
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.audio_thread.start()

    # Метод для відтворення аудіо
    def play_audio(self):
        if self.audio_file is not None:
            audio_data, sample_rate = librosa.load(self.audio_file, sr=None)
            sd.play(audio_data, sample_rate)
            sd.wait()


