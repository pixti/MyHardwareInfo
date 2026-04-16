from tkinter import ttk
from utils.converter import format_smart_size
import psutil

class NetWidget(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="네트워크 정보")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.tabs = {}

        try:
            self.last_io = psutil.net_io_counters(pernic=True)
        except (RuntimeError, PermissionError):
            self.last_io = {}

    def _create_tab(self, nic_name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=f" {nic_name} ")

        lbl_device = ttk.Label(frame, text="장치 : 확인 중...", font=("Arial", 9), foreground="gray")
        lbl_device.pack(anchor="w", padx=10, pady=(8, 2))

        lbl_type = ttk.Label(frame, text="주소 유형 : -", font=("Arial", 9))
        lbl_type.pack(anchor="w", padx=10, pady=1)

        lbl_ip = ttk.Label(frame, text="IP 주소 : -", font=("Arial", 10, "bold"))
        lbl_ip.pack(anchor="w", padx=10, pady=(1, 5))

        ttk.Separator(frame, orient="horizontal").pack(fill="x", padx=10, pady=5)

        lbl_bytes_sent = ttk.Label(frame, text="보낸 바이트 : -")
        lbl_bytes_sent.pack(anchor="w", padx=10, pady=1)

        lbl_bytes_recv = ttk.Label(frame, text="받은 바이트 : -")
        lbl_bytes_recv.pack(anchor="w", padx=10, pady=1)

        lbl_packets_sent = ttk.Label(frame, text="보낸 패킷 : -")
        lbl_packets_sent.pack(anchor="w", padx=10, pady=1)

        lbl_packets_recv = ttk.Label(frame, text="받은 패킷 : -")
        lbl_packets_recv.pack(anchor="w", padx=10, pady=1)

        lbl_speed = ttk.Label(frame, text="속도 : -", foreground="blue", font=("Arial", 9, "bold"))
        lbl_speed.pack(anchor="w", padx=10, pady=(8, 10))

        self.tabs[nic_name] = {
            "device": lbl_device, "type": lbl_type, "ip": lbl_ip,
            "b_sent": lbl_bytes_sent, "b_recv": lbl_bytes_recv,
            "p_sent": lbl_packets_sent, "p_recv": lbl_packets_recv,
            "speed": lbl_speed
        }

    def update_view(self, data):
        try:
            current_io = psutil.net_io_counters(pernic=True)
        except (RuntimeError, PermissionError):
            return

        for nic_name, nic_data in data.items():
            if nic_name not in self.tabs:
                self._create_tab(nic_name)

            tab = self.tabs[nic_name]

            tab["device"].config(text=f"장치 : {nic_data.get('device_name', '알 수 없음')}")
            tab["type"].config(text=f"주소 유형 : {nic_data.get('family', 'N/A')}")
            tab["ip"].config(text=f"IP 주소 : {nic_data.get('ip', 'N/A')}")

            b_sent = nic_data.get('bytes_sent', 0)
            b_recv = nic_data.get('bytes_recv', 0)

            tab["b_sent"].config(
                text=f"보낸 바이트 : {b_sent:,} Byte ({format_smart_size(b_sent)})"
            )
            tab["b_recv"].config(
                text=f"받은 바이트 : {b_recv:,} Byte ({format_smart_size(b_recv)})"
            )

            p_sent_count = nic_data.get('packets_sent', 0)
            p_recv_count = nic_data.get('packets_recv', 0)

            tab["p_sent"].config(
                text=f"보낸 패킷 : {format_smart_size(p_sent_count)} ({p_sent_count:,} 개)"
            )
            tab["p_recv"].config(
                text=f"받은 패킷 : {format_smart_size(p_recv_count)} ({p_recv_count:,} 개)"
            )

            if nic_name in self.last_io and nic_name in current_io:
                up_speed = current_io[nic_name].bytes_sent - self.last_io[nic_name].bytes_sent
                down_speed = current_io[nic_name].bytes_recv - self.last_io[nic_name].bytes_recv
                tab["speed"].config(text=f"업로드: {format_smart_size(up_speed, True)} | 다운로드: {format_smart_size(down_speed, True)}")

        self.last_io = current_io