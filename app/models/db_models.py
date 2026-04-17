from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.sql import func
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    # PayOS order code sinh ngẫu nhiên khá to, nên dùng BigInteger
    order_code = Column(BigInteger, unique=True, index=True) 
    chat_id = Column(BigInteger)
    order_items = Column(Text)       # Trích xuất danh sách món AI phân tích
    customer_info = Column(Text)     # Tên, địa chỉ, sđt
    amount = Column(Integer)
    status = Column(String, default="PENDING") # PENDING, PAID, DELIVERED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
