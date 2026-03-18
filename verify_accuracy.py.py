import pandas as pd
import numpy as np

# Завантажуємо твій згенерований звіт
df = pd.read_csv("outputs/defensive_report.csv")

print("🧪 ЗАПУСК ВЕРИФІКАЦІЇ МОДЕЛІ...")

# 1. Знаходимо всі реальні перехоплення (Interceptions)
# У файлах Metrica це Subtype 'INTERCEPTION' або Type 'BALL LOST'
real_failures = df[(df['Subtype'] == 'INTERCEPTION') | (df['Type'] == 'BALL LOST')]

if len(real_failures) > 0:
    # 2. Перевіряємо, скільки з цих втрат модель позначила як "Вразливість"
    # Тобто Vision Score був низьким у цей момент
    predicted_failures = real_failures[real_failures['Defensive_Vulnerability'] == True]
    
    accuracy = (len(predicted_failures) / len(real_failures)) * 100
    
    print(f"✅ Всього реальних перехоплень у матчі: {len(real_failures)}")
    print(f"🔍 Модель заздалегідь визначила вразливість у {len(predicted_failures)} з них.")
    print(f"🎯 ТОЧНІСТЬ МОДЕЛІ: {accuracy:.2f}%")
    
    if accuracy > 70:
        print("📈 Висновок: Модель має високу прогностичну здатність.")
else:
    print("⚠️ У даному уривку матчу не знайдено подій 'INTERCEPTION' для порівняння.")