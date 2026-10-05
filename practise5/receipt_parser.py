import json

# --- 1. Читаем файл ---
file = open("raw.txt", "r", encoding="utf-8")
text = file.read()
file.close()

# Разбиваем текст на строки и убираем пустые
lines = []
for line in text.split("\n"):
    line = line.strip()
    if line != "":
        lines.append(line)

# --- 2. Собираем товары ---
items = []
i = 0
while i < len(lines):
    line = lines[i]

    # Если строка начинается с "1.", "2." и т.д. — это новый товар
    if line.endswith(".") and line[:-1].isdigit():
        number = int(line[:-1])

        # Название — следующая строка
        name = lines[i + 1]

        # Строка с количеством и ценой выглядит так: "2,000 x 154,00"
        qty_price = lines[i + 2]
        parts = qty_price.split(" x ")
        quantity = float(parts[0].replace(",", "."))
        price = float(parts[1].replace(" ", "").replace(",", "."))

        # Сумма — следующая строка
        total = float(lines[i + 3].replace(" ", "").replace(",", "."))

        items.append({
            "number": number,
            "name": name,
            "quantity": quantity,
            "price": price,
            "sum": total,
        })

        # Перепрыгиваем через уже прочитанные строки (номер, имя, кол-во×цена, сумма, "Стоимость")
        i = i + 5
    else:
        i = i + 1

# --- 3. Ищем итоги, дату и способ оплаты ---
total_sum = 0.0
vat = 0.0
payment = 0.0
date = ""
time = ""
pay_method = "unknown"

for i in range(len(lines)):
    line = lines[i]

    if line == "ИТОГО:":
        total_sum = float(lines[i + 1].replace(" ", "").replace(",", "."))

    if line == "в т.ч. НДС 12%:":
        vat = float(lines[i + 1].replace(" ", "").replace(",", "."))

    if line == "Банковская карта:":
        payment = float(lines[i + 1].replace(" ", "").replace(",", "."))
        pay_method = "bank card"

    if line.startswith("Время:"):
        # строка: "Время: 18.04.2019 11:13:58"
        parts = line.replace("Время:", "").strip().split(" ")
        date = parts[0]
        time = parts[1]

# --- 4. Считаем сумму всех товаров для проверки ---
items_total = 0.0
for item in items:
    items_total = items_total + item["sum"]

# --- 5. Собираем результат ---
result = {
    "date": date,
    "time": time,
    "items": items,
    "total": total_sum,
    "vat": vat,
    "payment_method": pay_method,
    "payment_amount": payment,
    "items_total": items_total,
}

# --- 6. Печатаем красиво ---
print("=" * 60)
print("ЧЕК")
print("=" * 60)
print("Дата:", date, " Время:", time)
print("-" * 60)

for item in items:
    print(item["number"], ".", item["name"])
    print("   ", item["quantity"], "x", item["price"], "=", item["sum"])

print("-" * 60)
print("ИТОГО:", total_sum)
print("НДС:  ", vat)
print("Оплата:", pay_method, "-", payment)
print("=" * 60)

# Проверяем, сходится ли сумма
if items_total == total_sum:
    print("Проверка: всё сходится")
else:
    print("Проверка: сумма товаров", items_total, "не равна итогу", total_sum)

# --- 7. Сохраняем в JSON ---
file = open("receipt_parsed.json", "w", encoding="utf-8")
json.dump(result, file, ensure_ascii=False, indent=2)
file.close()

print("JSON сохранён в receipt_parsed.json")