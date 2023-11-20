# Import module  
from tkinter import *
import os
from tkinter import *
import tkinter as tk
import cv2
import os
import string
from tkinter import filedialog
from PIL import Image
from PIL import Image, ImageTk

def resize_image(event):
    
    window_width = event.width
    window_height = event.height

    
    resized_image = original_image.resize((window_width, window_height), Image.ANTIALIAS)
    
    tk_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(image_id, image=tk_image)
    canvas.image = tk_image  
    
root = Tk()
 

root.title("Image Stenogrophy")

root.geometry('700x700')



original_image = Image.open("C:\\Users\\ushah\\Downloads\\background.jpg")  


tk_image = ImageTk.PhotoImage(original_image)


canvas = tk.Canvas(root, width=tk_image.width(), height=tk_image.height())
canvas.pack(fill=tk.BOTH, expand=True)


image_id = canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)


canvas.bind("<Configure>", resize_image)



lbl = Label(root, text = "Image Stenography",fg="white",bg = "#1A1919", font=('Times 24'))
lbl.place(x=200,y=10)
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        cover_img_entry.delete(0, tk.END)  
        cover_img_entry.insert(0, file_path)  


def generateData(data):

		
		d = []

		for i in data:
			d.append(format(ord(i), '08b'))
		print("NEW ",d)
		return d


def modifyPixcel(pix, data):
	data = generateData(data)
	n = len(data)
	imagedata = iter(pix)
	for i in range(n):

		
		pixcel = [value for value in imagedata.__next__()[:3] +
								imagedata.__next__()[:3] +
								imagedata.__next__()[:3]]
		
		for j in range(0, 8):
			if (data[i][j] == '0' and pixcel[j]% 2 != 0):
				pixcel[j] -= 1

			elif (data[i][j] == '1' and pixcel[j] % 2 == 0):
				if(pixcel[j] != 0):
					pixcel[j] -= 1
				else:
					pixcel[j] += 1	
		if (i == n - 1):
			if (pixcel[-1] % 2 == 0):
				if(pixcel[-1] != 0):
					pixcel[-1] -= 1
				else:
					pixcel[-1] += 1

		else:
			if (pixcel[-1] % 2 != 0):
				pixcel[-1] -= 1

		pixcel = tuple(pixcel)
		yield pixcel[0:3]
		yield pixcel[3:6]
		yield pixcel[6:9]

def encode_info(nimg, data):
	w = nimg.size[0]
	(x, y) = (0, 0)

	for pixel in modifyPixcel(nimg.getdata(), data):


		nimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1


def encode():
    global new_img_name,password,msg,img

    img=str(cover_img_entry.get())
    print(img)
    imagefile = Image.open(img, 'r')
    
    data=sname_entry.get()
    
    if (len(data) == 0):
            raise ValueError('Data is empty')
   
    nimg = imagefile.copy()
    encode_info(nimg, data)
    original_folder = os.path.dirname(img)
    
    
    new_img_name=new_img_entry.get()
    
    new_path = os.path.join(original_folder, new_img_name)
  
    msg=sname_entry.get()

    
    i=cover_img_entry.get()
    password=passw_entry.get()
    img = cv2.imread(i)
    op=op_stego_entry.get()
    message_label.config(text="Stego Image is stored in \Python38\ " + new_img_name)
    nimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    os.system("start "+new_img_name)
  
    
