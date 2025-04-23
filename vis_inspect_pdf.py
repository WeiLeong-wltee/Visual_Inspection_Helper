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
        self.root.geometry('1000x300')
        # make grame for grid layout
        self.frame = Frame(self.root)
        self.frame.grid(row=1, column=0, sticky='nsew')
       
        self.e1 = Entry(self.frame)
        self.e1.grid(row=0, column=0, pady=5, padx=5)

        ### Modified ###
        self.b1 = Button(self.frame, text = 'Set File Path', command = self.new_window)
        self.b1.grid(row=3,column=0, pady=5)
        self.b2 = Button(self.frame,text="Browse Data Folders",command=self.browse_data)
        self.b2.grid(row=0, column=1, pady=5, padx=5)
        ### Modified ###
        
        ### Added ###
        self.e3 = Entry(self.frame)
        self.e3.grid(row=1, column=0, pady=5, padx=5)
        self.b3 = Button(self.frame,text="Browse Result Folders",command=self.browse_res)
        self.b3.grid(row=1, column=1, pady=5, padx=5)
        self.l3 = Label(self.frame, text="VI Result File Name, default with .csv suffix")
        self.l3.grid(row=2, column=0, pady=5)
        self.filename_entry = Entry(self.frame)
        self.filename_entry.grid(row=2, column=1, padx=5, pady=5)
        ### Added ###

    ### Modified ###
    def browse_data(self):
        self.filepath = askdirectory()+'/'
        self.e1.delete(0, 'end')
        self.e1.insert(END, self.filepath)
    ### Modified ###

    ### Added ###
    def browse_res(self):
        self.filepath = askdirectory()+'/'
        self.e3.delete(0, 'end')
        self.e3.insert(END, self.filepath)
    ### Added ###
        
    ### Modified ###
    def new_window(self):
        self.filepath = self.e1.get()
        self.savedfilename = self.e3.get()+self.filename_entry.get()
        self.newWindow = Toplevel(self.root)
        vis_ins(self.newWindow, self.filepath, self.savedfilename)
    ### Modified ###


