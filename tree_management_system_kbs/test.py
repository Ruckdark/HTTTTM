self.rules = [
    {"condition": lambda tree: tree.water_status == "Wet",  # Kiểm tra tình trạng nước trước
     "action": "Cây quá nhiều nước, cần kiểm tra lại hệ thống thoát nước."},
    
    {"condition": lambda tree: tree.height > 20 and tree.health_status == "Good",  # Cây cao cần gia cố
     "action": "Cây cao, cần gia cố hoặc cắt tỉa cành để tránh đổ hoặc gãy trong gió mạnh."},
    
    {"condition": lambda tree: tree.health_status == "Good" and tree.age > 10,  # Cây khỏe mạnh nhưng đất thiếu dinh dưỡng
     "action": "Cây khỏe mạnh nhưng đất trồng có thể thiếu dinh dưỡng, cần cải tạo đất và bón phân hữu cơ."},
    
    {"condition": lambda tree: tree.leaf_color == "Brown" and tree.health_status == "Weak" and tree.age < 10,  # Cây cháy nắng
     "action": "Cây có thể bị cháy nắng, cần di chuyển vào nơi râm mát hoặc cung cấp bóng mát."},
    
    {"condition": lambda tree: tree.water_status == "Dry",  # Cây thiếu nước
     "action": "Cây thiếu nước, cần tưới nước ngay."},
    
    {"condition": lambda tree: tree.pest_infestation == True,  # Cây bị sâu bệnh
     "action": "Cây bị sâu bệnh, cần phun thuốc trừ sâu ngay."},
    
    {"condition": lambda tree: tree.species == "Xà Cừ" and tree.health_status == "Good",  # Cây Xà Cừ ra hoa
     "action": "Cây đang ra hoa, cần chăm sóc đặc biệt và bổ sung dinh dưỡng."},
    
    {"condition": lambda tree: tree.leaf_color == "Brown" and tree.health_status == "Poor",  # Cây nguy cơ mục rỗng
     "action": "Cây có nguy cơ mục rỗng. Cần xử lý khẩn cấp để đảm bảo an toàn."},
    
    {"condition": lambda tree: tree.height > 15 and tree.health_status == "Good",  # Cây khỏe mạnh, bảo dưỡng định kỳ
     "action": "Cây khỏe mạnh, cần bảo dưỡng định kỳ."},
    
    {"condition": lambda tree: tree.age > 70 and tree.health_status == "Weak",  # Cây già yếu
     "action": "Cây già yếu. Cần gia cố hoặc cắt tỉa cành."},
    
    {"condition": lambda tree: tree.leaf_color == "Yellow" and tree.health_status == "Weak",  # Cây thiếu dinh dưỡng
     "action": "Cây thiếu dinh dưỡng. Cần bón phân và tưới nước bổ sung."},
    
    {"condition": lambda tree: tree.health_status == "Poor",  # Cây cần kiểm tra gốc rễ
     "action": "Cần kiểm tra gốc và rễ cây, có thể cần thay thế cây."}
]
