
import json
import os
os.environ['ARK_API_KEY'] = ''
os.environ['VOLC_ACCESSKEY']='M'
os.environ['VOLC_SECRETKEY']=''
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    region="cn-beijing"
)

def process_files(news_file_path, labels_file_path):
    news_data = []

    # 打开新闻文件和标签文件
    with open(news_file_path, 'r', encoding='utf-8') as news_file, \
            open(labels_file_path, 'r', encoding='utf-8') as labels_file:
        # 逐行读取新闻和标签
        news_lines = news_file.readlines()
        labels_lines = labels_file.readlines()

        # 假设两个文件的行数是相同的
        for news, label in zip(news_lines, labels_lines):
            # 清理每行的多余空格或换行符
            news = news.strip()
            label = label.strip()

            # 创建字典并添加到列表
            news_dict = {
                'content': news,
                'label': int(label)  # 将标签转化为整数 (0 或 1)
            }
            news_data.append(news_dict)

    return news_data



def predict_news_truthfulness(content: str):
    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20241227110458-8vkqz",
        messages = [
            {"role": "system", "content": "给定一则新闻，请你以从逻辑角度和常识角度判断该新闻是真新闻还是假新闻，"
                                      "若真新闻则输出1，假新闻则输出0，并给出相应理由。要求输出格式如下:"
                                      "\"td_rationale\": \"The message contains specific details, which add credibility.\","
                                      "td_pred\": 0,  "
                                      "cs_rationale\": \"Plausibility and source credibility are high.\","
                                       "cs_pred\": 0 "

             },
         {"role": "user", "content": content},
        ],
        extra_headers={'x-is-encrypted': 'true'},
    )

    text = '{' + completion.choices[0].message.content + '}'
    print(text)
    # 使用 json.loads 解析文本为字典
    data_dict = json.loads(text)
    return data_dict


def process_news(news_data, output_file,batch_size=500):
    result = []
    total= len(news_data)
    for index, news_item in enumerate(news_data):
        news_content = news_item["content"]  # 从news_data获取新闻内容
        label = news_item["label"]  # 获取对应的标签

        source_id = index
        if(index<2000):
            continue
        # 调用大模型来预测新闻的真假和推理
        prediction = predict_news_truthfulness(news_content)
        td_acc = 1 if prediction["td_pred"] == label else 0
        cs_acc = 1 if prediction["cs_pred"] == label else 0

        # 组织成JSON格式
        news_json = {
            "content": news_content,
            "label": label,  # 使用提供的标签
            "source_id": source_id,
            "td_rationale": prediction["td_rationale"],
            "td_pred": prediction["td_pred"],
            "td_acc": td_acc,
            "cs_rationale": prediction["cs_rationale"],
            "cs_pred": prediction["cs_pred"],
            "cs_acc": cs_acc,
            "split": "test",  # 假设数据集拆分为"test"
        }

        result.append(news_json)
        print(f'process finish: {index}/{total}')
        # 每处理完一部分新闻后就写入文件
        if (index + 1) % batch_size == 0:
            with open(output_file, 'a') as json_file:
                # 如果文件已存在，则使用追加模式
                json.dump(result, json_file, indent=4)
                json_file.write('\n')  # 在每批数据后换行
            result = []  # 清空当前批次数据，以便处理下一批

    # 处理完所有数据后再写入剩余的部分


    if result:
     with open(output_file, 'a') as json_file:
         json.dump(result, json_file, indent=4)
         json_file.write('\n')  # 在最后一批数据后换行

    print(f'Processed news saved to {output_file}')
    # 返回所有新闻的JSON列表
    return result

# 假设文件路径为 'news.txt' 和 'labels.txt'
news_file_path = "E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\gossipcop_lines.txt"
labels_file_path = "E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\gossipcop_label- 0 for fake and 1 for true.txt"

# 调用函数并获取组合好的数据
news_data = process_files(news_file_path, labels_file_path)


output_file = "E:\\2024-2025年度上学期\自然语言处理\期中展示\ARG-main\ARG-main\data\processed_news.json"
news_json_list = process_news(news_data,output_file)



