from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.models.db_models import Order
from app.services import bot_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Hiển thị trang Dashboard tổng hợp các đơn hàng.
    """
    # Lấy danh sách các đơn hàng và sắp xếp theo thời gian tạo mới nhất
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={"orders": orders, "timedelta": timedelta}
    )

@router.post("/dashboard/ship/{order_code}")
async def ship_order(order_code: int, db: Session = Depends(get_db)):
    """
    Xử lý nút Giao Hàng trên Dashboard. Cập nhật trạng thái và thông báo khách.
    """
    order = db.query(Order).filter(Order.order_code == order_code).first()
    
    if order and order.status == "PAID":
        # Đổi trạng thái qua DELIVERED
        order.status = "DELIVERED"
        db.commit()
        
        # Nhắc Bot gửi Telegram báo khách hàng
        chat_id = order.chat_id
        text = f"🛵 Alo con ơi! Đơn hàng #{order_code} của con đã làm xong và đang được giao nhé! Cầm điện thoại ra lấy trà sữa nha!"
        bot_service.send_message(chat_id, text)
        
        return {"status": "success", "message": "Đã đổi trạng thái sang DELIVERED và báo tin Teleram."}
        
    return {"status": "error", "message": "Không tìm thấy đơn hàng hoặc đơn chưa thanh toán!"}
