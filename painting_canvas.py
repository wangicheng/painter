import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class Painter:
    def __init__(self, canvas: tk.Canvas, image: Image = None) -> None:
        if image is None:
            self.image = Image.new('RGB', (480, 480), 'white')
        else:
            self.image = image
        
        self.draw = ImageDraw.Draw(self.image)
        self.canvas = canvas
        self.photo: ImageTk.PhotoImage = None
        self.records: list[Image.Image] = []
        self.record_index = 0
        self.is_saved = False
        self.pen_color = 'black'
        self.pen_width = 2
        self.is_drawing = False

        self.canvas.bind("<Button-1>", self.mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_up)
        self.canvas.bind("<B1-Motion>", self.mouse_move)   

        self.last_x = None
        self.last_y = None
     
        self._record()
        self._update_canvas()

    def mouse_down(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True
        
    def mouse_up(self, event):
        self.is_drawing = False
        self._record()
        self._update_canvas()
        
    def mouse_move(self, event):
        if not self.is_drawing:
            return
        if self.last_x is not None and self.last_y is not None:
            # 在 Canvas 上繪製線條
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.pen_color, width=self.pen_width)
            # 在 PIL Image 上繪製線條
            self.offset = self.pen_width / 2
            self.draw.line([self.last_x-self.offset, self.last_y-self.offset, event.x-self.offset, event.y-self.offset], fill=self.pen_color, width=self.pen_width)
            self.last_x = event.x
            self.last_y = event.y

    def can_undo(self) -> bool:
        return self.record_index > 0
    
    def can_redo(self) -> bool:
        return self.record_index < len(self.records) - 1

    def undo(self):
        if not self.can_undo():
            raise Exception(
                f"Cannot undo. ({self.record_index=}, {len(self.records)=})")
        self.record_index -= 1
        self.image = self.records[self.record_index].copy()
        self.draw = ImageDraw.Draw(self.image)
        self._update_canvas()

    def redo(self):
        if not self.can_redo():
            raise Exception(
                f"Cannot redo. ({self.record_index=}, {len(self.records)=})")
        self.record_index += 1
        self.image = self.records[self.record_index].copy()
        self.draw = ImageDraw.Draw(self.image)
        self._update_canvas()

    def _record(self):
        while self.record_index < len(self.records) - 1:
            self.records.pop()
        self.records.append(self.image.copy())
        self.record_index = len(self.records) - 1

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width

    def _update_canvas(self):
        # 使用 PIL Image 的内容更新 Canvas
        self.canvas.delete(tk.ALL)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        # print(f"_update_canvas. ({self.record_index=}, {len(self.records)=})")
        # print(self.records)
        # self.image.show()
