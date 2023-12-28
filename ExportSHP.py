#In[]
from arcgis.gis import GIS
import os 
import zipfile
from tkinter import messagebox
from GISDetails import GisCredentials

#In[]:

class ExportSHP:

    def __init__(self,project_name): 
        #Name of the project
        self.project_name = project_name
        # Username and password extracted from another class 
        self.username =  GisCredentials().user
        self.password = GisCredentials().password

    def CreateFolderToSave(self):
         
        directory_path = [r'P:\2023',r'P:\2022']

        for d in directory_path:

            #I will look in 2022 and 2022 directory to see where can I save it 
            Matchingfolder = [name for name in os.listdir(d) if 
                            os.path.isdir(os.path.join(d, name)) 
                            and self.project_name in name]
        
            if len(Matchingfolder)!=0:
                f = os.path.join(d, Matchingfolder[0])
                WorkFolder = os.path.join(f,"V1","07 Tekeningen","Werkmap M&R") # First with the new structure 
                if not os.path.exists(WorkFolder): 
                    WorkFolder = os.path.join(f,"V1","05 Tekeningen","Werkmap") # Try with the old structure
                return WorkFolder
                break
            else: #Otherwise just save it in downloads
                    userhome = os.path.expanduser('~')
                    WorkFolder = os.path.join(userhome, 'Downloads')
                    return WorkFolder
            
        print(WorkFolder)
        
  
    def ArcGISConnection(self):
        global gis
        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com/", self.username, self.password)

    def GetNamesLayers(self):

        # Search for the feature layer by its name
        feature_layer_name = self.project_name
        results = gis.content.search(query=feature_layer_name, item_type="Feature Layer")

        if len(results) != 0: 
            Layer_names = []
            NPs = []
            for i in range(len(results)):
                NP = results[i].id
                layer_item = gis.content.get(NP)
                for j in layer_item.layers:
                    Layer_names.append(j.properties.name)
                    NPs.append(NP)

            # Zip the two lists into a dictionary
            global Dic1
            Dic1 = dict(zip(Layer_names, NPs))

            return(list(Dic1.keys()))
                   
        else:

            message = "Er is geeen project {} gevonden. Probeer het nog eens!".format(self.project_name)
            # Display the messagebox
            messagebox.showwarning("Warning", message)


        ######################################################################################################


    def DownloadLayer(self, NameLayer,save_path):

        NP = Dic1[NameLayer]
        layer_item = gis.content.get(NP)
        feature_layer  = layer_item.layers
        
        for layer in feature_layer:
            if layer.properties.name == NameLayer:
                Layer_To_Download = layer
                break

        # First, I will see if the folder exists in the P drive
        if os.path.exists(save_path):
            # Create a folder to save the SHP file
            output_folder = os.path.join(save_path, "SHP_" + self.project_name + "_" +
                                        Layer_To_Download.properties.name)
            os.makedirs(output_folder, exist_ok=True)
        else: 
            userhome = os.path.expanduser('~')
            downloads_folder = os.path.join(userhome, 'Downloads')
            output_folder = os.path.join(downloads_folder, "SHP_" + self.project_name + "_" +
                            Layer_To_Download.properties.name)
            os.makedirs(output_folder, exist_ok=True)

        if Layer_To_Download.properties.geometryType == 'esriGeometryPoint':
            #For the boringen layer
            # Query the feature layer and download the results as a SHP file
            query_result = Layer_To_Download.query(where="1=1", out_fields=["NR,X,Y"], return_geometry=True)
            query_result.save(out_name = Layer_To_Download.properties.name + ".shp", save_location = output_folder)

        elif Layer_To_Download.properties.geometryType == 'esriGeometryPolygon':
            
            try:
            #For the vakken layer
                # Query the feature layer and download the results as a SHP file
                query_result = Layer_To_Download.query(where="1=1", out_fields=["NR,Shape__Area"], return_geometry=True)
                query_result.save(out_name = Layer_To_Download.properties.name + ".shp", save_location = output_folder)
            except: 
                #For the vakken layer
                # Query the feature layer and download the results as a SHP file
                query_result = Layer_To_Download.query(where="1=1", return_geometry=True)
                query_result.save(out_name = Layer_To_Download.properties.name + ".shp", save_location = output_folder)

        # Set the name for the zip file to be created
        zip_file_name = Layer_To_Download.properties.name + ".zip"

        # Create a ZipFile object with the output file name and mode
        with zipfile.ZipFile(os.path.join(output_folder, zip_file_name), 'w') as zipf:
            # Iterate through all files in the directory and add them to the zip file
            for foldername, subfolders, filenames in os.walk(output_folder):
                for filename in filenames:
                    # Ignore the output file itself
                    if filename != zip_file_name:
                        file_path = os.path.join(foldername, filename)
                        zipf.write(file_path, arcname=os.path.relpath(file_path, output_folder))


        return output_folder
#In[]:

# Testen = ExportSHP(project_name="23121")
# f = Testen.CreateFolderToSave()
# Testen.ArcGISConnection()
# Names = Testen.GetNamesLayers()
# Testen.DownloadLayer(NameLayer=Names[3],save_path=f)
#In[]:

