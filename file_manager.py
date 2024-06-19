from PIL import Image
from tkinter import filedialog

class FileManager:
    def __init__(self, file_path: str = None):
        self.file_path = file_path

    def save(self, image: Image.Image):
        # 選擇要儲存的檔案位置
        if self.file_path is None:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if self.file_path is not None:
            image.save(self.file_path)

    def open(self) -> Image.Image:
        # 選擇要開啟的檔案位置
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if self.file_path is None:
            return None
        image = Image.open(self.file_path)
        return image