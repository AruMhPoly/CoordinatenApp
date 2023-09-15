#In[]

from arcgis.gis import GIS
import pandas as pd
import os 
from tkinter import messagebox
from ExportSHP  import ExportSHP

#In[]: 

class ArcGIS:
    
    def __init__(self,project_name='Project Mh Poly'):

        self.project_name = project_name

    def Results(self):

        global gis
        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com/", "TSCMHPoly", "4aNTW$qrD*Hu$cA")

        # Search for the feature layer by its name
        feature_layer_name = self.project_name
        results = gis.content.search(query=feature_layer_name, item_type="Feature Layer")

        if len(results) != 0: 

            # x.name is the name of the web feature layer! 
            Names = [x.name for x in results]
            for i in range(len(Names)):
                if Names[i] == 'Boringen_HBR':
                    ProjectName = Names [i]
                    NP = results[i].id
                    LayerName = "Boringen_HBR"
                    return ProjectName,LayerName,NP
                    break

                elif Names[i] == '22131V1_TE01_WBO_IJmuiden_Uitvoering_WFL1':
                    ProjectName = Names [i]
                    LayerName = "Boringen_IJmuiden"
                    NP = results[i].id
                    return ProjectName,LayerName,NP
                    break
            
            for x in range(len(results)): 
                NP = results[x].id
                item = gis.content.get(NP)
                point_layer = None
                feature_layer  = item.layers
                for layer in item.layers:
                    if layer.properties.geometryType == "esriGeometryPoint":
                        ProjectName = item.name
                        point_layer = layer
                        LayerName = point_layer.properties.name
                        return ProjectName,LayerName,NP
                        break
        
        else:

            message = "Er is geeen project {} gevonden. Probeer het nog eens!".format(self.project_name)
            # Display the messagebox
            messagebox.showwarning("Warning", message)
    
            
    def get_coordinates(self,NP):

        layer_item = gis.content.get(NP)
        point_layer = None
        feature_layer  = layer_item.layers
        for layer in layer_item.layers:
            if layer.properties.geometryType == "esriGeometryPoint":
                point_layer = layer
                break
        # Query the feature layer to get all the features
        features = point_layer.query()
        # Create an empty list to store the coordinates
        coords = []
        labels = []
        Project = []
        # Loop through the features and extract the coordinates
        for feature in features:
            geometry = feature.geometry
            x = geometry['x']
            y = geometry['y']
            coords.append([x, y])
            attributes = feature.attributes
            labels.append(attributes['NR'])
            try:
                Project.append(attributes['Projectnummer'])
            except: 
                pass

        df = pd.DataFrame(coords, columns=['X', 'Y'])
        df =df.round(0).astype(int)
        df['NR'] = labels
        #In case we have more than one project saved in the same layer. Think HBR of IJmuiden
        if len(Project)>1:
            df['Project'] = Project
        df.sort_values(by=['NR'], inplace=True)
        df.set_index('NR',inplace=True)
        return df

    
    def filter_dataframe(self, pandas, SpecificProject, Format_Output="punt scheidingsteken",
                         ProjectName = "Project MH Poly",LayerName= "Boringen_23xxxx"):
        filtered_df = pandas[pandas['Project'] == SpecificProject]
        global Specific_Project
        Specific_Project = SpecificProject
        PN = ProjectName
        LN = LayerName
        self.Download(filtered_df, format=Format_Output,ProjectName=PN,LayerName=LN)

        
    def Download(self,pandas,format="punt scheidingsteken",
                 ProjectName = "Project MH Poly",LayerName= "Boringen_23xxxx"):
        if LayerName == "Boringen_HBR" or LayerName == "Boringen_IJmuiden":
            NameDoc = Specific_Project
        else:
            NameDoc = LayerName
        try:
            pandas = pandas.drop('Project', axis=1)
        except:
            pass 
############################################ Download Data #######################################################
        
        if format == "punt scheidingsteken":
        
            Name_File = "NR.X.Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 

        elif format == "komma scheidingsteken": 

            Name_File = "NR,X,Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 

        else: 

            Name_File = "NR.X.Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 

        # First, I will see if the folder exists in the P drive
        f = os.path.join(ExportSHP(self.project_name).CreateFolderToSave(),Name_File)

        if format == "punt scheidingsteken":
            
            pandas.to_csv(f + ".txt", sep='.', index=True)
            # Open the file for reading
            with open(f + ".txt", 'r') as file:
                # Read the contents of the file
                contents = file.read()
                # Replace double quotes with a space
                contents = contents.replace('"', ' ')
            # Open the file for writing
            with open(f + ".txt", 'w') as file:
                # Write the modified contents to the file
                file.write(contents)
        elif format == "komma scheidingsteken":
            pandas.to_csv(f + ".txt", sep=',', index=True)
            # Open the file for reading
            with open(f + ".txt", 'r') as file:
                # Read the contents of the file
                contents = file.read()
                # Replace double quotes with a space
                contents = contents.replace('"', ' ')
                contents = contents.replace(',', ', ')
            # Open the file for writing
            with open(f + ".txt", 'w') as file:
                # Write the modified contents to the file
                file.write(contents)
        elif format == "Excel Bestand":
            pandas.to_excel(f + ".xlsx")

        message = f"De cöordinaten van de laag {NameDoc} voor het project {ProjectName} werd opgeslagen in de route: {f}"
        # Display the messagebox
        messagebox.showwarning("Warning", message)


#In[]:

# #Testen 

# T = ArcGIS("23046")
# R = (T.Results())
# df = (T.get_coordinates(R[2]))
# T.Download(pandas= df, ProjectName=R[0],LayerName=R[1])

#In[]: