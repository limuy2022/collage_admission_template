import csv
import os

mottos = {
    '清华大学': ("校训", '自强不息，厚德载物'),
    '北京大学': ("北大精神", '兼容并包，思想自由'),
    '复旦大学': ('校训', '博学而笃志，切问而近思'),
    '上海交通大学': ('校训', '饮水思源，爱国荣校'),
    '浙江大学': ('校训', '求是创新'),
    '南京大学': ("校训", '诚朴雄伟，励学敦行'),
    '北京航空航天大学': ("校训", '德才兼备、知行合一'),
    '香港科技大学': ("核心价值", '追求卓越、坚守诚信、维护学术自由'),
    '中国科学技术大学': ('校训', '理实交融，红专并进'),
    '华中科技大学': ('校训','明德厚学、求是创新'),
}

def get_university_logo(university_name):
    # 支持多种图片格式查找
    extensions = ['.png', '.jpg', '.jpeg', '.svg']
    for ext in extensions:
        path = f"icons/{university_name}{ext}"
        if os.path.exists(path):
            return path
    return "icons/default_university.png"  # 默认校徽

def generate_admission_letters():
    # 创建输出目录
    os.makedirs('admission_letters', exist_ok=True)
    
    # 读取模板文件
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 读取学生数据
    with open('目标大学.csv', 'r', encoding='utf-8') as csvfile:
        students = csv.DictReader(csvfile)
        for student in students:
            try:
                from pypinyin import pinyin, Style
                pinyin_list = pinyin(student['姓名'], style=Style.NORMAL)
                pinyin_name = '_'.join([item[0] for item in pinyin_list]).lower()
                # 生成唯一文件名
                filename = f"{pinyin_name}.html"
                
                # 准备模板数据
                issue_date = '2026 年 8 月 1 日'
                
                
                motto = mottos[student['目标大学']]
                content = template.replace(r'{student_name}', student['姓名'])\
                .replace(r'{university_name}', student['目标大学'])\
                .replace(r'{issue_date}', issue_date)\
                .replace(r'{stamp_image}', f'icons/{student['目标大学']}.png')\
                    .replace(r'{university_logo}', get_university_logo(student['目标大学']))\
                    .replace(r'{background}', student.get('background', 'images/blue_bg.jpg'))\
                             .replace(r'{university_motto}', motto[1])\
                             .replace(r'{tip_header}', motto[0])

                
                # 保存生成的文件
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"生成{student.get('姓名','未知')}的通知书时出错：[{type(e).__name__}] {str(e)}\n数据记录：{dict(student)}")

if __name__ == "__main__":
    generate_admission_letters()
    print("录取通知书生成完成，请查看 admission_letters 目录")