def sub():
    global pas_entry,decrypt_label,stego_entry,decrypt_file_label 
    aa = Tk()
    
    aa.title("Image Stenogrophy")
    
    aa.geometry('700x500')
    
    aa.configure(bg="#1A1919")
    lbb = Label(aa, text = "Image Stenographyy", fg="white",bg = "#1A1919", font=('Times 24'))
    lbb.place(x=200,y=10)
    stego_label = tk.Label(aa, text = 'Image File Name',fg="white",bg = "#1A1919", font=('Times',19, 'bold'))
    stego_entry = tk.Entry(aa, font=('Times',19,'normal'))
    pas_label = tk.Label(aa, text = 'Password', fg="white",bg = "#1A1919", font =('Times',19, 'bold'))
    pas_entry=tk.Entry(aa, font = ('Times',19,'normal'), show = '*')
    

    stego_label.place(x=90,y=90)
    stego_entry.place(x=320,y=90)
    stego_entry.configure(bd=5)
    pas_entry.configure(bd=5)
    pas_label.place(x=90,y=160)
    pas_entry.place(x=320,y=160)
    extract_data=tk.Button(aa,text = 'Extract Data',fg="white",bg = "#1A1919",font =('Times',10, 'bold'),  
                activebackground='gray',height=2,width=10,command=decode)
    extract_data.place(x=330,y=300)
    decrypt_label = tk.Label(aa, text="",fg="white",bg = "#1A1919", pady=10, font=('Times',15,'normal'))
    decrypt_label.pack(side="bottom")
    decrypt_file_label = tk.Label(aa, text="", pady=20,fg="white",bg = "#1A1919", font=('Times',15,'normal'))
    decrypt_file_label.pack(side="bottom")




def decode():
    img = stego_entry.get()
    image = Image.open(img, 'r')
    pas=pas_entry.get()   
    data = ''
    original_img=new_img_entry.get()
    imginfo = iter(image.getdata())
    if(original_img==img):
        if(password == pas):
            while (True):
                pix = [x for x in imginfo.__next__()[:3] +
                                                            imginfo.__next__()[:3] +
                                                            imginfo.__next__()[:3]]
                binstr = ''
                for i in pix[:8]:
                        if (i % 2 == 0):
                                binstr += '0'
                        else:
                                binstr += '1'
                data += chr(int(binstr, 2))
                if (pix[-1] % 2 != 0):
                    print(data)
                    decrypt_label.config(text="")
                    decrypt_label.config(text="Decryption message: "+data)
                    break
        else:
            decrypt_label.config(text="")
            decrypt_label.config(text="Not valid key")
            print("Not valid key")
            
    else:
        decrypt_label.config(text="")
        decrypt_file_label.config(text="Not Valid File Location")
        print("Not valid")




sname_label = tk.Label(root, text = 'Text Message',fg="white",bg = "#1A1919", font=('Times',19, 'bold'))
sname_entry = tk.Entry(root, font=('Times',19,'normal'))

cover_img = tk.Label(root, text = 'Image File Location',fg="white",bg = "#1A1919", font=('Times',19, 'bold'))
cover_img_entry = tk.Entry(root,font=('Times',19,'normal'))

op_stego = tk.Label(root, text = 'Output File',fg="white",bg = "#1A1919", font=('Times',19, 'bold'))
op_stego_entry = tk.Entry(root, font=('Times',19,'normal'))


browse_button = tk.Button(root, text="^", height=2,fg="white",bg = "#1A1919", command=browse_file)
browse_button.place(x=590,y=160)

new_img = tk.Label(root, text = 'New Image Name',fg="white",bg = "#1A1919", font=('Times',19, 'bold'))
new_img_entry = tk.Entry(root,font=('Times',19,'normal'))

passw_label = tk.Label(root, text = 'Password',fg="white",bg = "#1A1919", font =('Times',19, 'bold'))
passw_entry=tk.Entry(root, font = ('Times',19,'normal'), show = '*')

message_label = tk.Label(root, text="",fg="white",bg = "#1A1919", pady=10, font=('Times',15,'normal'))
message_label.pack(side="bottom")

sname_label.place(x=90,y=90)


sname_entry.place(x=330,y=90)

sname_entry.configure(bd=5)
passw_entry.configure(bd=5)
cover_img_entry.configure(bd=5)

cover_img.place(x=90,y=160)
cover_img_entry.place(x=330,y=160)
passw_label.place(x=90,y=240)

passw_entry.place(x=330,y=240)
new_img.place(x=90,y=320)
new_img_entry.place(x=330,y=320)

Hide_btn=tk.Button(root,text = 'Hide Data',fg="white",bg = "#1A1919",font =('Times',10, 'bold'),  
                activebackground='white',height=2,width=15, command = encode)
extract_btn=tk.Button(root,text = 'Extract Data',fg="white",bg = "#1A1919",font =('Times',10, 'bold'),  
                activebackground='white',height=2,width=15,command=sub)


Hide_btn.place(x=250,y=400)

extract_btn.place(x=250,y=480)

root.mainloop()
 
