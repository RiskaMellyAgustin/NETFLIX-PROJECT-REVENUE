# customerapp/utils.py

from datetime import datetime
from .models import Subscription
from datetime import date


def generate_order_id():
    # Ambil tanggal hari ini dalam format YYYYMMDD
    today = datetime.now().strftime("%Y%m%d")

    # Hitung jumlah subscription yang dibuat hari ini
    count_today = (
        Subscription.objects.filter(created_at__date=datetime.today().date()).count()
        + 1
    )

    # Format urutan ke 4 digit (contoh: 0001)
    order_id = f"INV-{today}-{count_today:04d}"
    return order_id
