import csv
import os

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
                # 生成唯一文件名
                filename = f"admission_letters/{student['姓名']}_{student['目标大学']}_录取通知书.html"
                
                # 准备模板数据
                issue_date = '2026 年 8 月 1 日'
                
                
                # 转义模板中的百分号和大括号
                content = template.replace(r'{student_name}', student['姓名'])\
                .replace(r'{university_name}', student['目标大学'])\
                .replace(r'{issue_date}', issue_date)\
                .replace(r'{stamp_image}', f'icons/{student['目标大学']}.png')\
                    .replace(r'{university_logo}', get_university_logo(student['目标大学']))\
                    .replace(r'{background}', student.get('background', 'images/blue_bg.jpg'))\
                             .replace(r'{university_motto}', student.get('校训', '博学而笃志 切问而近思'))
                
                # 保存生成的文件
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            except Exception as e:
                print(f"生成{student.get('姓名','未知')}的通知书时出错：[{type(e).__name__}] {str(e)}\n数据记录：{dict(student)}")

if __name__ == "__main__":
    generate_admission_letters()
    print("录取通知书生成完成，请查看 admission_letters 目录")
