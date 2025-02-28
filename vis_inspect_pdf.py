from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfile
from pdf2image import convert_from_path
import os
from PIL import Image, ImageTk
import pandas as pd


class starting_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Inspection Start")
        # set dimensions
        self.root.geometry('350x100')
        # make grame for grid layout
        self.frame = Frame(self.root)
        self.frame.grid(row=1, column=0, sticky='nsew')
       
        self.e1 = Entry(self.frame)
        self.e1.grid(row=0, column=0, pady=5, padx=5)

        self.b1 = Button(self.frame, text = 'Set File Path', command = self.new_window)
        self.b1.grid(row=1,column=0, pady=5)
        self.b2=Button(self.frame,text="Browse Folders",command=self.browse)
        self.b2.grid(row=0, column=1, pady=5, padx=5)
        
    def browse(self):
        self.filepath = askdirectory()+'/'
        self.e1.delete(0, 'end')
        self.e1.insert(END, self.filepath)

    def new_window(self):
        self.filepath = self.e1.get()
        self.newWindow = Toplevel(self.root)
        vis_ins(self.newWindow, self.filepath)



class vis_ins:
    def __init__(self, root, filepath):
        self.filepath=filepath
        self.root = root
        self.root.title("[OIII] Visual Inspection")
        # set dimensions
        self.root.geometry('1300x500')

        # make frame for grid layout
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, sticky='nsew')
        # canvas with scrollbar
        self.canvas = Canvas(self.frame)
        self.scrollbar_v = Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_v.set)
        self.scrollbar_h = Scrollbar(self.frame, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar_h.set)
        
        # create frame for scroll content
        self.content_frame = Frame(self.canvas)
        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # configure resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        # pack canvas and scrollbar onto window
        self.canvas.create_window((0,0), window=self.content_frame, anchor='nw')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_v.grid(row=0, column=1, sticky='ns')
        self.scrollbar_h.grid(row=6, column=0, sticky='ew')


        # add image
        self.files = sorted(os.listdir(self.filepath))
        self.id_list = [f.split('_')[4] for f in self.files]
        self.i_list = range(len(self.files))
        
        # define dictionary to save to 
        self.ids  = [0]*len(self.files)
        self.flags= [0]*len(self.files)
        self.notes= [0]*len(self.files)
        self.redshift=[0]*len(self.files)
        
        self.i=0
        self.img1 = convert_from_path(self.filepath+str(self.files[self.i_list[self.i]]))[0]
        self.img1 = self.img1.resize((int(self.img1.width/2), int(self.img1.height/2)), Image.LANCZOS)
        # self.img1 = Image.open(self.filepath+str(self.files[self.i_list[self.i]]))
        self.img1 = ImageTk.PhotoImage(self.img1, master=self.root)
        # self.img1 = PhotoImage(self.img1.tobytes(), master=self.root)
        # self.img1.subsample((2,2), 0)
        self.imgl = Label(self.content_frame, image=self.img1)
        self.imgl.grid(row=0, column=2, columnspan=3, rowspan=4, padx=10, pady=5)


        
        # add text
        self.t1 = Label(self.content_frame, text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
        self.t1.grid(row=0, column=0)
        
        # add label2
        self.l1 = Label(self.content_frame, text = "Flags")
        self.l1.grid(row=1, column=0, pady=2)  # grid controls where lbl is -- no parameters, will be in 0,0 (top, left)
        self.l2 = Label(self.content_frame, text = "Notes")
        self.l2.grid(row=2, column=0, pady=2)
        
        self.l4 = Label(self.content_frame, text='Redshift')
        self.l4.grid(row = 3, column=0, pady=2)
        
        self.l3 = Label(self.content_frame, text = "Save Path/Name")
        self.l3.grid(row=4, column=0, pady=2)
        # add input boxes
        self.e1 = Entry(self.content_frame)
        self.e2 = Entry(self.content_frame)
        self.e1.grid(row=1, column=1, pady=2)
        self.e2.grid(row=2, column=1, pady=2)
        self.e3 = Entry(self.content_frame)
        self.e3.grid(row=4, column=1, pady=2)
        self.e4 = Entry(self.content_frame)
        self.e4.grid(row=3, column=1, pady=2)
        
        # add buttons
        self.b1 = Button(self.content_frame, text="First Image", width=20, command=self.back_pic)
        self.b1.grid(column=2, row=5, sticky='N')

        self.b2 = Button(self.content_frame, text="Next", width=20, command=self.next_pic)
        self.b2.grid(column=3, row=5, sticky='N')
        
        self.b3 = Button(self.content_frame, text="Save", command=self.save)
        self.b3.grid(column=0, row=5, padx=5)
        
        self.b4 = Button(self.content_frame,  text="Exit", command=self.exit)
        self.b4.grid(column=1, row=5, padx=5)

    def save(self):
        self.flags[self.i] = self.e1.get()
        self.notes[self.i] = self.e2.get()
        self.redshift[self.i] = self.e4.get()
        self.ids[self.i] = self.id_list[self.i_list[self.i]]
        self.info_dict = {'ID':self.ids, 'Flag':self.flags, 'Notes':self.notes, 'Redshift':self.redshift}
        self.pd_info = pd.DataFrame(self.info_dict)
        if not self.e3.get():
            self.savefilepath = asksaveasfile()
        else:
            self.savefilepath = self.e3.get()
        self.pd_info.to_csv(self.savefilepath, index=False)
    def exit(self):        
        self.flags[self.i] = self.e1.get()
        self.notes[self.i] = self.e2.get()
        self.redshift[self.i] = self.e4.get()
        self.ids[self.i] = self.id_list[self.i_list[self.i]]
        self.info_dict = {'ID':self.ids, 'Flag':self.flags, 'Notes':self.notes, 'Redshift':self.redshift}
        self.pd_info = pd.DataFrame(self.info_dict)
        if not self.e3.get():
            self.savefilepath = asksaveasfile()
        else:
            self.savefilepath = self.e3.get()
        self.pd_info.to_csv(self.savefilepath, index=False)
        self.root.destroy()
    def next_pic(self):
        # global i
        self.flags[self.i] = self.e1.get()
        self.notes[self.i] = self.e2.get()
        self.redshift[self.i] = self.e4.get()
        self.ids[self.i] = self.id_list[self.i_list[self.i]]
        if self.i==len(self.i_list)-1:
            self.b2.configure(text="Last Image")
            self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
        else:
            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            self.e4.delete(0, 'end')       
            self.i += 1
            self.new_image = convert_from_path(self.filepath+str(self.files[self.i_list[self.i]]))[0]
            self.new_image = self.new_image.resize((int(self.new_image.width/2), int(self.new_image.height/2)), Image.LANCZOS)
            self.new_image = ImageTk.PhotoImage(self.new_image, master=self.root)
            self.imgl.config(image=self.new_image)
            self.imgl.image = self.new_image
            self.b1.configure(text="Back")
            if self.i==len(self.i_list)-1:
                self.b2.configure(text="Save Last Image")
                self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
            else:
                self.b2.configure(text="Next")
                self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
    def back_pic(self):
            # global i
            if self.i==0:
                self.b1.configure(text="First Image")
            else:
                self.e1.delete(0, 'end')
                self.e2.delete(0, 'end')
                self.e4.delete(0, 'end')
                self.i -= 1
                self.new_image = convert_from_path(self.filepath+str(self.files[self.i_list[self.i]]))[0]
                self.new_image = self.new_image.resize((int(self.new_image.width/2), int(self.new_image.height/2)), Image.LANCZOS)
                self.new_image = ImageTk.PhotoImage(self.new_image, master=self.root)
                self.imgl.config(image=self.new_image)
                self.imgl.image = self.new_image
                self.b2.configure(text="Next")
                self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
                if self.i==0:
                    self.b1.configure(text="First Image")
                    self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
                else:
                    self.b1.configure(text="Back")
                    self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
        
        
def main(): 
    root = Tk()
    app = starting_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
