import json
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score
input_file="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\\en-data\\val.json"

# 读取JSON文件，假设文件路径为 "data.json"
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取真实标签（label）和预测标签（td_pred）
true_labels = [entry['label'] for entry in data]
pred_labels = [entry['td_pred'] for entry in data]

# 确保每个标签是0或1，过滤掉其他值
valid_indices = [
    i for i in range(len(true_labels))
    if (true_labels[i] == 0 or true_labels[i] == 1) and (pred_labels[i] == 0 or pred_labels[i] == 1)
]

# 使用 valid_indices 筛选出有效的数据
true_labels_clean = [true_labels[i] for i in valid_indices]
pred_labels_clean = [pred_labels[i] for i in valid_indices]

# 计算原样本总数、真样本总数、假样本总数
total_samples = len(true_labels_clean)  # 原样本总数
true_samples = true_labels_clean.count(1)  # 真样本总数
fake_samples = true_labels_clean.count(0)  # 假样本总数

# 计算准确率
accuracy = accuracy_score(true_labels_clean, pred_labels_clean)

# 计算针对真新闻（label = 1）和假新闻（label = 0）的召回率
recall_true = recall_score(true_labels_clean, pred_labels_clean, pos_label=1)  # 针对真新闻的召回率
recall_fake = recall_score(true_labels_clean, pred_labels_clean, pos_label=0)  # 针对假新闻的召回率

# 计算针对真新闻（label = 1）和假新闻（label = 0）的F1值
f1_true = f1_score(true_labels_clean, pred_labels_clean, pos_label=1)  # 针对真新闻（label = 1）的 F1 值
f1_fake = f1_score(true_labels_clean, pred_labels_clean, pos_label=0)  # 针对假新闻（label = 0）的 F1 值

# 计算宏观F1（MACF1）
macro_f1 = f1_score(true_labels_clean, pred_labels_clean, average='macro')

# 打印结果
print(f"原样本总数: {total_samples}")
print(f"真样本总数: {true_samples}")
print(f"假样本总数: {fake_samples}")
print(f"针对真新闻 (label = 1) 的 F1值: {f1_true:.4f}")
print(f"针对假新闻 (label = 0) 的 F1值: {f1_fake:.4f}")
print(f"准确率: {accuracy:.4f}")
print(f"真新闻召回率: {recall_true:.4f}")
print(f"假新闻召回率: {recall_fake:.4f}")
print(f"宏F1 (MACF1): {macro_f1:.4f}")