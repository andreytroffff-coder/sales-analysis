
import pandas as pd

# Читаем исходный CSV
df = pd.read_csv("sales.csv")

# Удаляем полностью повторяющиеся строки
df = df.drop_duplicates()

# Приводим дату к единому формату
df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")

# Считаем выручку только для доставленных заказов
df["revenue"] = (
    df["quantity"] * df["price"]
).where(df["status"].str.lower() == "delivered", 0)

# Группируем данные по артикулу и дате
result = (
    df.groupby(["sku", "order_date"], as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum")
    )
)

# Сортируем по артикулу и дате
result = result.sort_values(
    by=["sku", "order_date"]
)

# Сохраняем результат
result.to_csv("daily_by_sku.csv", index=False)

print("Файл daily_by_sku.csv успешно создан!")
