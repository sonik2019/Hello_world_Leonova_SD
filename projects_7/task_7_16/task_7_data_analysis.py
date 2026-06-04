#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ЗАДАНИЕ 7.16 - ВИЗУАЛИЗАЦИЯ ДАННЫХ
Анализ цен товаров из базы данных student (task_5_7)
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Настройка русского шрифта
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['font.size'] = 10

# ============= ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ =============
DB_CONFIG = {
    "host": "localhost",
    "port": "5435",
    "user": "postgres_task",
    "password": "student",
    "database": "student"
}

print("=" * 70)
print(" " * 15 + "ЗАДАНИЕ 7.16 - ВИЗУАЛИЗАЦИЯ ДАННЫХ")
print("=" * 70)

try:
    connection = psycopg2.connect(**DB_CONFIG)
    print("\n✅ Подключение к базе 'student' установлено")

    # ============= 1. ЗАГРУЗКА ДАННЫХ =============
    
    # 1.1. Средняя цена и количество записей по категориям
    df_categories = pd.read_sql("""
        SELECT 
            p.category,
            ROUND(AVG(pr.price)::numeric, 2) AS avg_price,
            COUNT(pr.id) AS price_count,
            COUNT(DISTINCT p.id) AS product_count
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        GROUP BY p.category
        ORDER BY avg_price DESC
    """, connection)
    
    # 1.2. Топ-10 самых дорогих товаров (по средней цене)
    df_top_products = pd.read_sql("""
        SELECT 
            p.name AS product_name,
            ROUND(AVG(pr.price)::numeric, 2) AS avg_price,
            COUNT(pr.id) AS price_changes
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        GROUP BY p.name
        ORDER BY avg_price DESC
        LIMIT 10
    """, connection)
    
    # 1.3. Все цены для гистограммы распределения
    df_all_prices = pd.read_sql("SELECT price FROM prices", connection)
    
    # 1.4. Количество товаров по категориям (для круговой диаграммы)
    df_category_counts = pd.read_sql("""
        SELECT 
            category,
            COUNT(DISTINCT id) AS product_count
        FROM products
        GROUP BY category
        ORDER BY product_count DESC
    """, connection)
    
    # 1.5. Количество поставщиков по категориям
    df_suppliers_by_category = pd.read_sql("""
        SELECT 
            p.category,
            COUNT(DISTINCT s.id) AS supplier_count,
            COUNT(DISTINCT p.id) AS product_count
        FROM suppliers s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.category
        ORDER BY supplier_count DESC
    """, connection)
    
    # 1.6. Аномалии: товары без поставщиков
    df_no_suppliers = pd.read_sql("""
        SELECT 
            p.name AS product_name,
            p.category
        FROM products p
        LEFT JOIN suppliers s ON p.id = s.product_id
        WHERE s.id IS NULL
        ORDER BY p.category
    """, connection)
    
    print(f"\n📊 Загружено данных:")
    print(f"   • Категорий: {len(df_categories)}")
    print(f"   • Топ-10 товаров: {len(df_top_products)}")
    print(f"   • Всего цен: {len(df_all_prices)}")
    print(f"   • Товаров без поставщиков: {len(df_no_suppliers)}")

except Exception as error:
    print(f"❌ Ошибка подключения: {error}")
    raise SystemExit
finally:
    connection.close()
    print("✅ Соединение закрыто\n")

# ============= 2. РАСЧЁТ СТАТИСТИЧЕСКИХ МЕТРИК =============
all_prices = df_all_prices['price']
stats = {
    'Среднее': all_prices.mean(),
    'Медиана': all_prices.median(),
    'Стандартное отклонение': all_prices.std(),
    'Минимум': all_prices.min(),
    'Максимум': all_prices.max(),
    'Q1 (25-й перцентиль)': all_prices.quantile(0.25),
    'Q3 (75-й перцентиль)': all_prices.quantile(0.75)
}

print("=" * 70)
print("📈 СТАТИСТИЧЕСКИЕ МЕТРИКИ")
print("=" * 70)
for name, val in stats.items():
    print(f"   {name:25s}: {val:12.2f} руб.")

# ============= 3. ПОСТРОЕНИЕ ГРАФИКОВ =============

# Создаём фигуру с 6 подграфиками (3 ряда × 2 колонки)
fig = plt.figure(figsize=(16, 14))
fig.suptitle("Анализ товарной базы данных", fontsize=16, fontweight="bold", y=1.02)

# Используем GridSpec для гибкого размещения графиков
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# ---- График 1: Средняя цена по категориям (горизонтальная столбчатая) ----
ax1 = fig.add_subplot(gs[0, 0])

