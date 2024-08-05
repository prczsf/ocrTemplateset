from lineless_table_rec import LinelessTableRecognition
from wired_table_rec import WiredTableRecognition
from markdownify import markdownify as md
def get_LinelessTable_str(img_path):
    table_rec = LinelessTableRecognition()
    table_str, elapse = table_rec(img_path)
    return table_str, elapse

def get_WiredTable_str(img_path):
    table_rec = WiredTableRecognition()
    table_str, elapse = table_rec(img_path)
    return table_str, elapse


if __name__ == "__main__":
    print("LinelessTableRecognition")
    print("WiredTableRecognition")

    # img_path = "2liness.png"
    # table_str, elapse = get_LinelessTable_str(img_path)
    # print(table_str)
    # # 将 HTML 转换为 Markdown
    # markdown_str = md(table_str)
    # # 保存为 Markdown 文件
    # markdownFileName = img_path.rsplit('.', 1)[0] + ".md"
    # with open(markdownFileName, "w", encoding="utf-8") as f:
    #     f.write(markdown_str)
    # print(markdown_str)
    # print(elapse)
