import os
import subprocess
from pathlib import Path

# --- КОНФІГУРАЦІЯ ---
# Визначаємо шлях до кореневої папки проекту
BASE_DIR = Path(__file__).resolve().parent

def run_module(description, command, working_dir=None):
    """Універсальна функція для запуску етапів конвеєра"""
    print(f"\n{description}")
    try:
        # Виконуємо команду у вказаній директорії
        subprocess.run(command, cwd=working_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка у модулі: {e}")
    except Exception as e:
        print(f"⚠️ Критична помилка: {e}")

# =====================================================
# ЗАПУСК КОНВЕЄРА (Pipeline)
# =====================================================

# ... (тут твої кроки 1-4: обробка відео, вилучення координат тощо) ...

# 6. ВЕРИФІКАЦІЯ ТА ТОЧНІСТЬ
# Ми запускаємо це ПЕРЕД дашбордом, бо Streamlit заблокує термінал
run_module(
    "📊 КРОК 6: Запуск верифікації точності моделі (Accuracy Check)...",
    ["python", "verify_accuracy.py"],
    working_dir=BASE_DIR
)

# 5. RAG + ДАШБОРД
# Це фінальний етап, який запускає веб-інтерфейс
print("\n🚀 КРОК 5: Запуск інтерактивного аналітичного дашборду...")
try:
    # Шлях до файлу дашборду
    app_path = BASE_DIR / "src" / "rag" / "app.py"
    # Запускаємо streamlit. Він буде працювати, поки ти не натиснеш Ctrl+C
    subprocess.run(["streamlit", "run", str(app_path)])
except KeyboardInterrupt:
    print("\n👋 Аналіз завершено. Сервер зупинено.")

print(f"\n✅ ВСІ МОДУЛІ ОБРОБЛЕНО! Перевір папку {BASE_DIR}/outputs/")