# Сортируем для наглядности
df_categories_sorted = df_categories.sort_values('avg_price', ascending=True)

colors = ['#ff6b6b' if x < df_categories_sorted['avg_price'].median() else '#4ecdc4' 
          for x in df_categories_sorted['avg_price']]

bars1 = ax1.barh(df_categories_sorted['category'], df_categories_sorted['avg_price'], 
                 color=colors, edgecolor='white', height=0.6)

# Подписи значений
for bar, val in zip(bars1, df_categories_sorted['avg_price']):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
             f'{val:.0f} руб.', va='center', fontsize=9)

ax1.axvline(stats['Медиана'], color='darkorange', linestyle='--', linewidth=1.5,
            label=f"Медиана всех цен: {stats['Медиана']:.0f} руб.")
ax1.set_xlabel('Средняя цена (руб.)')
ax1.set_title('📊 Средняя цена по категориям товаров', fontweight='bold', pad=10)
ax1.legend(fontsize=8)

# ---- График 2: Топ-10 дорогих товаров (вертикальная столбчатая) ----
ax2 = fig.add_subplot(gs[0, 1])

# Сокращаем длинные названия
short_names = [name[:20] + '...' if len(name) > 20 else name 
               for name in df_top_products['product_name']]

bars2 = ax2.bar(short_names, df_top_products['avg_price'], 
                color='#ffa500', edgecolor='white', width=0.6)

# Подписи значений
for bar, val in zip(bars2, df_top_products['avg_price']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'{val:.0f}', ha='center', fontsize=8, rotation=0)

ax2.set_ylabel('Средняя цена (руб.)')
ax2.set_title('💰 Топ-10 самых дорогих товаров', fontweight='bold', pad=10)
ax2.set_xticklabels(short_names, rotation=45, ha='right', fontsize=8)

# ---- График 3: Гистограмма распределения цен ----
ax3 = fig.add_subplot(gs[1, 0])

# Логарифмическая шкала для лучшего отображения широкого диапазона
n, bins, patches = ax3.hist(df_all_prices['price'], bins=30, color='#2ecc71', 
                             edgecolor='white', alpha=0.8)
ax3.set_yscale('log')
ax3.set_xlabel('Цена (руб.)')
ax3.set_ylabel('Частота (лог. шкала)')
ax3.set_title('📊 Распределение цен (логарифмическая шкала)', fontweight='bold', pad=10)

# Добавляем линии среднего и медианы
ax3.axvline(stats['Среднее'], color='red', linestyle='--', linewidth=1.5, 
            label=f"Среднее: {stats['Среднее']:.0f} руб.")
ax3.axvline(stats['Медиана'], color='blue', linestyle='--', linewidth=1.5,
            label=f"Медиана: {stats['Медиана']:.0f} руб.")

ax3.legend(fontsize=8)

# Текстовый блок со статистикой
stats_text = f"Среднее: {stats['Среднее']:.0f}\nМедиана: {stats['Медиана']:.0f}\nStd: {stats['Стандартное отклонение']:.0f}"
ax3.text(0.95, 0.95, stats_text, transform=ax3.transAxes, va='top', ha='right',
         fontsize=8, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# ---- График 4: Количество товаров по категориям (круговая диаграмма) ----
ax4 = fig.add_subplot(gs[1, 1])

# Подготовка данных
categories = df_category_counts['category']
counts = df_category_counts['product_count']
colors_pie = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#dfe6e9']

wedges, texts, autotexts = ax4.pie(
    counts, labels=None, autopct='%1.0f%%',
    colors=colors_pie[:len(categories)], startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    pctdistance=0.7
)

# Увеличиваем подписи процентов
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')

ax4.set_title('🏷️ Распределение товаров по категориям', fontweight='bold', pad=10)

# Легенда с количеством
pie_labels = [f'{cat} ({cnt} шт.)' for cat, cnt in zip(categories, counts)]
ax4.legend(wedges, pie_labels, loc='lower center', bbox_to_anchor=(0.5, -0.35), 
           fontsize=8, frameon=False, ncol=3)

# ---- График 5: Количество поставщиков по категориям ----
ax5 = fig.add_subplot(gs[2, 0])

df_suppliers_sorted = df_suppliers_by_category.sort_values('supplier_count', ascending=True)

bars5 = ax5.barh(df_suppliers_sorted['category'], df_suppliers_sorted['supplier_count'], 
                 color='#9b59b6', edgecolor='white', height=0.6)

# Подписи значений
for bar, (_, row) in zip(bars5, df_suppliers_sorted.iterrows()):
    ax5.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
             f"{int(bar.get_width())} пост. ({row['product_count']} тов.)",
             va='center', fontsize=8)

