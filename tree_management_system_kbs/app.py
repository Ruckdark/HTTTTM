from db_queries import fetch_all_trees, add_tree
import sys
import matplotlib.pyplot as plt
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

# Hệ thống chẩn đoán cây xanh sử dụng tri thức
class TreeKnowledgeBase:
    def __init__(self):
        # Tri thức suy luận IF-THEN dạng quy tắc
        self.rules = [
            {"condition": lambda tree: tree.health_status == "Poor", 
             "action": "Cần kiểm tra gốc và rễ cây, có thể cần thay thế cây."},
            {"condition": lambda tree: tree.leaf_color == "Yellow" and tree.health_status == "Weak",
             "action": "Cây thiếu dinh dưỡng. Cần bón phân và tưới nước bổ sung."},
            {"condition": lambda tree: tree.age > 70 and tree.health_status == "Weak",
             "action": "Cây già yếu. Cần gia cố hoặc cắt tỉa cành."},
            {"condition": lambda tree: tree.height > 15 and tree.health_status == "Good",
             "action": "Cây khỏe mạnh, cần bảo dưỡng định kỳ."},
            {"condition": lambda tree: tree.leaf_color == "Brown" and tree.health_status == "Poor",
             "action": "Cây có nguy cơ mục rỗng. Cần xử lý khẩn cấp để đảm bảo an toàn."},
            {"condition": lambda tree: tree.species == "Xà Cừ" and tree.health_status == "Good",
             "action": "Cây đang ra hoa, cần chăm sóc đặc biệt và bổ sung dinh dưỡng."},
            {"condition": lambda tree: tree.pest_infestation == True,
             "action": "Cây bị sâu bệnh, cần phun thuốc trừ sâu ngay."},
            {"condition": lambda tree: tree.water_status == "Dry",
             "action": "Cây thiếu nước, cần tưới nước ngay."},
            {"condition": lambda tree: tree.leaf_color == "Brown" and tree.health_status == "Weak" and tree.age < 10,
             "action": "Cây có thể bị cháy nắng, cần di chuyển vào nơi râm mát hoặc cung cấp bóng mát."},
            {"condition": lambda tree: tree.health_status == "Good" and tree.age > 10,
             "action": "Cây khỏe mạnh nhưng đất trồng có thể thiếu dinh dưỡng, cần cải tạo đất và bón phân hữu cơ."},
            {"condition": lambda tree: tree.height > 20 and tree.health_status == "Good",
             "action": "Cây cao, cần gia cố hoặc cắt tỉa cành để tránh đổ hoặc gãy trong gió mạnh."},
            {"condition": lambda tree: tree.water_status == "Wet",
             "action": "Cây quá nhiều nước, cần kiểm tra lại hệ thống thoát nước."}
        ]

    def diagnose_tree(self, tree):
        print(f"\n[Chẩn đoán cây {tree.tree_id} - Loài: {tree.species}]")  
        recommendations = []
        for rule in self.rules:
            if rule["condition"](tree):
                recommendations.append(f"-> Khuyến nghị: {rule['action']}")

        if recommendations:
            for recommendation in recommendations:
                print(recommendation)
        else:
            print("-> Không có khuyến nghị cụ thể. Cây ở trạng thái bình thường.")
        
        return tree.health_status  # Trả về tình trạng sức khỏe của cây

# main
knowledge_base = TreeKnowledgeBase()

# Lấy danh sách cây từ database
trees = fetch_all_trees()
if not trees:
    print("Không có dữ liệu cây nào trong hệ thống.")
else:
    # Chẩn đoán từng cây và thu thập dữ liệu cho biểu đồ
    health_statuses = []  # Danh sách lưu trữ tình trạng sức khỏe của các cây
    for tree in trees:
        health_status = knowledge_base.diagnose_tree(tree)
        health_statuses.append(health_status)

    # Vẽ biểu đồ thống kê tình trạng sức khỏe của cây
    health_status_counts = Counter(health_statuses)
    labels, values = zip(*health_status_counts.items())

    plt.bar(labels, values, color='skyblue')
    plt.title('Tình trạng sức khỏe cây xanh')
    plt.xlabel('Tình trạng sức khỏe')
    plt.ylabel('Số lượng cây')
    plt.show()
