import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import json
import vlc
import os

class MusicManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Ініціалізація змінних для управління музикою
        self.music_library = []
        self.playlists = {}
        self.current_playlist = None
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.create_widgets()
        self.load_library()

    def create_widgets(self):
        # Створення або вибір плейлиста
        self.playlist_label = ttk.Label(self, text="Playlist:")
        self.playlist_label.grid(row=0, column=0, pady=5)

        self.playlist_combobox = ttk.Combobox(self)
        self.playlist_combobox.grid(row=0, column=1, pady=5)
        self.playlist_combobox.bind("<<ComboboxSelected>>", self.select_playlist)

        self.create_playlist_button = ttk.Button(self, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.grid(row=0, column=2, pady=5)

        self.load_playlist_button = ttk.Button(self, text="Load Playlist", command=self.load_playlist)
        self.load_playlist_button.grid(row=0, column=3, pady=5)

        # Додавання треків до плейлиста
        self.add_track_button = ttk.Button(self, text="Add Track", command=self.add_track)
        self.add_track_button.grid(row=1, column=0, pady=5)

        # Поле з колонками та скролбаром
        self.track_tree = ttk.Treeview(self, columns=("Genre", "Artist", "Title"), show='headings')
        self.track_tree.heading("Genre", text="Genre")
        self.track_tree.heading("Artist", text="Artist")
        self.track_tree.heading("Title", text="Title")
        self.track_tree.grid(row=2, column=0, columnspan=4, pady=5, sticky="nsew")
        
        self.track_tree.bind("<Double-1>", self.play_track)  # Double click to play track

        # Скролбар
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.track_tree.yview)
        self.track_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky="ns")

        # Елементи управління відтворенням
        self.play_button = ttk.Button(self, text="Play", command=self.play_track)
        self.play_button.grid(row=3, column=0, pady=5)

        self.pause_button = ttk.Button(self, text="Pause", command=self.pause_track)
        self.pause_button.grid(row=3, column=1, pady=5)

        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_track)
        self.stop_button.grid(row=3, column=2, pady=5)

        # Управління треками в плейлисті
        self.move_up_button = ttk.Button(self, text="Move Up", command=self.move_track_up)
        self.move_up_button.grid(row=4, column=0, pady=5)

        self.move_down_button = ttk.Button(self, text="Move Down", command=self.move_track_down)
        self.move_down_button.grid(row=4, column=1, pady=5)

        self.remove_track_button = ttk.Button(self, text="Remove Track", command=self.remove_track)
        self.remove_track_button.grid(row=4, column=2, pady=5)

        # Сортування треків
        self.sort_by_label = ttk.Label(self, text="Sort by:")
        self.sort_by_label.grid(row=5, column=0, pady=5)

        self.sort_by_combobox = ttk.Combobox(self, values=["Genre", "Artist"])
        self.sort_by_combobox.grid(row=5, column=1, pady=5)
        self.sort_by_combobox.bind("<<ComboboxSelected>>", self.sort_tracks)

        # Збереження та завантаження бібліотеки
        self.save_library_button = ttk.Button(self, text="Save Library", command=self.save_library)
        self.save_library_button.grid(row=6, column=0, pady=5)

        self.load_library_button = ttk.Button(self, text="Load Library", command=self.load_library)
        self.load_library_button.grid(row=6, column=1, pady=5)

    # Метод створення нового плейлисту
    def create_playlist(self):
        playlist_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if playlist_name:
            self.playlists[playlist_name] = []
            self.current_playlist = playlist_name
            self.playlist_combobox['values'] = list(self.playlists.keys())
            self.playlist_combobox.set(playlist_name)
            self.track_tree.delete(*self.track_tree.get_children())
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully.")
    # Метод завантаження плейлисту
    def load_playlist(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                self.playlists[file_path] = json.load(file)
            self.playlist_combobox['values'] = list(self.playlists.keys())
            self.current_playlist = file_path
            self.playlist_combobox.set(file_path)
            self.track_tree.delete(*self.track_tree.get_children())
            for track in self.playlists[self.current_playlist]:
                self.track_tree.insert("", tk.END, values=(track['genre'], track['artist'], track['title']))
            messagebox.showinfo("Success", f"Playlist '{file_path}' loaded successfully.")
    # Метод вибору плейлисту з комбобоксу
    def select_playlist(self, event):
        self.current_playlist = self.playlist_combobox.get()
        self.track_tree.delete(*self.track_tree.get_children())
        for track in self.playlists[self.current_playlist]:
            self.track_tree.insert("", tk.END, values=(track['genre'], track['artist'], track['title']))
    
    # Метод додавання треку до плейлисту
    def add_track(self):
        if not self.current_playlist:
            messagebox.showerror("Error", "Please create or select a playlist first.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        if file_path:
            artist = simpledialog.askstring("Artist", "Enter artist name:")
            title = simpledialog.askstring("Title", "Enter track title:")
            genre = simpledialog.askstring("Genre", "Enter genre:")
            if artist and title and genre:
                track_info = {"artist": artist, "title": title, "genre": genre, "file_path": file_path}
                self.playlists[self.current_playlist].append(track_info)
                self.track_tree.insert("", tk.END, values=(genre, artist, title))
                messagebox.showinfo("Success", "Track added successfully.")
            else:
                messagebox.showerror("Input Error", "Please provide artist, title, and genre.")
    
    # Метод відтворення треку
    def play_track(self, event=None):
        selected_item = self.track_tree.selection()
        if selected_item:
            selected_track_index = self.track_tree.index(selected_item[0])
            selected_track = self.playlists[self.current_playlist][selected_track_index]
            media = self.instance.media_new(selected_track['file_path'])
            self.player.set_media(media)
            self.player.play()
        else:
            messagebox.showerror("Selection Error", "Please select a track to play.")
    
    # Метод паузи
    def pause_track(self):
        self.player.pause()

    # Метод зупинки відтворення
    def stop_track(self):
        self.player.stop()

    # Метод переміщення треку вище
    def move_track_up(self):
        selected_item = self.track_tree.selection()
        if selected_item:
            index = self.track_tree.index(selected_item[0])
            if index > 0:
                self.playlists[self.current_playlist].insert(index-1, self.playlists[self.current_playlist].pop(index))
                self.update_track_tree()
                self.track_tree.selection_set(self.track_tree.get_children()[index-1])

    # Метод переміщення треку нижче
    def move_track_down(self):
        selected_item = self.track_tree.selection()
        if selected_item:
            index = self.track_tree.index(selected_item[0])
            if index < len(self.playlists[self.current_playlist]) - 1:
                self.playlists[self.current_playlist].insert(index+1, self.playlists[self.current_playlist].pop(index))
                self.update_track_tree()
                self.track_tree.selection_set(self.track_tree.get_children()[index+1])
    
    # Метод видалення треку з плейлисту
    def remove_track(self):
        selected_item = self.track_tree.selection()
        if selected_item:
            index = self.track_tree.index(selected_item[0])
            del self.playlists[self.current_playlist][index]
            self.update_track_tree()
    
    # Метод сортування треків
    def sort_tracks(self, event):
        sort_by = self.sort_by_combobox.get().lower()
        self.playlists[self.current_playlist].sort(key=lambda x: x[sort_by])
        self.update_track_tree()

    # Метод оновлення відображення дерева треків
    def update_track_tree(self):
        self.track_tree.delete(*self.track_tree.get_children())
        for track in self.playlists[self.current_playlist]:
            self.track_tree.insert("", tk.END, values=(track['genre'], track['artist'], track['title']))

    # Метод збереження бібліотеки музики
    def save_library(self, show_message=True):
        for playlist_name, tracks in self.playlists.items():
            with open(playlist_name, "w") as file:
                json.dump(tracks, file)
        if show_message:
            messagebox.showinfo("Success", "Library and playlists saved successfully.")
    
    # Метод завантаження бібліотеки музики
    def load_library(self):
        if os.path.exists("music_library.json"):
            with open("music_library.json", "r") as file:
                data = json.load(file)
            self.music_library = data.get("music_library", [])
            self.playlists = data.get("playlists", {})
            self.playlist_combobox['values'] = list(self.playlists.keys())
            self.current_playlist = None
            self.track_tree.delete(*self.track_tree.get_children())
            messagebox.showinfo("Success", "Library loaded successfully.")
    
    # Метод обробки події закриття вікна
    def on_close(self):
        self.save_library(show_message=False)
        self.parent.destroy()
