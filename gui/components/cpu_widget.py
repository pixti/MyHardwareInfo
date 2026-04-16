from tkinter import ttk

class CPUWidget(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="CPU 정보")

        self.model_label = ttk.Label(self, text="모델 : 확인 중...", font=("Arial", 10, "bold"))
        self.model_label.pack(anchor="w", padx=10, pady=(5, 2))

        self.p_core_label = ttk.Label(self, text="물리 코어 수 : -")
        self.p_core_label.pack(anchor="w", padx=10, pady=1)

        self.l_core_label = ttk.Label(self, text="논리 코어 수 : -")
        self.l_core_label.pack(anchor="w", padx=10, pady=1)

        self.cache_label = ttk.Label(self, text="캐시 메모리 : L1(NULL), L2(NULL), L3(NULL)", font=("Arial", 9))
        self.cache_label.pack(anchor="w", padx=10, pady=(2, 5))

        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill="x", padx=10, pady=2)

        self.usage_label = ttk.Label(self.status_frame, text="사용률 : 0%", foreground="blue")
        self.usage_label.pack(side="left")

        self.speed_label = ttk.Label(self.status_frame, text="| 속도 : -", foreground="darkgreen")
        self.speed_label.pack(side="left", padx=5)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(2, 10))

    @staticmethod
    def _format_cache_size(kb_size):
        if kb_size is None or kb_size == 0:
            return "NULL"

        try:
            val = float(kb_size)
            if val >= 1024:
                return f"{val / 1024:.1f} MB"
            return f"{int(val)} KB"
        except (ValueError, TypeError):
            return "NULL"

    def update_view(self, data):
        self.model_label.config(text=f"모델 : {data.model}")
        self.p_core_label.config(text=f"물리 코어 수 : {data.physical_cores}")
        self.l_core_label.config(text=f"논리 코어 수 : {data.logical_cores}")

        l1_str = self._format_cache_size(data.l1_cache)
        l2_str = self._format_cache_size(data.l2_cache)
        l3_str = self._format_cache_size(data.l3_cache)

        self.cache_label.config(text=f"캐시 메모리 : L1({l1_str}), L2({l2_str}), L3({l3_str})")

        self.usage_label.config(text=f"사용률 : {data.usage}%")
        self.speed_label.config(text=f"| 속도 : {data.frequency}")

        try:
            self.progress['value'] = float(data.usage)
        except (ValueError, TypeError, KeyError):
            self.progress['value'] = 0