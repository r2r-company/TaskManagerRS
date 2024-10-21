from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm
import os

# Вказуємо шлях до шрифту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')

def generate_invoice_template(invoice):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Реєструємо шрифт для підтримки кирилиці
    pdfmetrics.registerFont(TTFont('DejaVu', FONT_PATH))
    p.setFont("DejaVu", 10)

    # Встановлюємо координати початку
    x_start = 15 * mm  # Вирівнюємо поля ближче до краю
    y_start = 270 * mm

    # Інформація про компанію (лівіше)
    p.drawString(x_start, y_start, "Організація:")
    p.setFont("DejaVu", 12)
    p.drawString(x_start + 50 * mm, y_start, "Роберт Сервіс")
    p.setFont("DejaVu", 10)



    # Заголовок рахунку (нижче)
    p.setFont("DejaVu", 14)
    p.drawString(x_start, y_start - 60, f"Рахунок на оплату № {invoice.invoice_number}")
    p.drawString(x_start, y_start - 75, f"Від {invoice.creation_date.strftime('%d.%m.%Y')} р.")

    # Інформація про виконавця та замовника
    p.setFont("DejaVu", 10)

    # Таблиця послуг (вирівнювання та відступи)
    data = [
        ['№', 'Найменування', 'Кількість', 'Ціна', 'Сума'],
    ]
    for index, service in enumerate(invoice.services.all(), 1):
        data.append([str(index), service.service_name, str(service.quantity), f"{service.price:.2f} грн", f"{service.quantity * service.price:.2f} грн"])

    data.append(['', '', '', 'Всього:', f"{invoice.total_amount:.2f} грн"])

    # Створюємо таблицю з відступами
    table = Table(data, colWidths=[15 * mm, 85 * mm, 25 * mm, 30 * mm, 35 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, -1), 'DejaVu'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    # Виводимо таблицю нижче заголовка
    table.wrapOn(p, 0, 0)
    table.drawOn(p, x_start, y_start - 160)

    # Підсумок нижче таблиці
    p.drawString(x_start, y_start - 170 - (len(invoice.services.all()) * 20), f"Всього до сплати: {invoice.total_amount:.2f} грн")
    p.drawString(x_start, y_start - 180 - (len(invoice.services.all()) * 20), f"Виконавець: {invoice.executor.get_full_name()}")

    # Закінчуємо PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
