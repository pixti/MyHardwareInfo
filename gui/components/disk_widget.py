from tkinter import ttk
from utils.converter import format_smart_size
from utils.gui_helper import set_colored_text
import psutil

class DiskWidget(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="디스크 정보")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.tabs = {}
        try:
            self.last_io = psutil.disk_io_counters()
        except:
            self.last_io = None

    def _create_tab(self, mount_point):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f" 드라이브 ({mount_point}) ")

        lbl_total = ttk.Label(frame, text="전체 용량 : -", font=("Arial", 10, "bold"))
        lbl_total.pack(anchor="w", padx=10, pady=(10, 2))

        used_frame = ttk.Label(frame)
        used_frame.pack(anchor="w", padx=10, pady=1)

        free_frame = ttk.Label(frame)
        free_frame.pack(anchor="w", padx=10, pady=1)

        lbl_speed = ttk.Label(frame, text="읽기: 0 B/s | 쓰기: 0 B/s", foreground="green")
        lbl_speed.pack(anchor="w", padx=10, pady=(5, 5))

        progress = ttk.Progressbar(frame, orient="horizontal", length=280, mode="determinate")
        progress.pack(fill="x", padx=10, pady=5)

        self.tabs[mount_point] = {
            "total": lbl_total,
            "used_frame": used_frame,
            "free_frame": free_frame,
            "speed": lbl_speed, "progress": progress
        }

    def update_view(self, _):
        try:
            current_io = psutil.disk_io_counters()
            if self.last_io and current_io:
                read_delta = current_io.read_bytes - self.last_io.read_bytes
                write_delta = current_io.write_bytes - self.last_io.write_bytes
                self.last_io = current_io
            else:
                read_delta, write_delta = 0, 0
                self.last_io = current_io
        except:
            read_delta, write_delta = 0, 0
        try:
            partitions = psutil.disk_partitions()
        except:
            return

        for p in partitions:
            m = p.mountpoint
            if 'cdrom' in p.opts or not m: continue

            try:
                usage = psutil.disk_usage(m)
                if m not in self.tabs:
                    self._create_tab(m)

                tab = self.tabs[m]
                used_p = usage.percent
                free_p = 100.0 - used_p

                tab["total"].config(text=f"전체 용량 : {format_smart_size(usage.total)}")

                used_black = f"사용 중 용량 : {format_smart_size(usage.used)} ["
                used_blue = f"{used_p}%"
                tab["used_frame"] = set_colored_text(tab["used_frame"], used_black, used_blue)

                free_black = f"남은 용량 : {format_smart_size(usage.free)} ["
                free_blue = f"{free_p:.1f}%"
                tab["free_frame"] = set_colored_text(tab["free_frame"], free_black, free_blue)

                speed_txt = f"읽기: {format_smart_size(read_delta, True)} | 쓰기: {format_smart_size(write_delta, True)}"
                tab["speed"].config(text=speed_txt)

                tab["progress"]['value'] = used_p
            except:
                continue