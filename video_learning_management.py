import tkinter
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import os
import openpyxl
import sqlite3


def enter_data():
    accepted = accept_var.get()
    
    if accepted == "accepted":
        
            title_name = title_name_entry.get()
            if title_name:
                kinds = kinds_combobox.get() 
                nationality = nationality_combobox.get()
                #saving course info
                viewing_status = viewing_status_var.get()
                #viewing_status = viewing_check.get()
                data_completion = data_completion_entry.get()
                
                print("title_name_entry:", title_name, "kinds_combobox: ", kinds, "nationality: ",nationality)
                print("viewing status: ",viewing_status)
                print("data_comletion: ", )
                print("-------------------------------------------------------------")
                
                #filepath = r"c:\users\pc\python_dev\video_learning_management\data.xlsx"
                filepath = tkinter.filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                if not os.path.exists(filepath):
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    heading = ["タイトル", "種類", "国籍", "視聴", "修了した日付"]
                    sheet.append(heading)
                    workbook.save(filepath)
                workbook = openpyxl.load_workbook(filepath)
                sheet = workbook.active
                sheet.append([title_name, kinds, nationality ,viewing_status, data_completion])
                workbook.save(filepath)
                
                #create table
                conn = sqlite3.connect('video.db')
                table_create_query = '''create table if not exists video_data
                (タイトル text, 種類 text, 国籍 text, 視聴 text, 修了した日付 int)'''
                
                conn.execute(table_create_query)
                
                #insert data
                data_insert_query = '''insert into video_data(タイトル, 種類, 国籍,
                視聴, 修了した日付) values(?,?,?,?,?)'''
                data_insert_tuple = (title_name, kinds, nationality, viewing_status, data_completion)
                coursor = conn.cursor()
                coursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close
                
                
            else:
                 tkinter.messagebox.showwarning(title="error", message="タイトルは必須です。")
            
    else:
        tkinter.messagebox.showwarning(title="error.", message="利用規約に同意していません")

window = tkinter.Tk()
window.title("video learning management form")

frame = tkinter.Frame(window)

#video info
video_info_frame = tkinter.LabelFrame(frame, text="video information")
video_info_frame.grid(row=0, column=0, padx=20, pady=10)
first_name_label = tkinter.Label(video_info_frame)

title_name_label = tkinter.Label(video_info_frame, text="タイトル")
title_name_label.grid(row=0, column=0)

title_name_entry = tkinter.Entry(video_info_frame)
title_name_entry.grid(row=1, column=0)

kind_label = tkinter.Label(video_info_frame, text="種類")
kinds_combobox = ttk.Combobox(video_info_frame, values=["", "youtube", "udemy"])
kind_label.grid(row=0, column=1)
kinds_combobox.grid(row=1, column=1)

nationality_label = ttk.Label(video_info_frame, text="国籍")
nationality_combobox = ttk.Combobox(video_info_frame, values=["アフリカ", "オーストラリア", "アジア","ヨーロッパ", "南アメリカ", "北アメリカ"])
nationality_label.grid(row=0, column=2)
nationality_combobox.grid(row=1, column=2)

for widget in video_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

#saving course info
course_frame = tkinter.LabelFrame(frame)
course_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

viewing_label = tkinter.Label(course_frame, text="視聴")
viewing_status_var = tkinter.StringVar(value="視聴していません")
viewing_check = tkinter.Checkbutton(course_frame, text="視聴可否", variable=viewing_status_var, onvalue="視聴", offvalue="視聴していません")
viewing_label.grid(row=0, column=0)
viewing_check.grid(row=1, column=0)

data_completion_label = tkinter.Label(course_frame, text="修了した日付")
data_completion_label.grid(row=0, column=1)
data_completion_entry = tkinter.Entry(course_frame)
data_completion_entry.grid(row=1, column=1)

#accept
accept_frame = tkinter.LabelFrame(frame, text="利用規約")
accept_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="not accepted")
accept_check = tkinter.Checkbutton(accept_frame, text="利用規約に同意しますします。", variable=accept_var, onvalue="accepted", offvalue="not accepted")
accept_check.grid(row=0, column=0)

#button
button = tkinter.Button(frame, text="登録", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)


frame.pack()

window.mainloop()
