import tkinter as tk

def delete_item():
    selected_item = listbox.curselection()  # 获取用户选择的项目的索引
    if selected_item:
        index = selected_item[0]  # 获取第一个选定项目的索引
        listbox.delete(index)  # 删除选定的项目

def clear_item():
    listbox.delete(0, tk.END) 
    input_textbox3.delete(0, tk.END)

def check_duplicate(item):
    for i in range(listbox.size()):
        if listbox.get(i) == item:
            return True
    return False

def show_warning(title, message):
    warning_window = tk.Toplevel()
    warning_window.title(title)
    warning_window.iconbitmap('misc/favicon.ico')  # 设置图标
    warning_window.geometry('300x100')  # 设置弹窗大小
    warning_label = tk.Label(warning_window, text="⚠️ " + message, font=("Arial", 10))  # 添加 emoji 图标和调整字体大小
    warning_label.pack(padx=10, pady=10)
    return_button = tk.Button(warning_window, text="返回", command=warning_window.destroy)
    return_button.pack(pady=10)

def process_input(text1, text2):
    if len(text1) == 1 and text1.isupper():  # 检查第一个输入框的内容是否为长度为1的大写字母
        item = f"{text1} -> {text2}"
        return item
    else:
        show_warning("警告", "请输入上下文无关文法")
        return None

def add_item():
    input_text1 = input_textbox1.get()
    input_text2 = input_textbox2.get()
    if input_text1 and input_text2:  # 检查输入框是否为空
        item = process_input(input_text1, input_text2)
        if item and not check_duplicate(item):
            listbox.insert("end", item)
        elif item:
            show_warning("警告", "要添加的内容已存在")
    else:
        show_warning("警告", "添加内容不能为空")

def edit_item():
    selected_item = listbox.curselection()  # 获取用户选择的项目的索引
    if selected_item:
        index = selected_item[0]  # 获取第一个选定项目的索引
        new_text1 = input_textbox1.get()
        new_text2 = input_textbox2.get()
        if new_text1 and new_text2:  # 检查输入框是否为空
            item = process_input(new_text1, new_text2)
            if item and not check_duplicate(item):
                listbox.delete(index)
                listbox.insert(index, item)
            elif item:
                show_warning("警告", "要修改的内容已存在")
        else:
            show_warning("警告", "修改内容不能为空")

def ll1_item():
    listbox.delete(0, tk.END) 
    sample_data = [('S -> TE'),('E -> +S|ε'),('T -> FU'),('U -> T|ε'),('F -> PG'),('G -> *G|ε'),('P -> (S)|a|b|∧')]
    for item in sample_data:
        listbox.insert(tk.END, item)  
    input_textbox3.delete(0, tk.END) 
    input_textbox3.insert(tk.END, "a*b+(∧)")  

def nll1_item():
    listbox.delete(0, tk.END) 
    sample_data = ["S -> a|∧|(T)", "T -> T,S|S"]
    for item in sample_data:
        listbox.insert(tk.END, item)  
    input_textbox3.delete(0, tk.END) 
    input_textbox3.insert(tk.END, "(a,∧)")  

from tkinter import filedialog
def import_file():
    listbox.delete(0, tk.END) 
    input_textbox3.delete(0, tk.END)
    file_path = filedialog.askopenfilename()  # 弹出选择文件目录窗口
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(" -> ")
                if len(parts) == 2 and process_input(parts[0], parts[1]):
                    listbox.insert(tk.END, line.strip())  # 添加符合规则的行到listbox中

def create_gui():
    # 创建主窗口
    root = tk.Tk()
    root.title("自顶向下语法分析程序")
    root.iconbitmap('misc/favicon.ico')
    root.resizable(False, False)

    # row=0 && row=1 标题及小字
    title_label = tk.Label(root, text="实验三：自顶向下语法分析程序", font=("华文中宋", 15))
    title_label.grid(row=0, column=0, columnspan=7, padx=10, pady=3)
    github_label = tk.Label(root, text="https://github.com/CUCPTT/test3", font=("Arial", 8))
    github_label.grid(row=1, column=0, columnspan=7, padx=10, pady=3, sticky="nsew")

    # row=2 添加列表输入框
    global input_textbox1
    input_textbox1 = tk.Entry(root, width=15)
    input_textbox1.grid(row=2, column=0, padx=10, pady=10)
    arrow_label = tk.Label(root, text="->")
    arrow_label.grid(row=2, column=1, padx=1, pady=10)
    global input_textbox2
    input_textbox2 = tk.Entry(root, width=18)
    input_textbox2.grid(row=2, column=2, padx=1, pady=10)
    add_button = tk.Button(root, text="添加", command=add_item)
    add_button.grid(row=2, column=3, padx=1, pady=10, sticky="w")
    edit_button = tk.Button(root, text="修改", command=edit_item)
    edit_button.grid(row=2, column=4, padx=1, pady=10, sticky="w")
    delete_button = tk.Button(root, text="删除", command=delete_item)
    delete_button.grid(row=2, column=5, padx=1, pady=10, sticky="w")
    clear_button = tk.Button(root, text="清空", command=clear_item)
    clear_button.grid(row=2, column=6, padx=1, pady=10, sticky="w")

    # row=3 4 5 6 列表展示
    global listbox
    listbox = tk.Listbox(root, height=10, width=40)
    listbox.grid(row=3, rowspan=4, column=0, columnspan=3, padx=10, pady=10)
    nll1_button = tk.Button(root, text="非LL(1)文法样例", command=nll1_item, width=18)
    nll1_button.grid(row=3, column=3, columnspan=4,padx=1, pady=1)
    ll1_button = tk.Button(root, text="LL(1)文法样例", command=ll1_item, width=18)
    ll1_button.grid(row=4, column=3, columnspan=4,padx=1, pady=1, sticky="n")
    load_button = tk.Button(root, text="导入", command=import_file, width=10)
    load_button.grid(row=5, column=3, columnspan=4,padx=1, sticky="s")

    # row=7 
    submit_button = tk.Button(root, text="提交", command=submit, width=10, bg="light blue")
    submit_button.grid(row=7, column=3, columnspan=4, padx=1, pady=5, sticky="s")
    string_label = tk.Label(root, text="请输入预测分析串：")
    string_label.grid(row=7, column=0, columnspan=2, padx=1, pady=10, sticky="e")
    global input_textbox3
    input_textbox3 = tk.Entry(root, width=20)
    input_textbox3.grid(row=7, column=2, padx=5, pady=10, sticky="e")

    # 运行主循环
    root.mainloop()

def submit():
    if listbox.size() == 0 or len(input_textbox3.get()) == 0:
        show_warning("警告", "提交内容不能为空")
    else:
        rules = [listbox.get(i) for i in range(listbox.size())]
        grammar = [tuple(rule.split(' -> ')) for rule in rules]
        print("input_grammar: ",grammar)
        print("prediction_string: ",input_textbox3.get())

if __name__ == "__main__":
    create_gui()