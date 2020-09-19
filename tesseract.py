import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from PIL import Image
import os
from wand.image import Image as wi
import csv
from tkinter import messagebox
import tkinter as tk
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract'
def convert(way):
    
    if not(os.path.exists('F:\python\open cv\jpegs')):
        os.mkdir('F:\python\open cv\jpegs')
        i=1
        img_dir=way
        for root,dirs,files in os.walk(img_dir):
            for file in files:
                if file.endswith(".pdf"):
                    path=os.path.join(root,file)
                    pdf=wi(filename=path,resolution=400)
                    pdfimage=pdf.convert("jpeg")
                    for imgs in pdfimage.sequence:
                        page=wi(image=imgs)
                        page.save(filename='F:\python\open cv\jpegs\conv_{}.jpg'.format(i))
                    i+=1
                    print("***proccessed****")
                else:
                    messagebox.showerror("error","{} is not PDF file".format(file))
                    
        print("=====converted=======")
    else:
        print("File already exists")
                
def grades(a,b,c,d,img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=img[a:b,c:d]
    img=cv2.resize(img,None,fx=1.0,fy=2.0)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,105,85)
    config="--psm 6"
    d=pytesseract.image_to_data(img,output_type=Output.DICT,config=config)
    
    for i in range(len(d["text"])):
        l=d["left"][i]
        t=d["top"][i]
        h=d["height"][i]
        w=d["width"][i]
        cv2.rectangle(img,(l,t),(l+w,t+h),(0,0,255),2)      
    cv2.imshow("image",img)
    
    return d["text"]
def main_code():
    
    grade=[]    
    names=[]
    credit=[]
    rno=[]
    gpa=[]
    
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    img_dir=os.path.join(BASE_DIR,"jpegs")
    for root,dirs,files in os.walk(img_dir):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                path=os.path.join(root,file)
                #print(file)
                img=cv2.imread(path)
                c=img.copy()
                name=img.copy()
                htno=img.copy()
                #Extracting grade acheived and converting them into respective points
                a=grades(1280,2090,2500,2700,img)
                for i in a:
                    if(i!=""):
                        if(i=='S'):
                            grade.append(10)
                        elif(i=='A'):
                            grade.append(9)
                        elif(i=='B'):
                            grade.append(8)
                        elif(i=='C'):
                            grade.append(7)
                        elif(i=='D'):
                            grade.append(6)
                        elif(i=='E'):
                            grade.append(5)
                        else:
                            grade.append(0)
                
                #Extracting credits from every sheet
                g=grades(1280,2090,2700,3000,c)
                for i in g:
                    if(i!=""):
                        credit.append(i)
                #Extracting name from every sheet
                x=[]
                for i in(grades(900,1000,500,2500,name)):
                    if i!="":
                        x.append(i)
                names.append(' '.join(x))
                #Extracting htno from every sheet
                for i in grades(800,900,500,1600,htno):
                    if(i!=""):
                        rno.append(i)
                #Calculating gpa and adding into gpa list
                sums=0
                total=0
                for k in credit:
                    sums+=int(k)
                for i in range(len(grade)):
                    total+=int(grade[i])*int(credit[i])
                gpa.append("{0:.2f}".format(total/sums))
                credit.clear()
                grade.clear()
                
            else:
                print("error")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    dataset=list()
    for i in range(len(names)):
        data=list()
        data.append(int(rno[i]))
        data.append(names[i])
        data.append(float(gpa[i]))
        dataset.append(data)
    print(dataset)    
    fields=["HTNO","NAME","GPA"]
    filename="gpa.csv"
    with open(filename,"w") as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(dataset)
    print("done successfully")
def main():
    root=tk.Tk()
    root.configure(bg="gray22")
    root.geometry("500x500")

    lh=tk.Label(root,text="GPA CALCULATOR", width="50",height="2", fg="black", bg="gray",font=("bold",30))
    lh.place(x=170,y=0)

    note1=tk.Label(root,text="=> Download the marks sheet from official website using print where you get pdf files downloaded." ,width="100", height="3",fg="orange red",bg="azure",anchor="w")
    note2=tk.Label(root,text="=>Screenshot Images are not allowed to be processed." ,width="100", height="3",fg="orange red",bg="azure",anchor="w")
    l1=tk.Label(root,text="PATH OF FOLDER",height="1" ,bg="gray22",fg="white" ,font=("bold",20))
    e1=tk.Entry(root,width="20",font=("italic",20),fg="blue")

    bc=tk.Button(root,text="CONVERT INTO JPEG",command=lambda:convert(str(e1.get())),width="30",height="2",bg="SkyBlue1",fg="black")
    bp=tk.Button(root,text="PROCESS",width="30",command=main_code,height="2",bg="SkyBlue1",fg="black")

    note1.place(x=100,y=200)
    note2.place(x=100,y=250)
    e1.place(x=800,y=400)
    l1.place(x=500,y=400)
    bc.place(x=690,y=500)
    bp.place(x=690,y=600)
    root.mainloop()
if __name__=="__main__":
    main()

