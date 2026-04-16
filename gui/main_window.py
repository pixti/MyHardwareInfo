# gui/main_window.py
import tkinter as tk
from tkinter import ttk

# 매니저 클래스들 임포트
from core.managers.cpu_manager import CPUManager
from core.managers.mem_manager import MemoryManager
from core.managers.disk_manager import DiskManager
from core.managers.net_manager import NetManager
from core.managers.gpu_manager import GPUManager

# UI 컴포넌트들 임포트
from gui.components.cpu_widget import CPUWidget
from gui.components.mem_widget import MemoryWidget
from gui.components.disk_widget import DiskWidget
from gui.components.net_widget import NetWidget
from gui.components.gpu_widget import GPUWidget

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My Hardware Info v1.0")
        self.geometry("520x700")  # 창 크기를 적절히 고정
        self.resizable(False, True) # 세로 확장만 허용

        # 1. 매니저 초기화
        self.cpu_mgr = CPUManager()
        self.mem_mgr = MemoryManager()
        self.disk_mgr = DiskManager()
        self.net_mgr = NetManager()
        self.gpu_mgr = GPUManager()

        # 2. 스크롤 가능한 UI 레이아웃 구성
        self._setup_scrollable_ui()

        # 3. 데이터 업데이트 시작
        self.update_data()

    def _setup_scrollable_ui(self):
        """캔버스와 스크롤바를 이용한 스크롤 영역 설정"""
        # 1. 메인 컨테이너 (Canvas + Scrollbar)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # 실제 위젯들이 배치될 내부 프레임
        self.scrollable_frame = ttk.Frame(self.canvas, padding="10")

        # 2. 내부 프레임의 크기가 변할 때마다 캔버스의 스크롤 범위 갱신
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 3. 캔버스 안에 프레임 배치
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 4. 캔버스 너비를 창 너비에 맞춤
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # 5. 마우스 휠 이벤트 바인딩
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # 6. 레이아웃 배치
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # --- 위젯 배치 시작 (이제 self.scrollable_frame에 배치합니다) ---
        self.cpu_widget = CPUWidget(self.scrollable_frame)
        self.cpu_widget.pack(fill="x", pady=5)

        self.mem_widget = MemoryWidget(self.scrollable_frame)
        self.mem_widget.pack(fill="x", pady=5)

        self.disk_widget = DiskWidget(self.scrollable_frame)
        self.disk_widget.pack(fill="x", pady=5)

        self.gpu_widget = GPUWidget(self.scrollable_frame)
        self.gpu_widget.pack(fill="x", pady=5)

        self.net_widget = NetWidget(self.scrollable_frame)
        self.net_widget.pack(fill="x", pady=5) # 탭 높이를 고려해 expand 제거

    def _on_canvas_configure(self, event):
        """창 크기가 변하면 내부 프레임 너비도 같이 조절"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        """마우스 휠 스크롤 지원"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_data(self):
        """데이터 주기적 갱신"""
        try:
            self.cpu_widget.update_view(self.cpu_mgr.get_integrated_data())
            self.mem_widget.update_view(self.mem_mgr.get_integrated_data())
            self.disk_widget.update_view(self.disk_mgr.get_integrated_data())
            self.gpu_widget.update_view(self.gpu_mgr.get_integrated_data())
            self.net_widget.update_view(self.net_mgr.get_integrated_data())
        except Exception as e:
            print(f"Error: {e}")

        self.after(1000, self.update_data)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()