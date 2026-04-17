import pandas as pd
import os

def get_menu_context() -> str:
    """
    Đọc dữ liệu menu từ file CSV và format thành chuỗi cho AI.
    """
    try:
        # File menu nằm ở data/Menu.csv
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Menu.csv')
        df = pd.read_csv(file_path)
        
        menu_str = "MENU CỦA QUÁN:\n"
        for index, row in df.iterrows():
            if row['available']:
                menu_str += f"- {row['name']} (ID: {row['item_id']}) - Mô tả: {row['description']}. Giá M: {row['price_m']} VND, Giá L: {row['price_l']} VND\n"
        return menu_str
    except Exception as e:
        print(f"Error loading menu: {e}")
        return "Menu đang được cập nhật."

# Khởi tạo MENU_DATA mỗi lần app chạy (có thể cache hoặc gọi real-time tùy nhu cầu)
MENU_DATA = get_menu_context()
