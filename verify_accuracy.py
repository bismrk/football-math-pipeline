import pandas as pd
import numpy as np
from pathlib import Path

def verify():
    REPORT_PATH = Path("outputs/defensive_report.csv")
    
    if not REPORT_PATH.exists():
        print(f"❌ Помилка: Файл {REPORT_PATH} не знайдено. Спочатку запусти генерацію звіту.")
        return

    df = pd.read_csv(REPORT_PATH)
    
    # 1. Знаходимо реальні втрати (Interceptions / Ball Lost)
    real_failures = df[(df['Subtype'] == 'INTERCEPTION') | (df['Type'] == 'BALL LOST')].copy()
    
    if len(real_failures) == 0:
        print("⚠️ У звіті не знайдено подій перехоплення для аналізу.")
        return

    # 2. Перевірка вікна (1 сек назад)
    def check_window_vulnerability(row, full_df):
        current_frame = row['Start Frame']
        # Шукаємо вразливість у вікні 25 кадрів (1 секунда)
        window = full_df[(full_df['Start Frame'] >= current_frame - 25) & 
                         (full_df['Start Frame'] <= current_frame)]
        
        return window['Defensive_Vulnerability'].any()

    # Проводимо розрахунок
    real_failures['Detected'] = real_failures.apply(lambda r: check_window_vulnerability(r, df), axis=1)
    
    accuracy = (real_failures['Detected'].sum() / len(real_failures)) * 100
    avg_score_at_loss = real_failures['Vision_Score'].mean()

    # 3. КРАСИВИЙ ВИВІД В ТЕРМІНАЛ
    print("\n" + "="*50)
    print("📊 ЗВІТ ПРО ВЕРИФІКАЦІЮ МОДЕЛІ (ОКЛЮЗІЇ)")
    print("="*50)
    print(f"✅ Всього проаналізовано втрат:    {len(real_failures)}")
    print(f"🎯 Модель передбачила (Detected): {real_failures['Detected'].sum()}")
    print(f"📉 Сер. Vision Score при втраті: {avg_score_at_loss:.2f}")
    print("-" * 50)
    print(f"🚀 ЗАГАЛЬНА ТОЧНІСТЬ:           {accuracy:.2f}%")
    print("="*50 + "\n")

    # Порада для диплома:
    if accuracy > 75:
        print("💡 Модель демонструє високу кореляцію з реальними помилками.")
    else:
        print("💡 Рекомендується відкалібрувати поріг вразливості в vision.py.")

# ЦЕЙ БЛОК ОБОВ'ЯЗКОВИЙ ДЛЯ ЗАПУСКУ ЧЕРЕЗ MAIN.PY
if __name__ == "__main__":
    verify()