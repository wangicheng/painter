import os
from enum import Enum

import tkinter as tk
from tkinter import ttk, Menu, PhotoImage, colorchooser

from file_manager import FileManager
from painting_canvas import Painter

import config


class PaintingMode(Enum):
    SELECT = 0
    PENCIL = 1
    ERASER = 2

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(config.WINDOW_SIZE)
        self.paint_size = 1
        self.painting_mode = PaintingMode.PENCIL
        self.file_manager = FileManager()
        self.painter: Painter = None
        
        self._update_title()
        self._set_icon(config.ICON_PATH)
        self._set_menu()
        self._set_painting_toolbar()
        self._set_canvas()
        self._set_footer()

    def _update_title(self):
        """Set the title"""
        title = '未命名'
        if self.file_manager.file_path is not None:
            title = os.path.basename(self.file_manager.file_path)
        title += ' - ' + config.WINDOW_TITLE
        self.title(title)

    def _set_icon(self, icon_file: str):
        """Set the icon"""
        self.iconphoto(False, PhotoImage(file=icon_file))

    def _set_menu(self):
        """Set the menu"""
        self.menu_bar = Menu(self)
        # 添加 "File" 菜單
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self._tools_new)
        file_menu.add_command(label="Open", command=self._tools_open)
        file_menu.add_command(label="Save", command=self._tools_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # 添加 "Edit" 菜單
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self._tools_undo)
        edit_menu.add_command(label="Redo", command=self._tools_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: print("Cut"))
        edit_menu.add_command(label="Copy", command=lambda: print("Copy"))
        edit_menu.add_command(label="Paste", command=lambda: print("Paste"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=self.menu_bar)

    def _set_painting_toolbar(self):
        """Set the painting toolbar"""
        self.painting_toolbar = tk.Frame(self, background='#f5f6f7')
        self.painting_toolbar.pack(side="top", fill="x")
        
        self.color_button = tk.Button(self.painting_toolbar, text="Choose Color", command=self._choose_color)
        self.color_button.grid(column=0, row=0)

    def _set_canvas(self):
        """Set the canvas"""
        self.canvas_frame = tk.Frame(self, background=config.WINDOW_BG_COLOR)
        self.canvas_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, highlightthickness=0, border=0
        )
        self.canvas.place(x=5, y=5)

        self.painter = Painter(self.canvas)

    def _set_footer(self):
        """Set the footer"""
        self.footer = tk.Frame(self, bg='#f0f0f0', height=30)
        self.footer.pack(side="bottom", fill="x")

        # 在 foot bar 中添加一些按钮或标签
        status_label = tk.Label(self.footer, text="Status: Ready")
        status_label.pack(side="left", padx=10)

        self._set_scale_tool()

    def _set_scale_tool(self):
        """Set the scale tool"""
        self.scale_tool = tk.Frame(self.footer)
        self.scale_tool.pack(side='right')

        self.current_scale_index = config.SCALE_SIZE_DEFAULE_INDEX

        # 創建一個字符串變數來顯示百分比
        percentage = tk.StringVar(value="100%")
        
        self.percentage_label = tk.Label(self.scale_tool, textvariable=percentage)
        self.percentage_label.grid(column=0, row=0)

        def update_label(value):
            self.current_scale_index = int(value)
            self.paint_size = config.SCALE_SIZES[int(value)]
            percentage.set(f"{self.paint_size * 100}%")

        # 創建一個水平滑動條
        self.scale = tk.Scale(self.scale_tool, from_=0, to=len(config.SCALE_SIZES) - 1, orient='horizontal', command=update_label, showvalue=False)
        self.scale.set(config.SCALE_SIZE_DEFAULE_INDEX)
        self.scale.grid(column=2, row=0)

        # 創建一個增加按鈕
        def increment():
            if self.current_scale_index < len(config.SCALE_SIZES) - 1:
                self.current_scale_index += 1
                self.scale.set(self.current_scale_index)
                update_label(self.current_scale_index)

        plus_button = ttk.Button(self.scale_tool, text="+", command=increment, width=2)
        plus_button.grid(column=3, row=0)

        # 創建一個減少按鈕
        def decrement():
            if self.current_scale_index > 0:
                self.current_scale_index -= 1
                self.scale.set(self.current_scale_index)
                update_label(self.current_scale_index)

        minus_button = ttk.Button(self.scale_tool, text="-", command=decrement, width=2)
        minus_button.grid(column=1, row=0)

    def _choose_color(self):
        color = colorchooser.askcolor()
        if color[1] is not None:
            self.painter.set_pen_color(color[1])
    
    def _tools_new(self):
        self.file_manager.file_path = None
        self.painter = Painter(self.canvas)
        self._update_title()
    
    def _tools_open(self):
        image = self.file_manager.open()
        self.painter = Painter(self.canvas, image)
        self._update_title()
    
    def _tools_save(self):
        self.file_manager.save(self.painter.image)
        self._update_title()
    
    def _tools_undo(self):
        self.painter.undo()
    
    def _tools_redo(self):
        self.painter.redo()

if __name__ == "__main__":
    # 創建主窗口
    root = MainWindow()

    # 主循環
    root.mainloop()