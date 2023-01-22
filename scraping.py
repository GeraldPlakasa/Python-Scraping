import requests, re, os
from bs4 import BeautifulSoup
from tkinter import *
import pickle, codecs, nltk
# nltk.download('punkt')

struct=Tk()
struct.geometry("354x350")
struct.title("Pemrosesan Bahasa Alami")
label=Label(struct,text="Scraping Search Engine",bg="gray",fg="white",font=("Comic Sans MS",20,"bold"))
label.pack(side=TOP)
struct.config(background="gray")

text=StringVar()

def search():
    try:
        data=requests.get('https://www.google.com/search?q='+text.get())
        soup=BeautifulSoup(data.content,"html.parser") #mengubah halaman web menjadi html
        result=soup.select(".kCrYT a") #DOM span dan a

        num = 0
        for link in result:
            searching=link.get("href")
            searching=searching[7:]
            searching=searching.split("&")
            
            if not "ie=UTF-8" in searching[0]: #encoding
                print(searching[0])
                save(num,searching[0])
                num += 1
            if num == 10:
                break
    except Exception as e:
        print(e)

def save(num, head):
    data = requests.get(head)
    soup = BeautifulSoup(data.content, 'html.parser')

    filename = ('file' + str(num+1) + '.txt')
    f = open(filename, "w", encoding="utf-8")
    headers = head+"\n"+soup.get_text().replace('\n\n', ' ')
    f.write(headers)

def btnSegmentasi():
    button=Button(struct,text="Split",font=("Times",10,"bold"),width=20,bd=2, command=btnSplit)
    button.place(relx=.5, rely=.6, anchor='center')

    button=Button(struct,text="Tokenize",font=("Times",10,"bold"),width=20,bd=2, command=btnTokenize)
    button.place(relx=.5, rely=.7, anchor='center')

    button=Button(struct,text="Punkt",font=("Times",10,"bold"),width=20,bd=2, command=btnPunkt)
    button.place(relx=.5, rely=.8, anchor='center')

def btnSplit():
    print('─' * 100)
    f = open("file1.txt", "r", encoding="utf8").read().split(".")
    # menghapus nilai kosong pada list
    f = list(filter(None, f))

    try:
        f2 = open("hasil_split.txt", "x")
        f2.close()
    except Exception as e:
        os.remove("hasil_split.txt")
        f2 = open("hasil_split.txt", "x")
        f2.close()
    
    for word in f:
        # hapus mutiple space
        word = re.sub(' +', ' ', word)
        try:
            with open("hasil_split.txt", "a", encoding="utf-8") as f3:
                f3.write(word.strip()+"\n\n")
                f3.close()
        except Exception as e:
            print(e)
    print("Complete!!")
        

def btnTokenize():
    print('─' * 100)
    f = open("file1.txt", "r", encoding="utf8").read()
    teks = nltk.sent_tokenize(f)

    # menghapus nilai kosong pada list
    teks = list(filter(None, teks))

    try:
        f2 = open("hasil_tokenize.txt", "x")
        f2.close()
    except Exception as e:
        os.remove("hasil_tokenize.txt")
        f2 = open("hasil_tokenize.txt", "x")
        f2.close()

    for tokeniz in teks:
        # hapus mutiple space
        tokeniz = re.sub(' +', ' ', tokeniz)
        try:
            with open("hasil_tokenize.txt", "a", encoding="utf-8") as f3:
                f3.write(tokeniz.strip()+"\n\n")
                f3.close()
        except Exception as e:
            print(e)
    print("Complete!!")

def btnPunkt():
    print('─' * 100)
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    f = codecs.open("file1.txt", "r", "utf8").read()
    tokenizer.train(f)
    out = open("indonesian.pickle", "wb")
    pickle.dump(tokenizer, out)
    out.close()
    seg_kalimat = nltk.data.load('indonesian.pickle')
    teks = seg_kalimat.tokenize(f)

    # menghapus nilai kosong pada list
    teks = list(filter(None, teks))

    try:
        f2 = open("hasil_punkt.txt", "x")
        f2.close()
    except Exception as e:
        os.remove("hasil_punkt.txt")
        f2 = open("hasil_punkt.txt", "x")
        f2.close()

    for punktz in teks:
        # rename multiple \n to space
        punktz = punktz.replace('\n', ' ')
        # hapus mutiple space
        punktz = re.sub(' +', ' ', punktz)
        try:
            with open("hasil_punkt.txt", "a", encoding="utf-8") as f3:
                f3.write(punktz.strip()+"\n\n")
                f3.close()
        except Exception as e:
            print(e)
    print("Complete!!")

label=Label(struct,text="Enter here to search",bg="gray",fg="white",font=("Times",15,"bold"))
label.place(relx=.5, rely=.3, anchor="center")
enter=Entry(struct,font=("Times",10,"bold"),textvar=text,width=30,bd=2,bg="white")
enter.place(relx=.5, rely=.4, anchor='center')
button=Button(struct,text="Search",font=("Times",10,"bold"),width=30,bd=2,command=lambda:[search(), btnSegmentasi()] )
button.place(relx=.5, rely=.5, anchor='center')

struct.mainloop()