from tkinter import ttk
from utils.gui_helper import set_colored_text

class MemoryWidget(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="메모리 정보")

        self.total_label = ttk.Label(self, text="메모리 용량 : 확인 중...", font=("Arial", 10, "bold"))
        self.total_label.pack(anchor="w", padx=10, pady=(5, 2))

        self.used_frame = ttk.Label(self)
        self.used_frame.pack(anchor="w", padx=10, pady=1)

        self.free_frame = ttk.Label(self)
        self.free_frame.pack(anchor="w", padx=10, pady=1)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(5, 10))

    @staticmethod
    def _format_size(byte_value):
        gb = byte_value / (1024**3)
        mb = byte_value / (1024**2)
        return f"{gb:.2f} GB ({mb:,.0f} MB)"

    def update_view(self, data):
        self.total_label.config(text=f"메모리 용량 : {self._format_size(data.total)}")

        used_str = self._format_size(data.used)
        used_black = f"사용 중 메모리 크기 : {used_str} ["
        used_blue = f"{data.percent}%"
        self.used_frame = set_colored_text(self.used_frame, used_black, used_blue)

        free_percent = 100.0 - data.percent
        free_str = self._format_size(data.free)
        free_black = f"남은 메모리 크기 : {free_str} ["
        free_blue = f"{free_percent:.1f}%"
        self.free_frame = set_colored_text(self.free_frame, free_black, free_blue)

        self.progress['value'] = data.percent