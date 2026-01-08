import os
import tkinter as tk
from tkinter import font
import cv2
import random
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import numpy as np

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model

class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#808080')

        # --- Load Assets ---
        self.model = load_model("keras_Model.h5", compile=False)
        with open("labels.txt", "r", encoding="utf-8") as f:
            self.class_names = [line.strip() for line in f.readlines()]
        
        self.font_path = "C:/Windows/Fonts/msjh.ttc"
        self.ui_font = font.Font(family="Microsoft JhengHei", size=12)
        self.result_font = font.Font(family="Microsoft JhengHei", size=20, weight="bold")
        self.pil_font = ImageFont.truetype(self.font_path, 24)

        # Map labels to image paths
        self.image_paths = {
            "石頭": "Stone.png",
            "布": "Cloth.png",
            "剪刀": "scissors.png"
        }
        self.choices = list(self.image_paths.keys())
        
        # Load images and resize them
        self.choice_images = {name: self.load_and_resize_image(path, (150, 150)) for name, path in self.image_paths.items()}
        self.choice_images["default"] = self.create_default_image((150, 150), "等待出拳")

        # --- Game State ---
        self.player_move = None
        self.player_move_name = "N/A"

        # --- UI Setup ---
        # 1. Camera Feed (玩家出拳顯示區)
        tk.Label(root, text="玩家出拳顯示區", font=self.ui_font, bg='#FFFFFF').place(x=50, y=20)
        self.camera_label = tk.Label(root, bg='black')
        self.camera_label.place(x=50, y=50, width=480, height=360)

        # 2. Player's Detected Move (出拳判斷顯示)
        self.player_move_label = tk.Label(root, image=self.choice_images["default"], bg='#FFA500')
        self.player_move_label.place(x=150, y=430, width=180, height=150)
        tk.Label(root, text="出拳判斷顯示", font=self.ui_font, bg='#FFA500').place(x=190, y=580)


        # 3. Computer's Move (電腦出拳區)
        self.computer_move_label = tk.Label(root, image=self.choice_images["default"], bg='#ADD8E6')
        self.computer_move_label.place(x=580, y=50, width=180, height=150)
        tk.Label(root, text="電腦出拳區", font=self.ui_font, bg='#ADD8E6').place(x=620, y=200)

        # 4. Result Display (顯示勝負)
        self.result_label = tk.Label(root, text="顯示勝負", font=self.result_font, bg='#90EE90', width=12)
        self.result_label.place(x=580, y=280)

        # 5. Start Button (開始猜拳)
        self.start_button = tk.Button(root, text="開始猜拳", font=self.ui_font, bg='#8B0000', fg='white', command=self.play_game)
        self.start_button.place(x=580, y=350, width=180, height=50)
        
        # --- Initialize Camera ---
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def load_and_resize_image(self, path, size):
        try:
            img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            return self.create_default_image(size, f"找不到\n{os.path.basename(path)}")

    def create_default_image(self, size, text):
        img = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(img)
        text_bbox = draw.textbbox((0,0), text, font=self.pil_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        draw.text(((size[0]-text_width)/2, (size[1]-text_height)/2), text, fill='black', font=self.pil_font)
        return ImageTk.PhotoImage(img)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)

            # --- Prediction ---
            image_for_pred = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            size = (224, 224)
            image_for_pred = ImageOps.fit(image_for_pred, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image_for_pred)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array
            
            prediction = self.model.predict(data, verbose=0)
            index = np.argmax(prediction)
            
            # Get the class name, removing the index part e.g., "1 石頭" -> "石頭"
            current_move_name = ' '.join(self.class_names[index].split(' ')[1:])

            if current_move_name in self.choices:
                self.player_move = current_move_name
                self.player_move_label.config(image=self.choice_images[self.player_move])
            else:
                 self.player_move = None # It's 'nano' or something else
                 self.player_move_label.config(image=self.choice_images["default"])


            # --- Display Camera Feed ---
            img = cv2.resize(frame, (480, 360))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            
            self.camera_label.imgtk = img_tk
            self.camera_label.config(image=img_tk)

        self.root.after(10, self.update_frame)

    def play_game(self):
        if not self.player_move:
            self.result_label.config(text="未偵測到手勢")
            return
        
        # Lock in player's move and disable button
        self.locked_player_move = self.player_move
        self.start_button.config(state=tk.DISABLED)
        
        # Start countdown
        self.countdown(3)

    def countdown(self, count):
        if count > 0:
            self.result_label.config(text=str(count))
            self.root.after(1000, self.countdown, count - 1)
        else:
            self.show_result()

    def show_result(self):
        # Computer's move
        computer_choice = random.choice(self.choices)
        self.computer_move_label.config(image=self.choice_images[computer_choice])

        # Determine winner
        player = self.locked_player_move
        computer = computer_choice

        if player == computer:
            result = "平手！"
        elif (player == "石頭" and computer == "剪刀") or \
             (player == "剪刀" and computer == "布") or \
             (player == "布" and computer == "石頭"):
            result = "你贏了！"
        else:
            result = "你輸了！"
            
        self.result_label.config(text=result)
        
        # Re-enable button after a short delay
        self.root.after(2000, lambda: self.start_button.config(state=tk.NORMAL))

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
