#In[]
from arcgis.gis import GIS
import os 
import zipfile
from tkinter import messagebox

#In[]:

class ExportSHP:

    def __init__(self,project_name = "Project Mh Poly"): 
        #Name of the project
        self.project_name = project_name
        self.directory_path = r'P:\2023'

    def CreateFolderToSave(self):
        
        #It does not create the general path where everything will be saved. But it looks where it can be saved.
        Matchingfolder = [name for name in os.listdir(self.directory_path) if 
                          os.path.isdir(os.path.join(self.directory_path, name)) 
                          and self.project_name in name]
        
        if len(Matchingfolder) != 0:
            f = os.path.join(self.directory_path, Matchingfolder[0])
            # Get a list of all folders inside f
            folders = [name for name in os.listdir(f) if os.path.isdir(os.path.join(f, name))]
            first_folder = os.path.join(f, folders[0])
            save_path =  os.path.join(first_folder, "05 Tekeningen", "Werkmap")
            return save_path
        else: 
            save_path = "Geen oveenkomende map gevonden! "
            return save_path
    
    def ArcGISConnection(self):
        global gis
        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com/", "TSCMHPoly", "n1H1p1*HZEO3")

    def GetNamesLayers(self):

        ##################

        # Search for the feature layer by its name
        feature_layer_name = self.project_name
        results = gis.content.search(query=feature_layer_name, item_type="Feature Layer")

        if len(results) != 0: 
            global feature_layer
            # x.name is the name of the web feature layer! 
            Names = [x.name for x in results]
            for i in range(len(Names)):

                if Names[i] == 'Boringen_HBR':
                    NP = results[i].id
                    layer_item = gis.content.get(NP)
                    feature_layer  = layer_item.layers
                    Layers_Names = []
                    for x in feature_layer:
                        Layers_Names.append(x.properties.name)
                    return Layers_Names
                    break



                elif Names[i] == '22131V1_TE01_WBO_IJmuiden_Uitvoering_WFL1':
                    NP = results[i].id
                    layer_item = gis.content.get(NP)
                    feature_layer  = layer_item.layers
                    Layers_Names = []
                    for x in feature_layer:
                        Layers_Names.append(x.properties.name)
                    return Layers_Names
                    break
            

            NP = results[0].id
            layer_item = gis.content.get(NP)
            feature_layer  = layer_item.layers
            Layers_Names = []
            for x in feature_layer:
                Layers_Names.append(x.properties.name)
            return Layers_Names
            
        
        else:

            message = "Er is geeen project {} gevonden. Probeer het nog eens!".format(self.project_name)
            # Display the messagebox
            messagebox.showwarning("Warning", message)


        ######################################################################################################


    def DownloadLayer(self, NameLayer,save_path):
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


        # Define the fields to be downloaded
        fields = ['NR', 'X','Y']

        try: 
            #For the boringen layer
            # Query the feature layer and download the results as a SHP file
            query_result = Layer_To_Download.query(where="1=1", out_fields=["NR,X,Y"], return_geometry=True)
            query_result.save(out_name = Layer_To_Download.properties.name + ".shp", save_location = output_folder)

        except: 
            try:
            #For the vakken layer
                # Query the feature layer and download the results as a SHP file
                query_result = Layer_To_Download.query(where="1=1", out_fields=["NR,Shape__Area"], return_geometry=True)
                query_result.save(out_name = Layer_To_Download.properties.name + ".shp", save_location = output_folder)
            except: 
                #For the vakken layer
                # Query the feature layer and download the results as a SHP file
                query_result = Layer_To_Download.query(where="1=1", out_fields=["NR,Shape_Area"], return_geometry=True)
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

# Testen = ExportSHP(project_name="23001")
# f = Testen.CreateFolderToSave()
# Testen.ArcGISConnection()
# Names = Testen.GetNamesLayers()
# Testen.DownloadLayer(NameLayer=Names[0],save_path=f)

#In[]: