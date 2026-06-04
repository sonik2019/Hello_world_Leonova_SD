#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import pandas as pd
import sys

# ============= НАСТРОЙКИ ПОДКЛЮЧЕНИЯ =============
DB_CONFIG = {
    "host": "localhost",
    "port": "5435",           
    "user": "postgres_task",  
    "password": "student",    
    "database": "student"     
}

print("=" * 70)
print(" " * 15 + "ЗАДАНИЕ 6.18 - СТАТИСТИЧЕСКИЙ АНАЛИЗ ДАННЫХ")
print("=" * 70)

try:
    # ============= ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ =============
    print(f"\n[1] Подключение к БД {DB_CONFIG['database']} на порту {DB_CONFIG['port']}...")
    connection = psycopg2.connect(**DB_CONFIG)
    print("    ✅ ПОДКЛЮЧЕНИЕ УСТАНОВЛЕНО!\n")

    # ============= SQL-ЗАПРОС =============
    query = """
    SELECT 
        p.id AS product_id,
        p.name AS product_name,
        p.category,
        pr.price,
        pr.created_at,
        s.name AS supplier_name
    FROM prices pr
    JOIN products p ON pr.product_id = p.id
    LEFT JOIN suppliers s ON p.id = s.product_id
    ORDER BY p.category, p.name, pr.created_at
    """
    
    print("[2] Загрузка данных из таблиц...")
    df = pd.read_sql(query, connection)
    print(f"    ✅ ЗАГРУЖЕНО {len(df)} ЗАПИСЕЙ\n")

    # ============= 1. ПЕРВИЧНЫЙ ОСМОТР =============
    print("=" * 70)
    print("1. ПЕРВИЧНЫЙ ОСМОТР ДАННЫХ")
    print("=" * 70)
    
    print(f"\n   Всего записей о ценах: {len(df)}")
    print(f"   Уникальных товаров: {df['product_id'].nunique()}")
    print(f"   Уникальных категорий: {df['category'].nunique()}")
    print(f"   Категории: {', '.join(df['category'].unique())}")
    print(f"   Диапазон цен: от {df['price'].min():.2f} до {df['price'].max():.2f} руб.")
    print(f"   Пропуски в цене: {df['price'].isna().sum()}")
    
    print("\n   Первые 5 записей:")
    print(df.head(5).to_string(index=False))

    # ============= 2. ОПИСАТЕЛЬНАЯ СТАТИСТИКА =============
    print("\n" + "=" * 70)
    print("2. ОПИСАТЕЛЬНАЯ СТАТИСТИКА ЦЕН")
    print("=" * 70)
    
    print(f"\n   Среднее (mean)      : {df['price'].mean():12.2f} руб.")
    print(f"   Медиана (median)    : {df['price'].median():12.2f} руб.")
    print(f"   Ст. отклонение (std): {df['price'].std():12.2f} руб.")
    print(f"   Минимум (min)       : {df['price'].min():12.2f} руб.")
    print(f"   Максимум (max)      : {df['price'].max():12.2f} руб.")

    # ============= 3. КВАРТИЛИ =============
    print("\n" + "=" * 70)
    print("3. КВАРТИЛИ И IQR")
    print("=" * 70)
    
    q1 = df['price'].quantile(0.25)
    q2 = df['price'].quantile(0.50)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1
    
    print(f"   Q1 (25-й перцентиль): {q1:12.2f} руб.")
    print(f"   Q2 (50-й) - медиана : {q2:12.2f} руб.")
    print(f"   Q3 (75-й перцентиль): {q3:12.2f} руб.")
    print(f"   IQR (Q3 - Q1)       : {iqr:12.2f} руб.")
    
    # Товары выше Q3
    expensive = df[df['price'] > q3][['product_name', 'price']].drop_duplicates()
    print(f"\n   Товаров с ценой ВЫШЕ Q3 (> {q3:.2f} руб.): {len(expensive)} шт.")
    if len(expensive) > 0:
        print("   Примеры:")
        for _, row in expensive.head(5).iterrows():
            print(f"      • {row['product_name'][:35]:35s} — {row['price']:10.2f} руб.")

    # ============= 4. СТАТИСТИКА ПО КАТЕГОРИЯМ =============
    print("\n" + "=" * 70)
    print("4. СТАТИСТИКА ПО КАТЕГОРИЯМ")
    print("=" * 70)
    
    by_category = df.groupby('category')['price'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std'
    ).round(2).sort_values('mean', ascending=False)
    
    print(by_category.to_string())
    
    best_cat = by_category.index[0]
    worst_cat = by_category.index[-1]
    print(f"\n   📈 Самая дорогая категория: {best_cat} ({by_category.loc[best_cat, 'mean']:.2f} руб.)")
    print(f"   📉 Самая дешёвая категория: {worst_cat} ({by_category.loc[worst_cat, 'mean']:.2f} руб.)")

    # ============= 5. РЕЙТИНГ ТОВАРОВ =============
    print("\n" + "=" * 70)
    print("5. ТОП-10 САМЫХ ДОРОГИХ ТОВАРОВ")
    print("=" * 70)
    
    by_product = df.groupby('product_name')['price'].agg(
        changes='count',
        avg_price='mean'
    ).round(2).sort_values('avg_price', ascending=False)
    
    print(by_product.head(10).to_string())
    
    if len(by_product) > 0:
        print(f"\n   🥇 Самый дорогой: {by_product.index[0]} ({by_product.iloc[0]['avg_price']:.2f} руб.)")
        print(f"   🥉 Самый дешёвый: {by_product.index[-1]} ({by_product.iloc[-1]['avg_price']:.2f} руб.)")

    # ============= 6. ТОВАРЫ С НАИБОЛЬШИМ РАЗБРОСОМ =============
    print("\n" + "=" * 70)
    print("6. ТОВАРЫ С НАИБОЛЬШИМ РАЗБРОСОМ ЦЕН")
    print("=" * 70)
    
    # ИСПРАВЛЕНО: правильно считаем разброс
    price_range = df.groupby('product_name')['price'].agg([
        ('min_price', 'min'),
        ('max_price', 'max'),
        ('spread', lambda x: x.max() - x.min())
    ]).round(2).sort_values('spread', ascending=False).head(5)
    
    print(price_range.to_string())

    # ============= 7. РАСПРЕДЕЛЕНИЕ ЦЕН =============
    print("\n" + "=" * 70)
    print("7. РАСПРЕДЕЛЕНИЕ ЦЕН")
    print("=" * 70)
    
    bins = [0, 1000, 5000, 10000, 25000, 50000, 100000, float('inf')]
    labels = ['<1k', '1k-5k', '5k-10k', '10k-25k', '25k-50k', '50k-100k', '>100k']
    df['price_group'] = pd.cut(df['price'], bins=bins, labels=labels)
    
    for group, count in df['price_group'].value_counts().sort_index().items():
        pct = count / len(df) * 100
        bar = '█' * int(pct // 2)
        print(f"   {group:10s}: {count:4d} записей ({pct:5.1f}%) {bar}")

    # ============= 8. КОРРЕЛЯЦИЯ =============
    print("\n" + "=" * 70)
    print("8. КОРРЕЛЯЦИЯ ЦЕНЫ С КОЛИЧЕСТВОМ ПОСТАВЩИКОВ")
    print("=" * 70)
    
    supplier_count = df.groupby('product_id')['supplier_name'].nunique().reset_index()
    supplier_count.columns = ['product_id', 'supplier_count']
    df_with_suppliers = df.merge(supplier_count, on='product_id').drop_duplicates('product_id')
    
    correlation = df_with_suppliers['price'].corr(df_with_suppliers['supplier_count'])
    print(f"   Коэффициент корреляции: {correlation:.3f}")
    if correlation > 0.3:
        print("   ➕ Слабая положительная связь")
    elif correlation < -0.3:
        print("   ➖ Слабая отрицательная связь")
    else:
        print("   ⚪ Значимой связи не обнаружено")

    # ============= 9. ОТВЕТЫ НА ВОПРОСЫ =============
    print("\n" + "=" * 70)
    print("9. ОТВЕТЫ НА КОНТРОЛЬНЫЕ ВОПРОСЫ")
    print("=" * 70)
    
    print(f"""
    Вопрос 1: Сколько всего записей в таблице prices?
       → {len(df)} записей

    Вопрос 2: Какие значения принимает поле price? Есть ли пропуски?
       → от {df['price'].min():.2f} до {df['price'].max():.2f} руб.
       → пропусков: {df['price'].isna().sum()}

    Вопрос 3: Какие категории товаров есть в данных?
       → {', '.join(df['category'].unique())}

    Вопрос 4: Чему равно среднее? Совпадает с медианой?
       → среднее = {df['price'].mean():.2f} руб.
       → медиана = {df['price'].median():.2f} руб.
       → {'НЕ совпадают' if abs(df['price'].mean() - df['price'].median()) > 100 else 'Совпадают'}

    Вопрос 5: О чём говорит стандартное отклонение?
       → std = {df['price'].std():.2f} руб.
       → Это говорит о {'большом разбросе' if df['price'].std() > 20000 else 'умеренном разбросе'} цен

    Вопрос 6: Есть ли товары с минимальной ценой?
       → Минимум {df['price'].min():.2f} руб.

    Вопрос 7: Какая категория имеет самую высокую среднюю цену?
       → {best_cat} ({by_category.loc[best_cat, 'mean']:.2f} руб.)

    Вопрос 8: У какого товара наибольший разброс цен?
       → {price_range.index[0]} (разброс {price_range.iloc[0]['spread']:.2f} руб.)
    """)

    print("=" * 70)
    print(" " * 25 + "✅ АНАЛИЗ ЗАВЕРШЁН")
    print("=" * 70)

except Exception as error:
    print(f"\n❌ ОШИБКА: {error}")
    print("\nПроверьте:")
    print("  1. Запущен ли контейнер: docker ps")
    print("  2. Параметры подключения (порт 5435, БД student)")
    print("  3. Установлены ли библиотеки: pip install pandas psycopg2-binary")
    import traceback
    traceback.print_exc()
    sys.exit(1)