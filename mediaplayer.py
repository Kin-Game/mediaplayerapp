import tkinter as tk
from tkinter import ttk
from view import ViewTab
from edit_photo import EditPhotoTab
from edit_audio import EditAudioTab
from edit_video import EditVideoTab

class MediaPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        
        # Створення фрейму для розміщення табулятора
        self.tabControlFrame = tk.Frame(root)
        self.tabControlFrame.pack(expand=True, fill=tk.BOTH)

        # Створення вкладок
        self.tabControl = ttk.Notebook(self.tabControlFrame)
        self.view_tab = ViewTab(self.tabControl)
        self.edit_photo_tab = EditPhotoTab(self.tabControl, self)  # Передача посилання на об'єкт MediaPlayerApp
        self.edit_audio_tab = EditAudioTab(self.tabControl, self)
        self.edit_video_tab = EditVideoTab(self.tabControl, self)
        
        # Додавання вкладок до табулятора
        self.tabControl.add(self.view_tab, text="View")
        self.tabControl.add(self.edit_photo_tab.frame, text="Edit Photo")  # Використовуємо frame з вкладки "Edit Photo"
        self.tabControl.add(self.edit_audio_tab, text="Edit Audio")
        self.tabControl.add(self.edit_video_tab, text="Edit Video")
        
        # Відображення табулятора
        self.tabControl.pack(expand=True, fill=tk.BOTH)

def main():
    root = tk.Tk()
    app = MediaPlayerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()