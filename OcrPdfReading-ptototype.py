from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pdf2jpg import pdf2jpg
from tkinter import ttk
import os
import shutil
import pytesseract
from PIL import Image
import json
import time





root=Tk()
root.geometry('500x400+300+200')
root.title('PDF хранилище')
def askdirectory():


    try:
        q=open("data_slovar.json",'r+',encoding='UTF-8')
        data_slovar=json.load(q)
        q.close()
        q=open("data_slovar.json",'w',encoding='UTF-8')
        print ("json был , скачаны файлы,  json обнулен и создан заново")
    except FileNotFoundError:
        q=open("data_slovar.json",'w',encoding='UTF-8')
        data_slovar={}
        print ("json не было ,json создан заново")
    outputpath=''
    
        
    
    list_of_pdf_files=[]
    of=filedialog.askdirectory()
    list_of_folder = os.listdir(of)
    try:
        os.mkdir("dump_for_jpg")
    except OSError:
        print ("Директория есть?")


    for i in range(len(list_of_folder)):
        if list_of_folder[i].endswith(".pdf"):
            list_of_pdf_files.append(list_of_folder[i])
    print(list_of_pdf_files)
    print(len(list_of_pdf_files))
    

    for i in range(len(list_of_pdf_files)):
        beta_inputpath=of+"/"+list_of_pdf_files[i]
        beta_inputpath=list(beta_inputpath)
        alfa_inputpath=''
        for k in range(len(beta_inputpath)):
            if beta_inputpath[k]=='/':
                alfa_inputpath=alfa_inputpath+'//'
            else:
                alfa_inputpath+=beta_inputpath[k]
        #print(alfa_inputpath)
        outputpath=os.getcwd()+'//'+'dump_for_jpg'
        result = pdf2jpg.convert_pdf2jpg(alfa_inputpath, outputpath, pages="ALL")
        
        
    
        dir_list = os.listdir(outputpath)
        
        for i in range(len(dir_list)):
            #list_of_jpg_input_for_tesseract=os.listdir()
            path_remove = outputpath +'//'+dir_list[i]
            list_of_jpgs=os.listdir(path_remove)
            name_of_folder_with_jpg=dir_list[i]
            for l in range(len(list_of_jpgs)):
                dir_of_jpg=path_remove+'//'+list_of_jpgs[l]
                string_of_image = pytesseract.image_to_string(Image.open(dir_of_jpg), lang='rus')
                if name_of_folder_with_jpg[:-4] in data_slovar:
                    data_slovar[name_of_folder_with_jpg[:-4]]=data_slovar[name_of_folder_with_jpg[:-4]]+' '+string_of_image
                else:
                    data_slovar[name_of_folder_with_jpg[:-4]]=string_of_image
                
    #!!!!! УДАЛЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ  
            shutil.rmtree(path_remove , ignore_errors=False, onerror=None)
    #!!!!! УДАЛЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ В "PATH'

    #закрытие файла json
    
    json.dump(data_slovar,q)
    q.close()
    print("Представление окончено")

        



def askfail():
    try:
        q=open("data_slovar.json",'r+',encoding='UTF-8')
        data_slovar=json.load(q)
        q.close()
        q=open("data_slovar.json",'w',encoding='UTF-8')
        print ("json был , скачаны файлы,  json обнулен и создан заново")
    except FileNotFoundError:
        q=open("data_slovar.json",'w',encoding='UTF-8')
        data_slovar={}
        print ("json не было ,json создан заново")


    try:
        os.mkdir("dump_for_jpg")
    except OSError:
        print ("Директория есть?")
        
    #ОСНОВА ПРОГРАММЫ НАЧАЛО
    directory_of_pdf_fail=filedialog.askopenfilename()

    #l2['text']=directory_of_pdf_fail
    outputpath=os.getcwd()+'//'+'dump_for_jpg'
    result = pdf2jpg.convert_pdf2jpg(directory_of_pdf_fail, outputpath, pages="ALL")

    name_of_folder_with_jpg=os.listdir(outputpath)[0]

    if name_of_folder_with_jpg[:-4] in data_slovar:
        json.dump(data_slovar,q)
        q.close()
        to_remove=outputpath+'//'+name_of_folder_with_jpg
        shutil.rmtree(to_remove, ignore_errors=False, onerror=None)
        messagebox.showinfo("Опа-па", "PDF фаил с таким именем уже присутствует в базе данных")
        return
        
    print("А ВЫХОДА ТО НЕ БЫЛО!!!")
    folder_with_jpg=outputpath+'//'+os.listdir(outputpath)[0]
    list_of_names_jpg=os.listdir(folder_with_jpg)

    print(list_of_names_jpg)
    print(folder_with_jpg)
    for i in range(len(list_of_names_jpg)):
        input_path_of_jpg_to_ocr=folder_with_jpg+'//'+list_of_names_jpg[i]
        string_of_image = pytesseract.image_to_string(Image.open(input_path_of_jpg_to_ocr), lang='rus')

        if name_of_folder_with_jpg[:-4] in data_slovar:
            data_slovar[name_of_folder_with_jpg[:-4]]=data_slovar[name_of_folder_with_jpg[:-4]]+' '+string_of_image
        else:
            data_slovar[name_of_folder_with_jpg[:-4]]=string_of_image

    #!!!!! УДАЛЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ  
    shutil.rmtree(folder_with_jpg , ignore_errors=False, onerror=None)
    #!!!!! УДАЛЕНИЕ СОДЕРЖИМОГО ДИРЕКТОРИИ В "PATH'

    json.dump(data_slovar,q)
    q.close()
    print("Представление окончено")

