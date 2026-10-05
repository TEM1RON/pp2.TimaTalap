import json

file = open("raw.txt", "r", encoding="utf-8")
text = file.read()
file.close()

lines = []
for line in text.split("\n"):
    line = line.strip()
    if line != "":
        lines.append(line)
        
items = []
i = 0
while i < len(lines):
    line = lines[i]

    if line.endswith(".") and line[:-1].isdigit():
        number = int(line[:-1])

        name = lines[i + 1]

        qty_price = lines[i + 2]
        parts = qty_price.split(" x ")
        quantity = float(parts[0].replace(",", "."))
        price = float(parts[1].replace(" ", "").replace(",", "."))

        total = float(lines[i + 3].replace(" ", "").replace(",", "."))

        items.append({
            "number": number,
            "name": name,
            "quantity": quantity,
            "price": price,
            "sum": total,
        })

        i = i + 5
    else:
        i = i + 1

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
        parts = line.replace("Время:", "").strip().split(" ")
        date = parts[0]
        time = parts[1]

items_total = 0.0
for item in items:
    items_total = items_total + item["sum"]

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

if items_total == total_sum:
    print("Проверка: всё сходится")
else:
    print("Проверка: сумма товаров", items_total, "не равна итогу", total_sum)

file = open("receipt_parsed.json", "w", encoding="utf-8")
json.dump(result, file, ensure_ascii=False, indent=2)
file.close()

print("JSON сохранён в receipt_parsed.json")