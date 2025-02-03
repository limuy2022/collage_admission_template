import csv
import qrcode
import os
from pathlib import Path

# 配置参数
CSV_FILE = "目标大学.csv"
QRCODE_DIR = "pic"
BASE_URL = "https://collageadmission.limuy.top/{pinyin}.html"
QRCODE_SIZE = 10  # 二维码尺寸级别 (1-40)
QRCODE_BORDER = 2  # 二维码白边尺寸
QRCODE_VERSION = 15  # 二维码版本 (1-40)


def generate_qrcodes():
    # 创建输出目录
    Path(QRCODE_DIR).mkdir(parents=True, exist_ok=True)

    # 读取学生数据
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # 获取学生信息并生成拼音
                chinese_name = row["姓名"]
                from pypinyin import pinyin, Style

                pinyin_list = pinyin(chinese_name, style=Style.NORMAL)
                pinyin_name = "_".join([item[0] for item in pinyin_list]).lower()

                # 生成二维码内容
                url = BASE_URL.format(pinyin=pinyin_name)

                # 创建二维码对象
                qr = qrcode.QRCode(
                    version=QRCODE_VERSION,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=QRCODE_SIZE,
                    border=QRCODE_BORDER,
                )
                qr.add_data(url)
                qr.make(fit=True)

                # 生成并保存二维码图片
                img = qr.make_image(fill_color="black", back_color="white")
                output_path = os.path.join(QRCODE_DIR, f"{chinese_name}_qrcode.png")
                img.save(output_path)

                print(f"已生成 {chinese_name} 的二维码: {output_path}")

            except Exception as e:
                print(f"处理 {row.get('姓名', '未知')} 时出错: {str(e)}")


if __name__ == "__main__":
    generate_qrcodes()
