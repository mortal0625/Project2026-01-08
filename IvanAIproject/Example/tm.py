import os
from tf_keras.models import load_model
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Disable scientific notation
np.set_printoptions(suppress=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "../keras_model.h5")
labels_path = os.path.join(script_dir, "../labels.txt")

model = load_model(model_path, compile=False)

try:
    with open(labels_path, "r", encoding="utf-8") as f:
        class_names = f.readlines()
except:
    with open(labels_path, "r") as f:
        class_names = f.readlines()

print("="*40)
print(" 攝像頭來源選擇 / Camera Source ")
print("="*40)
print("1. 使用數字索引 (嘗試自動搜尋)")
print("2. 使用 DroidCam IP 連線 (最穩定)")
choice = input("請選擇 (1 或 2): ").strip()

cap = None
if choice == '2':
    ip = input("請輸入手機畫面的 WiFi IP (例如 192.168.1.105): ").strip()
    port = input("請輸入 Port (預設 4747): ").strip()
    if not port: port = "4747"
    # Append resolution parameters for DroidCam (standard API)
    # /video?640x480 forces lower resolution
    url = f"http://{ip}:{port}/video?640x480"
    print(f"正在連線至 IP 攝像頭: {url}...")
    cap = cv2.VideoCapture(url)
    
    # Set buffer size to 1 to reduce latency (always show latest frame)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
else:
    for idx in range(11):
        print(f"嘗試索引 {idx}...", end="")
        temp_cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if temp_cap.isOpened():
            ret, _ = temp_cap.read()
            if ret:
                print(" 成功！")
                cap = temp_cap
                break
            temp_cap.release()
        print(" 失敗。")

if cap is None or not cap.isOpened():
    print("錯誤: 無法開啟任何攝像頭。請檢查 IP 是否正確或設備是否被佔用。")
    exit()

print("執行成功！按 'q' 退出，按 'n' 切換鏡頭 (僅限索引模式)。")

frame_count = 0
class_name = "Detecting..."
confidence_score = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        print("無法讀取畫面。")
        break
    
    # 每一幀都更新計數 / Increment frame counter
    frame_count += 1

    # 每 5 幀才做一次預測 (大幅提升流暢度) / Predict every 5 frames
    if frame_count % 5 == 0:
        image_resized = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
        normalized_image_array = (image_array / 127.5) - 1

        prediction = model.predict(normalized_image_array, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index].strip()
        confidence_score = prediction[0][index]

    cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im_rgb)
    draw = ImageDraw.Draw(pil_im)
    try:
        font = ImageFont.truetype("msjh.ttc", 32)
    except:
        font = ImageFont.load_default()

    display_text = f"{class_name} ({confidence_score:.2f})"
    draw.text((10, 30), display_text, font=font, fill=(0, 255, 0))
    frame = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    cv2.imshow("Webcam Image", frame)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break
    if key == ord('n') and choice != '2':
        # Simple cycle for index mode
        pass 

cap.release()
cv2.destroyAllWindows()
