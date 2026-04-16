from tkinter import ttk

class GPUWidget(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="그래픽 카드(GPU) 정보")
        self.container = ttk.Frame(self)
        self.container.pack(fill="x", padx=10, pady=5)

    def update_view(self, data_list):
        for child in self.container.winfo_children():
            child.destroy()

        if not data_list:
            ttk.Label(self.container, text="GPU 정보를 찾을 수 없습니다.").pack()
            return

        for gpu in data_list:
            # 모델명
            lbl_model = ttk.Label(self.container, text=f"모델 : {gpu.model}", font=("Arial", 9, "bold"))
            lbl_model.pack(anchor="w", pady=(5, 0))

            # 드라이버 버전
            lbl_drv = ttk.Label(self.container, text=f"드라이버 버전 : {gpu.driver_version}", foreground="gray", font=("Arial", 8))
            lbl_drv.pack(anchor="w", pady=(0, 5))

            ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=5)