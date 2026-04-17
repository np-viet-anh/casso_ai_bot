from fastapi import APIRouter, BackgroundTasks, Request, Depends
from sqlalchemy.orm import Session
from app.services.ai_service import generate_reply
from app.services import bot_service
from app.services import payment_service
from app.db.database import get_db
from app.models.db_models import Order

router = APIRouter()

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Nhận webhook từ Telegram (Message hoặc Callback Query).
    """
    update = await request.json()
    
    # Xử lý khi có message thường
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        background_tasks.add_task(generate_reply, chat_id, text)
        
    return {"status": "ok"}

@router.post("/webhook/payos")
async def payos_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Webhook thực tế từ PayOS.
    """
    body = await request.json()
    
    try:
        # Nhắc lại body ra terminal để theo dõi
        print(f"\n[Webhook PAYOS] Đã nhận tín hiệu mới: {body}\n")
        
        # Xác thực Webhook từ PayOS bằng Checksum Key (API v2)
        webhook_data = payment_service.payos_client.webhooks.verify(body)
        
        # 'code' của giao dịch thành công là "00"
        if webhook_data.code == "00":
            order_code = webhook_data.order_code
            
            # Khởi tạo db update
            order = db.query(Order).filter(Order.order_code == order_code, Order.status == "PENDING").first()
            if order:
                chat_id = order.chat_id
                
                # Cập nhật status
                order.status = "PAID"
                db.commit()
                
                # Báo cho khách hàng
                success_text = f"✅ Ting ting! Cô đã nhận được tiền hoá đơn {order_code} của con rồi nhé. Cô đang pha chế rồi, con đợi lát nhé!"
                bot_service.send_message(chat_id, success_text)
                
    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        print("Webhook validation error:", err_str)
        return {"status": "error", "message": str(e), "traceback": err_str}
        
    return {"status": "success", "message": "Webhook processed"}

