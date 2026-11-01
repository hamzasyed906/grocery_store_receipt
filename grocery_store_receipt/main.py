import csv
from csv import writer, reader
import reportlab
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors 

inventory = r"inventory.csv"

updatedinven = []
items = {}

with open(inventory, "r") as f:
    reader = csv.reader(f)

    for row in reader:
        items[row[0].lower()] = {"price": float(row[1]), "stock": int(row[2])}

print("Available items:")
print("-------------------")

for item in items:
    print(item, "-", "$" + str(items.get(item, {}).get("price")), "- Stock: " + str(items.get(item, {}).get("stock")))

subtotal = 0
receipt = []

while True:
    item = input("\nEnter item name or enter done ").lower()

    if item == "done":
        break

    if item not in items:
        print("item not found")

    else:
        try:
            quantity = int(input("Enter Quantity: "))

        except ValueError:
            print("Please enter a correct value")
            break

        price = items[item]["price"]
        stock = items[item]["stock"]

        if quantity > stock or quantity < 0:
            print("Quantity not possible")
            break

        else:
            total = price * quantity
            subtotal += total

            receipt.append([item.title(), quantity, price, total])

            items[item]["stock"] -= quantity

            updatedinven.clear()

            with open(inventory, "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    if row[0].lower() == item:
                        row[2] = str(items[item]["stock"])

                    updatedinven.append(row)

            with open(inventory, "w", newline="") as f:
                csv_writer = writer(f)
                csv_writer.writerows(updatedinven)

gst = subtotal * 0.05
grand_total = subtotal + gst

print("\nReceipt:")
print("-------------------")

for item in receipt:
    print(item[0])
    print("Quantity:", item[1])
    print("Unit Price: $", item[2])
    print("Total Price: $", round(item[3], 2))
    print()

print("Subtotal: $", round(subtotal, 2))
print("GST (5%): $", round(gst, 2))
print("Grand Total: $", round(grand_total, 2))

print("\nThank You for Shopping!")

pdf = canvas.Canvas("receipt.pdf")

pdf.setFont("Courier", 20)
pdf.drawString(220, 790, "Grocery Store")

pdf.setFont("Courier", 15)
pdf.drawString(215, 760, "Date:" + datetime.now().strftime("%d-%m-%y %H:%M"))

pdf.setFont("Courier", 11)
pdf.drawString(76, 808, "----------------------------------------------------------------")
pdf.drawString(76, 779, "----------------------------------------------------------------")
pdf.drawString(76, 750, "----------------------------------------------------------------")

x = 91
y = 730

for item in receipt:
    name = f"{str(item[1])}x {str(item[0])}"
    price = f"Price: ${str(round(item[3], 2))}"

    pdf.setFont("Courier", 12)
    pdf.drawString(x, y, name)
    y = y - 20
    pdf.drawString(x, y, price)
    y = y - 35

pdf.setDash(3, 3)
pdf.line(76, y, 498, y)
y = y - 30

pdf.setFont("Courier", 15)
pdf.drawString(x, y, f"Subtotal: ${subtotal}")
y = y - 20

pdf.drawString(x, y, f"GST(%5): %{gst}")
y = y - 20

pdf.drawString(x, y, f"Grand Total: ${grand_total}")
y = y - 50

pdf.drawString(193, y, "Thank You for Shopping")

pdf.drawImage(
    "logo.png",
    300,
    10,
    width=300,
    height=300,
    mask="auto"
)

pdf.save()

#in this code even though "logo.jpeg" has no background it shows a black background on the pdf file