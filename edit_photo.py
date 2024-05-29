import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter


class EditPhotoTab(tk.Frame):
    def __init__(self, parent, media_player_app):
        super().__init__(parent)
        self.parent = parent
        self.media_player_app = media_player_app

        # Фрейм для вкладки "Edit Photo"
        self.frame = ttk.Frame(parent)

        # Кнопка вибору фото
        self.choose_photo_button = ttk.Button(self.frame, text="Choose Photo", command=self.choose_photo)
        self.choose_photo_button.pack(pady=10)

        # Перегляд фото
        self.photo_label = ttk.Label(self.frame, text="Selected Photo:")
        self.photo_label.pack()

        # Фрейм для відображення фото
        self.image_frame = ttk.Frame(self.frame)
        self.image_frame.pack()

        # Функціонал для відображення фото
        self.photo_canvas = tk.Canvas(self.image_frame)
        self.photo_canvas.pack()

        # Повзунки для редагування параметрів

        # Яскравість
        self.brightness_label = ttk.Label(self.frame, text="Brightness:")
        self.brightness_label.pack()
        self.brightness_scale = ttk.Scale(self.frame, from_=0, to=2, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_scale.set(1)  
        self.brightness_scale.pack()
        # Контрастінсть
        self.contrast_label = ttk.Label(self.frame, text="Contrast:")
        self.contrast_label.pack()
        self.contrast_scale = ttk.Scale(self.frame, from_=0, to=2, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_scale.set(1) 
        self.contrast_scale.pack()
        # Насиченість
        self.saturation_label = ttk.Label(self.frame, text="Saturation:")
        self.saturation_label.pack()
        self.saturation_scale = ttk.Scale(self.frame, from_=0, to=2, orient=tk.HORIZONTAL, command=self.update_saturation)
        self.saturation_scale.set(1)  
        self.saturation_scale.pack()
        # Розмиття
        self.blur_label = ttk.Label(self.frame, text="Blur:")
        self.blur_label.pack()
        self.blur_scale = ttk.Scale(self.frame, from_=0, to=10, orient=tk.HORIZONTAL, command=self.update_blur)
        self.blur_scale.set(0)  
        self.blur_scale.pack()

        # Збережені параметри фільтрів
        self.filter_parameters = {
            'brightness': 1,
            'contrast': 1,
            'saturation': 1,
            'blur': 0
        }

        # Кнопка вибору фото для слайдшоу
        self.choose_slideshow_photos_button = ttk.Button(self.frame, text="Choose Slideshow Photos", command=self.choose_slideshow_photos)
        self.choose_slideshow_photos_button.pack(pady=10)

        # Функціонал для слайдшоу
        self.slideshow_photos = []  

        # Кнопка для відтворення слайдшоу
        self.play_slideshow_button = ttk.Button(self.frame, text="Play Slideshow", command=self.play_slideshow)
        self.play_slideshow_button.pack(pady=10)
        # Кнопка для збереження редагованого фото
        self.save_button = ttk.Button(self.frame, text="Save", command=self.save_photo)
        self.save_button.pack(pady=10)

        # Встановлення зв'язку з розмірами вікна
        self.parent.bind("<Configure>", self.on_window_resize)

    # Метод вибору фото
    def choose_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.show_photo(file_path)

    # Метод відображення фото
    def show_photo(self, file_path):
        original_image = Image.open(file_path)
        original_image.thumbnail((800, 800))  
        self.original_image = original_image

        # Відображення зменшеного фото
        photo = ImageTk.PhotoImage(original_image)
        self.photo_canvas.config(width=photo.width(), height=photo.height())
        self.photo_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.photo_canvas.photo = photo

    # Метод для оновлення зображення при зміні розміру вікна
    def on_window_resize(self, event):
        if hasattr(self, 'original_image'):
            resized_image = self.resize_image(self.original_image, (self.parent.winfo_width(), self.parent.winfo_height()))
            self.show_resized_photo(resized_image)

    # Метод зміни розміру зображення
    def resize_image(self, image, new_size):
        return image.resize(new_size, Image.ANTIALIAS)


    # Метод для відображення зміненого за розмірами фото
    def show_resized_photo(self, image):
        photo = ImageTk.PhotoImage(image)
        self.photo_canvas.config(width=photo.width(), height=photo.height())
        self.photo_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.photo_canvas.photo = photo

    # Метод оновлення якравості
    def update_brightness(self, value):
        if hasattr(self, 'original_image'):
            self.filter_parameters['brightness'] = float(value)
            enhanced_image = self.apply_enhancements(self.original_image, **self.filter_parameters)
            self.show_resized_photo(enhanced_image)


    # Функція вибору фотографій для слайдшоу
    def choose_slideshow_photos(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            self.slideshow_photos = [Image.open(file_path) for file_path in file_paths]

    # Функція відтворення слайдшоу
    def play_slideshow(self):
        if self.slideshow_photos:
            for photo in self.slideshow_photos:
                resized_photo = photo.copy()
                resized_photo.thumbnail((800, 800), Image.LANCZOS)
                self.show_resized_photo(resized_photo)
                self.parent.update()  
                self.parent.after(2000)  


    # Метод оновлення контрасту
    def update_contrast(self, value):
        if hasattr(self, 'original_image'):
            self.filter_parameters['contrast'] = float(value)
            enhanced_image = self.apply_enhancements(self.original_image, **self.filter_parameters)
            self.show_resized_photo(enhanced_image)

    # Метод оновлення насиченості
    def update_saturation(self, value):
        if hasattr(self, 'original_image'):
            self.filter_parameters['saturation'] = float(value)
            enhanced_image = self.apply_enhancements(self.original_image, **self.filter_parameters)
            self.show_resized_photo(enhanced_image)

    # Метод оновлення розмиття
    def update_blur(self, value):
        if hasattr(self, 'original_image'):
            self.filter_parameters['blur'] = float(value)
            enhanced_image = self.apply_enhancements(self.original_image, **self.filter_parameters)
            self.show_resized_photo(enhanced_image)

    # Метод застосування фільтрів до зображення
    def apply_enhancements(self, image, brightness=1, contrast=1, saturation=1, blur=0):
        enhanced_image = image.copy()
        enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(brightness)
        enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast)
        enhanced_image = ImageEnhance.Color(enhanced_image).enhance(saturation)
        enhanced_image = enhanced_image.filter(ImageFilter.GaussianBlur(blur))
        return enhanced_image

    # Метод збереження фото
    def save_photo(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            edited_image = self.apply_enhancements(self.original_image, **self.filter_parameters)
            edited_image.save(file_path)