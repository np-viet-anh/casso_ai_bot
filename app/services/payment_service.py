import time
import urllib.parse
from payos import PayOS
from payos.type import PaymentData, ItemData
from app.core.config import settings
from app.services import bot_service

payos_client = PayOS(
    client_id=settings.payos_client_id,
    api_key=settings.payos_api_key,
    checksum_key=settings.payos_checksum_key
)

from app.db.database import SessionLocal
from app.models.db_models import Order

def process_payment(chat_id: int, amount: int, items_desc: str, cust_info: str):
    """
    Tạo link thanh toán PayOS thực tế, gửi cho khách và lưu DB.
    """
    try:
        # Tạo OrderCode duy nhất (dùng timestamp)
        order_code = int(time.time() * 1000) % 1000000000 
        
        # Ghi data xuống DB
        db = SessionLocal()
        try:
            new_order = Order(
                order_code=order_code,
                chat_id=chat_id,
                order_items=items_desc,
                customer_info=cust_info,
                amount=amount,
                status="PENDING"
            )
            db.add(new_order)
            db.commit()
        except Exception as db_err:
            print("Lỗi lưu DB:", db_err)
            db.rollback()
        finally:
            db.close()

        # Cắt bớt description cho ItemData để không quá dài
        short_desc = items_desc[:50]

        payment_data = PaymentData(
            orderCode=order_code,
            amount=amount,
            description="Thanh toan don TS", # Không dài quá 25 ký tự
            items=[ItemData(name=short_desc, quantity=1, price=amount)],
            cancelUrl="https://web.telegram.org/a/#8701359518",
            returnUrl="https://web.telegram.org/a/#8701359518"  
        )

        # Trả về kết quả link từ PayOS
        payment_link = payos_client.createPaymentLink(paymentData=payment_data)
        checkout_url = payment_link.checkoutUrl
        
        # Lấy file ảnh QR trực tiếp qua VietQR API
        bin_bank = payment_link.bin
        acc_num = payment_link.accountNumber
        acc_name = payment_link.accountName
        desc_qr = payment_link.description
        
        # Encode URL parameters (đề phòng có dấu cách)
        encoded_acc_name = urllib.parse.quote(acc_name) if acc_name else ""
        encoded_desc = urllib.parse.quote(desc_qr) if desc_qr else ""
        
        qr_url = f"https://img.vietqr.io/image/{bin_bank}-{acc_num}-compact2.jpg?amount={amount}&addInfo={encoded_desc}&accountName={encoded_acc_name}"
        
        caption = f"Mã thanh toán đơn hàng đây nha. Bấm vào nút dưới hoặc link sau để thanh toán {amount:,} VNĐ nhé!\n\n👉 {checkout_url}"
        
        # Gửi ảnh trước, kèm caption
        bot_service.send_photo(chat_id, qr_url, caption=caption)

    except Exception as e:
        print("Lỗi tạo QR payment API:", e)
        bot_service.send_message(chat_id, "Lỗi kết nối PayOS, con đợi cô xíu nha!")
