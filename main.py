# main.py — головний скрипт інтеграції (твій внесок)
import subprocess
import os
from pathlib import Path

print("🚀 Запуск інтегрованої математичної системи...")

# 1. PnL калібровка (якщо є відео)
if Path("data/match.mp4").exists():
    print("1️⃣ Запуск PnL-оптимізації...")
    os.chdir("src/pnl")
    subprocess.run([
        "python", "inference.py",
        "--weights_kp", "SV_kp",
        "--weights_line", "SV_lines",
        "--pnl_refine",
        "--input_path", "../../data/match.mp4",
        "--input_type", "video",
        "--save_path", "../../outputs/calibrated_field.json"
    ])
    os.chdir("../..")

# 2. Генерація event data
# print("2️⃣ Генерація подійних даних...")
# run_module(
#     "2️⃣ Генерація подійних даних...",
#     ["python", "generate_event_data.py"],
#     working_dir=BASE_DIR / "src" / "events"
# )

# 3. Vision layer (stochastic FOV)
print("3️⃣ Обчислення візуальної поведінки...")
os.chdir("src/vision")
subprocess.run(["python", "vision_layer.py"])   # якщо notebook — спочатку конвертуй
os.chdir("../..")

# 4. DEFCON + Pressing triggers
print("4️⃣ Оцінка оборонної цінності...")
os.chdir("src/defcon")
subprocess.run(["python", "main.py"])
os.chdir("../triggers")
subprocess.run(["python", "main.py"])
os.chdir("../..")

# 5. RAG + дашборд
print("5️⃣ Генерація scouting-звіту через RAG...")
os.chdir("src/rag")
subprocess.run(["streamlit", "run", "app.py", "--server.headless", "true"])
os.chdir("../..")

print("✅ ВСІ МОДУЛІ ЗАПУЩЕНО! Перевір папку outputs/")
