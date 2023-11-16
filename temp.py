import tkinter as tk
from tkinter import ttk

def create_table():
    # 创建主窗口
    root = tk.Tk()
    root.title("预测分析表示例")
    
    # 创建标题标签
    title_label = tk.Label(root, text="预测分析表示例", font=("Arial", 12))
    title_label.pack(pady=10)
    
    # 创建表格
    table = ttk.Treeview(root)
    table["columns"] = ("Steps", "AnalyzeStack", "RemainingInputString","ProductionOrMatch")
    
    # 设置列宽
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Steps", width=100)
    table.column("AnalyzeStack", width=100)
    table.column("RemainingInputString", width=100)
    table.column("ProductionOrMatch", width=150)
    
    # 设置列标题
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Steps", text="步骤")
    table.heading("AnalyzeStack", text="分析栈")
    table.heading("RemainingInputString", text="剩余输入串")
    table.heading("ProductionOrMatch", text="推导所用产生式或匹配")
    
    # 添加数据
    table.insert("", tk.END, text="1", values=("1", '#S', "i+i*i#",'S -> TE'))
    table.insert("", tk.END, text="2", values=("2", '#ET', "i+i*i#",'T -> FU'))
    table.insert("", tk.END, text="3", values=("3", '#ETF', "i+i*i#",'F -> i'))
    
    # 显示表格
    table.pack()
    
    # 运行主循环
    root.mainloop()

# 调用函数创建表格
create_table()