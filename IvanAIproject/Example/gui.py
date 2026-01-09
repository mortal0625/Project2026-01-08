import customtkinter as ctk
import cv2
import numpy as np
import os
from PIL import Image
from tf_keras.models import load_model

# 設定外觀模式
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 視窗設定 ---
        self.title("Ivan AI Project - Object Recognition")
        self.geometry("1000x650")
        self.is_running = True
        
        # 定義顏色 (簡約科技風格)
        self.col_bg = "#1A1A1A"        # 背景深灰
        self.col_panel = "#2B2B2B"     # 面板稍亮
        self.col_accent = "#3B8ED0"    # 科技藍
        self.col_text = "#FFFFFF"      # 白字

        self.configure(fg_color=self.col_bg)

        # --- 路徑設定 ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(script_dir, "../keras_model.h5")
        self.labels_path = os.path.join(script_dir, "../labels.txt")

        # --- 載入模型 ---
        print("Loading Model...")
        try:
            self.model = load_model(self.model_path, compile=False)
            print("Model Loaded.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

        # --- 載入標籤 ---
        self.class_names = []
        try:
            with open(self.labels_path, "r", encoding="utf-8") as f:
                self.class_names = f.readlines()
        except Exception as e:
            print(f"Error loading labels: {e}")
            self.class_names = ["Unknown"]

        # --- 攝影機設定 ---
        self.camera_source = 0 # 預設使用本機攝影機
        config_file = os.path.join(script_dir, "camera_config.txt")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        self.camera_source = content
                        print(f"Loaded camera source from config: {self.camera_source}")
            except Exception as e:
                print(f"Error reading config: {e}")
        
        print(f"Connecting to camera...")
        self.cap = cv2.VideoCapture(self.camera_source)
        
        # --- 介面佈局 (Grid) ---
        self.grid_columnconfigure(0, weight=3) # 左側 (相機) 佔比較大
        self.grid_columnconfigure(1, weight=1) # 右側 (資訊)
        self.grid_rowconfigure(0, weight=0)    # 標題
        self.grid_rowconfigure(1, weight=1)    # 內容

        # 1. 標題列
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 5))
        
        self.title_label = ctk.CTkLabel(self.header_frame, 
                                      text="AI 視覺辨識系統", 
                                      font=("Microsoft JhengHei", 24, "bold"), 
                                      text_color=self.col_text)
        self.title_label.pack(side="left")

        # 2. 左側：相機畫面 (模擬觀景窗)
        self.camera_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=10)
        self.camera_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # 這裡用 Label 來顯示影像
        self.camera_display = ctk.CTkLabel(self.camera_frame, text="", corner_radius=0)
        self.camera_display.pack(expand=True, fill="both", padx=2, pady=2)

        # 3. 右側：結果與操作
        self.right_frame = ctk.CTkFrame(self, fg_color=self.col_panel, corner_radius=15)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1) # 結果區
        self.right_frame.grid_rowconfigure(1, weight=0) # 按鈕區

        # 3.1 結果顯示區
        self.result_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.result_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.result_container, text="辨識結果", font=("Microsoft JhengHei", 16), text_color="gray").pack(pady=(20, 5))
        
        self.result_label = ctk.CTkLabel(self.result_container, 
                                       text="等待中...", 
                                       font=("Microsoft JhengHei", 36, "bold"), 
                                       text_color=self.col_accent,
                                       wraplength=200)
        self.result_label.pack(pady=10)
        
        ctk.CTkLabel(self.result_container, text="信心指數", font=("Microsoft JhengHei", 14), text_color="gray").pack(pady=(30, 5))
        
        self.confidence_label = ctk.CTkLabel(self.result_container, 
                                           text="-- %", 
                                           font=("Roboto", 24), 
                                           text_color="white")
        self.confidence_label.pack()

        # 進度條
        self.progress_bar = ctk.CTkProgressBar(self.result_container, height=8, progress_color=self.col_accent)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10, fill="x")

        # 3.2 按鈕區
        self.btn_recognize = ctk.CTkButton(self.right_frame, 
                                           text="開始辨識", 
                                           font=("Microsoft JhengHei", 18, "bold"),
                                           height=50,
                                           corner_radius=8,
                                           fg_color=self.col_accent,
                                           hover_color="#2A6EA0",
                                           command=self.predict_frame)
        self.btn_recognize.grid(row=1, column=0, sticky="ew", padx=20, pady=30)

        # 啟動相機循環
        self.update_camera()

    def update_camera(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            # 轉 RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb = cv2.flip(frame_rgb, 1) # 鏡像
            
            self.current_frame = frame_rgb 

            # 轉成 PIL Image
            img = Image.fromarray(frame_rgb)
            
            # 固定顯示大小，提升效能 (4:3 比例)
            # 不再隨視窗動態計算，避免 lag
            display_w, display_h = 640, 480
            
            ctk_img = ctk.CTkImage(light_image=img, size=(display_w, display_h))
            self.camera_display.configure(image=ctk_img)
        
        # 每 30ms 更新一次 (約 33 FPS)，比 10ms 更省資源
        self.after(30, self.update_camera)

    def predict_frame(self):
        if hasattr(self, 'current_frame') and self.model is not None:
            # 簡單防手抖/UI回饋
            self.btn_recognize.configure(state="disabled", text="分析中...")
            self.update_idletasks()

            # 影像處理
            image_resized = cv2.resize(self.current_frame, (224, 224), interpolation=cv2.INTER_AREA)
            image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
            normalized_image_array = (image_array / 127.5) - 1
            
            # 預測
            prediction = self.model.predict(normalized_image_array, verbose=0)
            index = np.argmax(prediction)
            class_name = self.class_names[index].strip()
            confidence_score = prediction[0][index]
            
            # 去除編號 (如 "0 ClassName" -> "ClassName")
            display_text = class_name
            if " " in display_text:
                display_text = display_text.split(" ", 1)[1]
            
            # 更新介面
            self.result_label.configure(text=display_text)
            self.confidence_label.configure(text=f"{confidence_score*100:.1f}%")
            self.progress_bar.set(confidence_score)
            
            # 恢復按鈕
            self.btn_recognize.configure(state="normal", text="開始辨識")
        else:
            print("No frame or model available")

    def on_closing(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()