class vis_ins:
    def __init__(self, root, filepath, savedfilename): ### Modified ###
        self.filepath=filepath
        self.root = root
        self.savedfilename = savedfilename ### Added ###
        self.root.title("[OIII] Visual Inspection")
        # set dimensions
        self.root.geometry('2100x900')

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
        self.files = sorted([i for i in os.listdir(self.filepath) if i.split('.')[-1] in ['png','pdf','jpg','tiff','jpeg']]) ### Modified ###
        self.id_list = ['ID'+f.split('ID')[1].split('_')[0] for f in self.files] ### Modified ###
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
        
        # self.l3 = Label(self.content_frame, text = "Save Path/Name") ### Modified ###
        # self.l3.grid(row=4, column=0, pady=2) ### Modified ###
        # add input boxes
        self.e1 = Entry(self.content_frame)
        self.e2 = Entry(self.content_frame)
        self.e1.grid(row=1, column=1, pady=2)
        self.e2.grid(row=2, column=1, pady=2)
        self.e3 = Entry(self.content_frame) ### changed to ID input
        self.e3.grid(row=5, column=0, pady=2) ### hanged to ID input
        self.e4 = Entry(self.content_frame) 
        self.e4.grid(row=3, column=1, pady=2)
        
        # add buttons
        self.b1 = Button(self.content_frame, text="First Image", width=20, command=self.back_pic)
        self.b1.grid(column=2, row=5, sticky='N')

        self.b2 = Button(self.content_frame, text="Next", width=20, command=self.next_pic)
        self.b2.grid(column=3, row=5, sticky='N')
        
        self.b3 = Button(self.content_frame, text="Jump", command=self.jump_pic) ### changed to ID jump
        self.b3.grid(column=1, row=5, padx=5) ### changed to ID jump
        
        #self.b4 = Button(self.content_frame,  text="Exit", command=self.exit)
        #self.b4.grid(column=1, row=5, padx=5)

        ### Added ####
        # Instead of hardcoded 'autosave_comments.csv'
        self.comment_data_path = os.path.join(self.savedfilename + ".csv")
        self.comment_df = self.load_existing_comments()
        self.load_current_comments()
        ### Added ####

    ### >>> ADDED: Load existing comments from CSV if it exists
    def load_existing_comments(self):
        if os.path.exists(self.comment_data_path):
            return pd.read_csv(self.comment_data_path, dtype=str).fillna('')
        else:
            return pd.DataFrame(columns=["ID", "Flag", "Notes", "Redshift"])
    ### >>> ADDED: Load existing comments from CSV if it exists

    ### >>> ADDED: Save current comment to DataFrame and file
    def autosave_current_comment(self):
        current_id = self.id_list[self.i_list[self.i]]
        new_data = {
            "ID": current_id,
            "Flag": self.e1.get(),
            "Notes": self.e2.get(),
            "Redshift": self.e4.get()
        }

        # Remove existing entry if exists
        self.comment_df = self.comment_df[self.comment_df["ID"] != current_id]
        self.comment_df = pd.concat([self.comment_df, pd.DataFrame([new_data])], ignore_index=True)
        self.comment_df.to_csv(self.comment_data_path, index=False)
    ### >>> ADDED: Save current comment to DataFrame and file

    ### >>> ADDED: Load comment from self.comment_df if available
    def load_current_comments(self):
        current_id = self.id_list[self.i_list[self.i]]
        row = self.comment_df[self.comment_df["ID"] == current_id]
        if not row.empty:
            self.e1.delete(0, 'end')
            self.e1.insert(0, row.iloc[0]["Flag"])
            self.e2.delete(0, 'end')
            self.e2.insert(0, row.iloc[0]["Notes"])
            self.e4.delete(0, 'end')
            self.e4.insert(0, row.iloc[0]["Redshift"])
        else:
            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            self.e4.delete(0, 'end')
    ### >>> ADDED: Load comment from self.comment_df if available

    ### >>> No longer needed due to WLT autosave functions
    # def save(self):
    #     self.flags[self.i] = self.e1.get()
    #     self.notes[self.i] = self.e2.get()
    #     self.redshift[self.i] = self.e4.get()
    #     self.ids[self.i] = self.id_list[self.i_list[self.i]]
    #     self.info_dict = {'ID':self.ids, 'Flag':self.flags, 'Notes':self.notes, 'Redshift':self.redshift}
    #     self.pd_info = pd.DataFrame(self.info_dict)
    #     if not self.e3.get():
    #         self.savefilepath = asksaveasfile()
    #     else:
    #         self.savefilepath = self.e3.get()
    #     self.pd_info.to_csv(self.savefilepath, index=False)
    # def exit(self):        
    #     self.flags[self.i] = self.e1.get()
    #     self.notes[self.i] = self.e2.get()
    #     self.redshift[self.i] = self.e4.get()
    #     self.ids[self.i] = self.id_list[self.i_list[self.i]]
    #     self.info_dict = {'ID':self.ids, 'Flag':self.flags, 'Notes':self.notes, 'Redshift':self.redshift}
    #     self.pd_info = pd.DataFrame(self.info_dict)
    #     if not self.e3.get():
    #         self.savefilepath = asksaveasfile()
    #     else:
    #         self.savefilepath = self.e3.get()
    #     self.pd_info.to_csv(self.savefilepath, index=False)
    #     self.root.destroy()


    def next_pic(self):
        self.flags[self.i] = self.e1.get()
        self.notes[self.i] = self.e2.get()
        self.redshift[self.i] = self.e4.get()
        self.ids[self.i] = self.id_list[self.i_list[self.i]]
        self.e3.delete(0, 'end')
        ##### Added ####
        self.autosave_current_comment()  # <-- Save before switching
        ##### Added ####
        if self.i==len(self.i_list)-1:
            self.b2.configure(text="Last Image")
            self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
            ##### Added ####
            self.load_current_comments()  # <-- Load saved comment if exists
            ##### Added ####
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
            ##### Added ####
            self.load_current_comments()  # <-- Load saved comment if exists
            ##### Added ####

    def jump_pic(self):
            self.autosave_current_comment()
            
            if self.e3.get() in self.id_list:
                self.i = [i for i, x in enumerate(self.id_list) if x == self.e3.get()][0]#np.argwhere(self.id_list == self.e3.get())
                self.e3.delete(0, 'end')

                if self.i==len(self.i_list)-1:
                    self.b2.configure(text="Last Image")
                    self.b1.configure(text="Back")
                elif self.i==0:
                    self.b1.configure(text="First Image")
                    self.b2.configure(text="Next")
                else:
                    self.b2.configure(text="Next")
                    self.b1.configure(text="Back")

                self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
                self.e1.delete(0, 'end')
                self.e2.delete(0, 'end')
                self.e4.delete(0, 'end')
                self.load_current_comments()  # <-- Load saved comment if exists
                self.new_image = convert_from_path(self.filepath+str(self.files[self.i_list[self.i]]))[0]
                self.new_image = self.new_image.resize((int(self.new_image.width/2), int(self.new_image.height/2)), Image.LANCZOS)
                self.new_image = ImageTk.PhotoImage(self.new_image, master=self.root)
                self.imgl.config(image=self.new_image)
                self.imgl.image = self.new_image
            else:
                self.e3.delete(0, 'end')
                self.e3.insert(0, 'Invalid ID')

    def back_pic(self):
        ##### Added ####
        self.autosave_current_comment()  # <-- Save before switching
        ##### Added ####
        self.e3.delete(0, 'end')
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
                ##### Added ####
                self.load_current_comments()  # <-- Load saved comment if exists
                ##### Added ####
            else:
                self.b1.configure(text="Back")
                self.t1.configure(text=f"Source ID: {self.id_list[self.i_list[self.i]]}")
                ##### Added ####
                self.load_current_comments()  # <-- Load saved comment if exists
                ##### Added ####
        
        
def main(): 
    root = Tk()
    app = starting_window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