def open_2_window():

    top=Toplevel()
    top.geometry('800x400+300+200')
    top.title('Поиск файлов')


    def pokaz_tablici_is_json():

        

        show = top.pack_slaves()
        show=list(show)
        #print(len(show))

        
        
        global tree

        if len(show)>3:
            tree.destroy()
        
        tree=ttk.Treeview(top)

        tree["columns"]=("one","two")
        tree.column("#0", width=270, minwidth=270)
        tree.column("one", width=150, minwidth=150)
        tree.column("two", width=450, minwidth=450)

        tree.heading("#0",text="PDF фаил")
        tree.heading("one", text="Найдено совпадений")
        tree.heading("two", text="Ссылка на документ")
        show = top.pack_slaves()
        show=list(show)
        
        tree.pack(side=TOP,fill=Y)
            
        


        str_words= e1.get()
        list_words=str_words.split()
        print(list_words)
        print(len(list_words))
        len_list_words=len(list_words)
        
        
          # Level 1
        
        try:
            q= open("data_slovar.json",'r')
            w=json.load(q)
            q.close()
        except:
            messagebox.showerror("Ошибка", "Базы Данных с PDF фаилами не найдено")

        try:
            for i in w:
                sovpadeniy=0
                    
                text_from_pdf=w[i].lower()
                for j in list_words:
                    result=text_from_pdf.find(j.lower())
                    if result!=-1:
                        sovpadeniy+=1
                #stroka_dla_tablici=str(str(sovpadeniy)+' из  '+str(len_list_words))
                #print(stroka_dla_tablici)
                #tree.insert('',3, text=str(i), values=(str(str(sovpadeniy)+'_из_'+str(len_list_words))) )
                if sovpadeniy!=0:
                    a=os.getcwd()
                    ssilka=a+'\\'+str(i)
                    tree.insert('',3, text=str(i), values=(sovpadeniy,ssilka) )
                          
        except:
             messagebox.showerror("Ошибка", "ошибка при трансфере данных")
             
                
                
        #except:
            #messagebox.showerror("Ошибка", "Ошибка Представления данных ")


        

        
        print(show)
        
        #tree.destroy()



    l4=Label(top,width=70,height=2,text='Введите ключевые слова для поиска через пробел')
    l4.pack()
    e1=Entry(top,width=70,text='Ввод')
    e1.pack()
    b4=Button(top,text='Поиск', width=60,height=2,bg='blue',fg='white',command=pokaz_tablici_is_json)
    b4.pack()

    top.grab_set()
    top.focus_set()
    top.wait_window()
    
    
    
            
        




b1=Button(root,text='выбор директории с файлами',width=30,height=3,bg='blue',fg='white',command=askdirectory)
b1.pack()

#l1=Label(root,width=40,height

l2=Label(root,width=30,height=5)
l2.pack()
b2=Button(root,text='выбор одного pdf фаила', width=30,height=3,bg='blue',fg='white',command=askfail)
b2.pack()
l3=Label(root,width=30,height=5)
l3.pack()
b3=Button(root,text='Поиск PDF фаилов', width=30,height=3,bg='blue',fg='white',command=open_2_window)
b3.pack()


root.mainloop() 


