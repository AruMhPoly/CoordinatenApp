#In[]

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import ImageTk, Image
from Coordinaten import ArcGIS

#In[]: 


window = tk.Tk()

# window.geometry("550x300+300+150")
# window.resizable(width=True, height=True)

class Vista:

    def __init__(self, window):
        

        self.Project_Number = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        

        # Welcome Frame

        welcome_frame = tk.LabelFrame(window, text="Coördinaten uit ArcGIS Online", relief=tk.RIDGE, padx=5, pady=5)
        welcome_frame.grid(row=1, column=0,pady=7,columnspan = 3)
        welcome_frame.grid(sticky=tk.E + tk.W + tk.N + tk.S)

        # Imagen Escuela

        image1 = Image.open(f"C:\Python\Coordinaten_App\Logo\Logo.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.grid(row=0, column=0,columnspan = 3)
        label1.image = test

        # Texto de bievenida

        window.title("Coördinaten uit ArcGIS Online")
        lbl_welcome = Label(welcome_frame,
                            text="Hoi! Wat is jouw projectnummer?")
        lbl_welcome.pack()

        # Frame Buttom search
        global buttons_frame
        buttons_frame = tk.LabelFrame(window, text="Project gegevens", relief=tk.RIDGE)
        buttons_frame.grid(row=2, sticky="nsew",pady = 5)

        # Frame Créditos

        credit_frame = tk.LabelFrame(window,
                                            text="Contact persoon", relief=tk.RIDGE)
        credit_frame.grid(row=6, sticky="nsew", pady=5)
        # Texto de Créditos

        Label(credit_frame,text="Gecrëerd door: MH Poly").grid(row=0, sticky="nsew", pady=2)
        Label(credit_frame, text="E-mail: aru@mhpoly.com").grid(row=1, sticky="nsew", pady=2)
        Label(credit_frame, text="Telefoon nummer: +31 (0)164 245 566").grid(row=2, sticky="nsew", pady=2)

        #Coordinates button

        Get_Coordinates_Button = tk.Button(buttons_frame,text = "Raadplegen"
                                        ,command = self.Coordinaten)
        Get_Coordinates_Button.grid(row=1,column=0, padx=10,pady=10)

        #Field number of project

        Label(buttons_frame,
              text="Projectnummer:").grid(row=0, column=0, pady=5, sticky="w")

        ttk.Entry(buttons_frame, width=20, textvariable= self.Project_Number
                  ).grid(row=1,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)
 

    def Coordinaten(self):
            Project = ArcGIS(self.Project_Number.get())
            Pandas = ArcGIS().get_coordinates(Project.Results())
            unique_projects = Pandas['Project'].unique().tolist()
            if len(unique_projects) >= 2:
                # Create a combobox to select the project
                global project_combobox
                project_combobox = ttk.Combobox(buttons_frame, width=20, values=unique_projects
                  )
                project_combobox.grid(row=2,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)
                #Create buttom to download the results of an specific project
                DownloadProject = tk.Button(buttons_frame,text = "Downloaden" 
                ,command = self.SpecificProjectDownload)
                DownloadProject.grid(row=2,column=0, padx=0,pady=0)
            else:
                Project.Download(Pandas)
                window.destroy()

    def SpecificProjectDownload(self):        
            Project = ArcGIS(self.Project_Number.get())
            Pandas = ArcGIS().get_coordinates(Project.Results())
            Filtered_Df = ArcGIS().filter_dataframe(Pandas,SpecificProject=project_combobox.get())
            window.destroy()
        
# Create the entire GUI program
Vista(window)

# Start the GUI event loop
tk.mainloop()    

#In[]: 

