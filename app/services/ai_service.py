import json
from openai import OpenAI
from app.core.config import settings
from app.services.menu_service import MENU_DATA
from app.services import bot_service
from app.services import payment_service

# Khởi tạo OpenAI Client
client = OpenAI(api_key=settings.openai_api_key)


# In-memory session lưu trữ (dùng tạm thời, có thể thay thế bằng Redis)
user_sessions = {}

SYSTEM_PROMPT = f"""
Bạn là một bản sao AI của "Cô chủ quán" trà sữa thân thiện, xởi lởi.
Giọng điệu: Vui vẻ, nhiệt tình, xưng "cô" gọi "con" hoặc "bạn", hay dùng emoji.

Nhiệm vụ:
1. Chào hỏi, tư vấn món dựa trên Menu sau (liệt kê đầy đủ, có giá cả rõ ràng để khách dễ chọn):
{MENU_DATA}

2. Lấy đủ thông tin: Tên món, Size (M/L), Số lượng, Tên khách, SĐT, Địa chỉ nhận.
3. TUYỆT ĐỐI KHÔNG TÍNH TIỀN KHI CHƯA CHỐT ĐỦ THÔNG TIN.
4. Tổng kết lại hóa đơn và HỎI KHÁCH XÁC NHẬN (Ví dụ: "Con xem đúng chưa để cô chốt nhé?"). 
5. CHỈ KHI NÀO KHÁCH ĐỒNG Ý (Ví dụ khách nói: "Ok", "Đúng rồi", "Chốt"), bạn mới báo khách đợi mã QR và BẮT BUỘC TRẢ VỀ khối JSON theo đúng định dạng sau ở cuối câu:

{{
  "action": "create_payment",
  "total_amount": 100000,
  "order_items": "1x Trà sữa trân châu XL, 1x Hồng trà M",
  "customer_info": "Tên, SĐT, Địa chỉ"
}}

Lưu ý: Tuyệt đối KHÔNG xuất ra JSON nếu khách chưa xác nhận đồng ý!
"""

def generate_reply(chat_id: int, user_text: str):
    """
    Xử lý text user gửi lên, gọi LLM qua Groq, trả về bot_service và payment_service.
    """
    try:
        # Gửi hành động đang gõ
        bot_service.send_chat_action(chat_id, 'typing')

        # Khởi tạo session nếu khách mới
        if chat_id not in user_sessions:
            user_sessions[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Lưu tin nhắn khách
        user_sessions[chat_id].append({"role": "user", "content": user_text})

        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=user_sessions[chat_id],
            temperature=0.7
        )
        
        bot_reply = response.choices[0].message.content
        user_sessions[chat_id].append({"role": "assistant", "content": bot_reply})
        
        # Bóc tách JSON nếu có
        if "{" in bot_reply and '"action"' in bot_reply and '"create_payment"' in bot_reply:
            try:
                start_idx = bot_reply.find('{')
                end_idx = bot_reply.rfind('}') + 1
                
                json_str = bot_reply[start_idx:end_idx]
                text_part = bot_reply[:start_idx].replace("```json", "").replace("```", "").strip()
                
                # Gửi lời chào trước khi gửi ảnh (nếu có)
                if text_part:
                    bot_service.send_message(chat_id, text_part)
                
                # Parse JSON
                order_data = json.loads(json_str)
                amount = order_data.get('total_amount', 0)
                items = order_data.get('order_items', 'Đơn hàng')
                cust_info = order_data.get('customer_info', 'Khách lạ')
                
                # Chuyển qua service tạo QR và ghi DB
                payment_service.process_payment(chat_id, amount, items, cust_info)
                
            except Exception as e:
                print("Lỗi Parse JSON:", e)
                bot_service.send_message(chat_id, "Cô đang lú chút, con nhắn lại giúp cô nha!")
        else:
            bot_service.send_message(chat_id, bot_reply.replace("```json", "").replace("```", ""))
            
    except Exception as e:
        print(f"Error AI: {e}")
        bot_service.send_message(chat_id, "Xin lỗi con, tiệm đang đông khách quá, con chờ cô xíu nha...")
