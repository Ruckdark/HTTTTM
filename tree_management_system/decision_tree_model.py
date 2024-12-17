import pandas as pd
import numpy as np

class DecisionTreeClassifierCustom:
    def __init__(self):
        self.tree = {}

    def fit(self, x, y):
        data = x.copy()
        data['label'] = y
        self.tree = self._build_tree(data)

    def _entropy(self, y):
        counts = np.bincount(y)
        probabilities = counts / len(y)
        return -np.sum([p * np.log2(p) for p in probabilities if p > 0])

    def _information_gain(self, data, feature, label_entropy):
        values = data[feature].unique()
        weighted_entropy = 0
        for value in values:
            subset = data[data[feature] == value]
            subset_entropy = self._entropy(subset['label'])
            weighted_entropy += (len(subset) / len(data)) * subset_entropy
        return label_entropy - weighted_entropy

    def _best_feature(self, data):
        label_entropy = self._entropy(data['label'])
        features = data.columns[:-1]
        information_gains = [self._information_gain(data, feature, label_entropy) for feature in features]
        return features[np.argmax(information_gains)]

    def _build_tree(self, data):
        if len(data['label'].unique()) == 1:
            return data['label'].iloc[0]
        
        if len(data.columns) == 1:
            return data['label'].mode()[0]
        
        best_feature = self._best_feature(data)
        tree = {best_feature: {}}
        values = data[best_feature].unique()
        for value in values:
            subset = data[data[best_feature] == value]
            subset = subset.drop(columns=best_feature)
            subtree = self._build_tree(subset)
            tree[best_feature][value] = subtree
        return tree

    def predict(self, x):
        predictions = x.apply(self._predict_row, axis=1, tree=self.tree)
        return predictions

    def _predict_row(self, row, tree):
        if not isinstance(tree, dict):
            return tree
        feature, branches = next(iter(tree.items()))
        value = row[feature]
        if value in branches:
            return self._predict_row(row, branches[value])
        else:
            return np.nan

def train_decision_tree(data):
    df = pd.DataFrame(data)  # Chuyển dữ liệu đầu vào thành DataFrame
    if not df.empty:  # Kiểm tra xem DataFrame có rỗng hay không
        x = df[['Height', 'Diameter', 'Age']]  # Lấy các đặc điểm của cây làm biến đầu vào (features)
        y = df['HealthStatus']  # Lấy tình trạng sức khỏe cây làm biến mục tiêu (label)
        
        # Đổi tên tình trạng sức khỏe thành nhãn số (encode labels)
        y_labels, y = np.unique(y, return_inverse=True)

        # Tạo và huấn luyện mô hình cây quyết định tùy chỉnh
        clf = DecisionTreeClassifierCustom()
        clf.fit(x, y)
        
        return clf, y_labels  # Trả về mô hình đã huấn luyện và nhãn (labels)
    return None, None  # Trả về None nếu DataFrame rỗng
