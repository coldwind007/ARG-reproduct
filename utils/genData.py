import json
import random
input_file="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\processed_news.json"
output_file="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\processed_news_data.json"

train_data_output="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\\en-data\\train.json"
test_data_output="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\\en-data\\test.json"
val_data_output="E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\\en-data\\val.json"


with open(input_file, 'r', encoding='utf-8') as f:
    merged_data = []  # 用来存储合并后的数据
    current_array = []  # 当前正在拼接的 JSON 数组

    for line in f:
        line = line.strip()  # 去掉每行的首尾空白字符
        if line:  # 如果该行非空
            # 拼接当前行到 current_array 中
            current_array.append(line)

            # 如果该行以 ']' 结尾，则表示当前 JSON 数组结束
            if line.endswith(']'):
                try:
                    # 尝试将拼接的 JSON 数组解析为 Python 对象
                    merged_data.extend(json.loads(''.join(current_array)))
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                # 清空当前数组准备处理下一个数组
                current_array = []

# 将合并后的数据保存到一个新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(merged_data, out_file, ensure_ascii=False, indent=2)

print(f"合并后的数据已保存到 {output_file} 文件中。")

# 打乱数据顺序
random.shuffle(merged_data)

# 计算切分的索引
total_len = len(merged_data)
train_len = int(total_len * 0.6)  # 60% 用作训练集
test_val_len = total_len - train_len  # 剩下的 40% 用作测试集和验证集
test_len = val_len = test_val_len // 2  # 40% 分成两个部分，20% 测试集，20% 验证集

# 分割数据集
train_data = merged_data[:train_len]
test_data = merged_data[train_len:train_len + test_len]
val_data = merged_data[train_len + test_len:]

# 保存到 JSON 文件
with open(train_data_output, 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=2)

with open(test_data_output, 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)

with open(val_data_output, 'w', encoding='utf-8') as f:
    json.dump(val_data, f, ensure_ascii=False, indent=2)

print("数据已按 3:1:1 的比例分割并保存为 'train.json', 'test.json', 和 'val.json'.")