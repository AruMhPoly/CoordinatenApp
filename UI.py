#In[]

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from PIL import ImageTk, Image
from Coordinaten import ArcGIS
from ExportSHP  import ExportSHP
from tkinter import messagebox

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

        # Logo

        image1 = Image.open(f"C:\Python\Coordinaten_App\Logo\Logo.jpeg")
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.grid(row=0, column=0,columnspan = 3)
        label1.image = test

        # Welcome Text

        window.title("Coördinaten uit ArcGIS Online")
        lbl_welcome = Label(welcome_frame,
                            text="Hoi! Hoe kan ik je helpen?")
        lbl_welcome.pack()

        # Frame Project Nummer

        ProjectNummer = tk.LabelFrame(window, text="Gegevens", relief=tk.RIDGE)
        ProjectNummer.grid(row=2, sticky="nsew",pady = 5)        
        
        # Text Frame Project Nummer 
        Label(ProjectNummer,
        text="Project nummer:           ").grid(row=0, column=0, pady=5, sticky="w")
        
        #Entry Frame Project Nummer

        ttk.Entry(ProjectNummer, width=20, textvariable= self.Project_Number
                  ).grid(row=0,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)

        #Frame to get the coordinates 
        global CöordinatenFrame
        CöordinatenFrame = tk.LabelFrame(window, text="Cöordinaten halen", relief=tk.RIDGE)
        CöordinatenFrame.grid(row=3, sticky="nsew",pady = 5)

        # First consult and see if there's more than one or more projects

        Label(CöordinatenFrame,
        text="Gewenst formaat:").grid(row=0, column=0, pady=5, sticky="w")

        Label(CöordinatenFrame,
        text="Database raadplagen:").grid(row=1, column=0, pady=5, sticky="w")

        #Coordinates button

        Get_Coordinates_Button = tk.Button(CöordinatenFrame,text = "Raadplegen"
                                        ,command = self.Coordinaten)
        Get_Coordinates_Button.grid(row=1,column=1, padx=10,pady=10,sticky='nsew')

       # Create a combobox to select the desired format
        global Format_Combobox
        Format_Combobox = ttk.Combobox(CöordinatenFrame, width=20, values=["punt scheidingsteken", "komma scheidingsteken","Excel Bestand"]
            )
        Format_Combobox.grid(row=0,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)
        Format_Combobox.current(0)


        # Frame Download Shapefiles 
        
        global SHP_Download_Frame
        SHP_Download_Frame = tk.LabelFrame(window, text="Shapefile Downloaden", relief=tk.RIDGE)
        SHP_Download_Frame.grid(row=4, sticky="nsew",pady = 5)


        #Buttom to get the layers associated to the project

        GetAvailableLayers = tk.Button(SHP_Download_Frame,text = "Raadplegen"
                                        ,command = self.ListLayers)
        GetAvailableLayers.grid(row=0,column=0, padx=10,pady=10,sticky="nsew")
        # Label(SHP_Download_Frame,
        # text="Lagen raadplegen").grid(row=0, column=0, pady=5, sticky="w")

        # Frame Créditos

        credit_frame = tk.LabelFrame(window,
                                            text="Contact persoon", relief=tk.RIDGE)
        credit_frame.grid(row=6, sticky="nsew", pady=5)


        # Texto de Créditos

        Label(credit_frame,text="Gecrëerd door: MH Poly").grid(row=0, sticky="nsew", pady=2)
        Label(credit_frame, text="E-mail: aru@mhpoly.com").grid(row=1, sticky="nsew", pady=2)
        Label(credit_frame, text="Telefoon nummer: +31 (0)164 245 566").grid(row=2, sticky="nsew", pady=2)

       
    # METHODS FOR THE APPLICATION - UP TO HIER WAS USER INTERFACE



    def Coordinaten(self):
        Project = ArcGIS(self.Project_Number.get())
        global R
        R = (Project.Results())
        print(R)
        Pandas = (Project.get_coordinates(R[2]))
        try:
            unique_projects = Pandas['Project'].unique().tolist()
        except: 
            #NVT = Niet van Toepassing
                unique_projects = ["NVT"]
        if len(unique_projects) >= 2:
            # Create a combobox to select the project
            global project_combobox
            project_combobox = ttk.Combobox(CöordinatenFrame, width=20, values=unique_projects
                )
            project_combobox.grid(row=2,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)
            #Create buttom to download the results of an specific project
            DownloadProject = tk.Button(CöordinatenFrame,text = "Downloaden" 
            ,command = self.SpecificProjectDownload)
            DownloadProject.grid(row=2,column=0, padx=0,pady=0)
        else:
            Project.Download(Pandas,format=Format_Combobox.get(),ProjectName=R[0],LayerName=R[1])
            window.destroy()

    def SpecificProjectDownload(self):        
        Project = ArcGIS(self.Project_Number.get())
        Pandas = Project.get_coordinates(R[2])
        Filtered_Df = ArcGIS().filter_dataframe(Pandas,SpecificProject=project_combobox.get()
                                                ,Format_Output=Format_Combobox.get(),
                                                ProjectName=R[0],LayerName=R[1])
        window.destroy()

    def ListLayers (self):
        Project = ExportSHP(project_name=self.Project_Number.get())
        Project.ArcGISConnection()
        Names = Project.GetNamesLayers()
        # Create a combobox to select the project
        global SHP_Combobox
        SHP_Combobox = ttk.Combobox(SHP_Download_Frame, width=20, values=Names
            )
        SHP_Combobox.grid(row=0,column=1,sticky=tk.E + tk.W + tk.N + tk.S, pady=5,)
        ##Decoration
        Label(SHP_Download_Frame,
              text="    Dat was het!").grid(row=2, column=0, sticky=tk.E + tk.W + tk.N + tk.S, pady=5)
        #Create buttom to download the results of an specific project
        DownloadShapeFile = tk.Button(SHP_Download_Frame,text = "Downloaden" 
        ,command = self.DownloadShapefile)
        DownloadShapeFile.grid(row=2,column=1, padx=0,pady=0)        

    def DownloadShapefile(self):        
        Project = ExportSHP(project_name=self.Project_Number.get())
        f = Project.CreateFolderToSave()
        OutputFolder = Project.DownloadLayer(NameLayer=SHP_Combobox.get(),save_path=f)
        message = "De laag werd opgeslagen op: {}".format(OutputFolder)
        # Display the messagebox
        messagebox.showwarning("Warning", message)
        window.destroy()

# Create the entire GUI program
Vista(window)

# Start the GUI event loop
tk.mainloop()    

#In[]: 