ax5.set_xlabel('Количество поставщиков')
ax5.set_title('🔗 Количество поставщиков по категориям', fontweight='bold', pad=10)

# ---- График 6: Аномалии - товары без поставщиков ----
ax6 = fig.add_subplot(gs[2, 1])

if len(df_no_suppliers) > 0:
    # Группируем по категориям
    missing_by_cat = df_no_suppliers.groupby('category').size().sort_values(ascending=True)
    
    bars6 = ax6.barh(missing_by_cat.index, missing_by_cat.values, 
                     color='#e74c3c', edgecolor='white', height=0.6)
    
    # Подписи
    for bar, val in zip(bars6, missing_by_cat.values):
        ax6.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{int(val)} тов.', va='center', fontsize=9)
    
    ax6.set_xlabel('Количество товаров')
    ax6.set_title('⚠️ Товары без поставщиков (аномалии)', fontweight='bold', pad=10)
else:
    ax6.text(0.5, 0.5, '✅ Аномалий не обнаружено!\nВсе товары имеют поставщиков',
             ha='center', va='center', fontsize=12, transform=ax6.transAxes,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax6.set_title('✅ Проверка аномалий', fontweight='bold', pad=10)
    ax6.set_xticks([])
    ax6.set_yticks([])

# Общая подпись под фигурой
fig.text(0.5, -0.02, 
         f"📌 Статистика: всего товаров — {df_category_counts['product_count'].sum()}, "
         f"всего цен — {len(df_all_prices)}, "
         f"средняя цена — {stats['Среднее']:.0f} руб.",
         ha='center', fontsize=9, style='italic')

# Сохранение графика
plt.tight_layout()
OUTPUT_FILE = "task_7_analysis_charts.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"\n✅ График сохранён: {OUTPUT_FILE}")

# Показываем график
plt.show()

# ============= 4. ВЫВОДЫ ПО ГРАФИКАМ =============
print("\n" + "=" * 70)
print("📝 ВЫВОДЫ ПО РЕЗУЛЬТАТАМ АНАЛИЗА")
print("=" * 70)

print("""
1. 📊 ГРАФИК «Средняя цена по категориям»:
   → Показывает, какие категории товаров в среднем дороже.
   → Если есть категория со средней ценой значительно выше других — 
     это может говорить о премиальности товаров в этой категории.
   → Пунктирная линия — медиана всех цен (для сравнения).

2. 💰 ГРАФИК «Топ-10 самых дорогих товаров»:
   → Выявляет конкретные товары-лидеры по цене.
   → Позволяет понять, какие товары приносят наибольшую маржу.
   → Может использоваться для анализа ценовой политики.

3. 📊 ГРАФИК «Распределение цен»:
   → Гистограмма с логарифмической шкалой показывает форму распределения.
   → Красная линия — среднее, синяя — медиана.
   → Если среднее существенно больше медианы — распределение 
     имеет «длинный правый хвост» (есть очень дорогие товары).

4. 🏷️ ГРАФИК «Распределение товаров по категориям»:
   → Круговая диаграмма показывает долю каждой категории в ассортименте.
   → Помогает оценить сбалансированность товарного портфеля.

5. 🔗 ГРАФИК «Количество поставщиков по категориям»:
   → Показывает, насколько диверсифицированы поставки в каждой категории.
   → Малое количество поставщиков — потенциальный риск.

6. ⚠️ ГРАФИК «Товары без поставщиков»:
   → Выявляет аномалии в данных — товары, у которых нет привязанных поставщиков.
""")

# Аномалии
print("\n" + "=" * 70)
print("🔍 АНАМАЛИИ В ДАННЫХ")
print("=" * 70)

if len(df_no_suppliers) > 0:
    print(f"   ⚠️ Обнаружено {len(df_no_suppliers)} товаров без поставщиков:")
    for _, row in df_no_suppliers.head(10).iterrows():
        print(f"      • {row['product_name']} ({row['category']})")
    if len(df_no_suppliers) > 10:
        print(f"      ... и ещё {len(df_no_suppliers) - 10} товаров")
else:
    print("   ✅ Аномалий не обнаружено — все товары имеют поставщиков")

print("\n" + "=" * 70)
print(" " * 25 + "✅ АНАЛИЗ ЗАВЕРШЁН")
print("=" * 70)