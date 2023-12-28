#In[]

from arcgis.gis import GIS
import pandas as pd
import os 
from tkinter import messagebox
from ExportSHP  import ExportSHP
from GISDetails import GisCredentials
import re 
import sys

#In[]: 

class ArcGIS:
    
    def __init__(self,project_name):

        self.project_name = project_name

        # Username and password extracted from another class 
        self.client_id=GisCredentials().client_id
        self.pattern = r'bor.*'
        self.waypointstructure = "[Waypoint(0)] \nType = 0 \nXwp = xcoord \nYwp = ycoord \nZwp = 0\nName = boornum. \n\n"

    def Results(self):

        global gis
        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com", client_id=self.client_id)
        # Search for the feature layer by its name
        feature_layer_name = self.project_name
        results = gis.content.search(query=feature_layer_name, item_type="Feature Layer")
        if len(results) != 0: 
            # x.name is the name of the web feature layer! 
            Names = [x.name for x in results]
            for i in range(len(Names)):
                if Names[i] == 'Boringen_HBR':
                    ProjectName = Names [i]
                    LayerName = "Boringen_HBR"
                    NP = results[i].id
                    item = gis.content.get(NP)
                    point_layer = None                    
                    for layer in item.layers:
                        if layer.properties.geometryType == "esriGeometryPoint" and re.search(T.pattern, layer.properties.name.lower()):
                            ProjectName = item.name
                            point_layer = layer
                            LayerName = point_layer.properties.name
                            return ProjectName,LayerName,point_layer
                            break
                    #Break if the boringen layer has been found 
                    if point_layer is not None:
                        break
                    break

                elif Names[i] == '22131V1_TE01_WBO_IJmuiden_Uitvoering_WFL1':
                    ProjectName = Names [i]
                    LayerName = "Boringen_IJmuiden"
                    NP = results[i].id
                    item = gis.content.get(NP)
                    point_layer = None
                    for layer in item.layers:
                        if layer.properties.geometryType == "esriGeometryPoint" and re.search(T.pattern, layer.properties.name.lower()):
                            ProjectName = item.name
                            point_layer = layer
                            LayerName = point_layer.properties.name
                            return ProjectName,LayerName,point_layer
                            break
                    #Break if the boringen layer has been found 
                    if point_layer is not None:
                        break
                    break
            
            for x in range(len(results)): 
                NP = results[x].id
                item = gis.content.get(NP)
                point_layer = None
                for layer in item.layers:
                    if layer.properties.geometryType == "esriGeometryPoint" and re.search(self.pattern, layer.properties.name.lower()):
                        ProjectName = item.name
                        point_layer = layer
                        LayerName = point_layer.properties.name
                        return ProjectName,LayerName,point_layer
                        break
                #Break if the boringen layer has been found 
                if point_layer is not None:
                    break
                   
        else:

            message = "Er is geeen project {} gevonden. Probeer het nog eens!".format(self.project_name)
            # Display the messagebox
            messagebox.showwarning("Warning", message)
    
            
    def get_coordinates(self,point_layer):

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
                #In old layers this did not exist 
                Project.append(attributes['Projectnummer'])
            except: 
                pass

        df = pd.DataFrame(coords, columns=['X', 'Y'])
        df =df.round(0).astype(int)
        df['NR'] = labels

        # In case we are dealing with an old layer that did 
        # not have the column projectnummer 
        if len(Project)>1:
            
            df['Project'] = Project
        
        df.sort_values(by=['NR'], inplace=True)
        df.set_index('NR',inplace=True)
        return df

    
    def filter_dataframe(self, pandas, 
                         SpecificProject,
                         ProjectName = "Project XXXX Change",
                         LayerName= "Boringen_23xxxx"):
        filtered_df = pandas[pandas['Project'] == SpecificProject]
        global Specific_Project
        Specific_Project = SpecificProject
        PN = ProjectName
        LN = LayerName
        self.Download(filtered_df,ProjectName=PN,LayerName=LN)

        
    def Download(self,pandas,
                 ProjectName = "Project XXXX",
                 LayerName= "Boringen_23xxxx"):
        
        if LayerName == "Boringen_HBR" or LayerName == "Boringen_IJmuiden":
            NameDoc = Specific_Project
        else:
            NameDoc = LayerName
        try:
            pandas = pandas.drop('Project', axis=1)
        except:
            pass 
        
        #Names of the files 

        Name_File_punt = "NR.X.Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 
        Name_File_komma = "NR,X,Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 
        Name_File_Waypoint = "NR.X.Y v1.0 Coördinaten_" + ProjectName + "_" + NameDoc 

        # First, I will see if the folder exists in the P drive
        fp = os.path.join(ExportSHP(project_name=self.project_name).CreateFolderToSave(),Name_File_punt)
        fc = os.path.join(ExportSHP(project_name=self.project_name).CreateFolderToSave(),Name_File_komma)

        #First point separated
        pandas.to_csv(fp + ".txt", sep='.', index=True)
        # Now with a coma 
        pandas.to_csv(fc + ".txt", sep=',', index=True)
        # As excel        
        pandas.to_excel(fp + ".xlsx")
        # As waypoint 
        Template = self.waypointstructure
        WaypointText = str()

        for index, row in pandas.iterrows():
            NewLocation = Template
            NewLocation = NewLocation.replace("xcoord",str(row["X"]))
            NewLocation = NewLocation.replace("ycoord",str(row["Y"]))
            NewLocation= NewLocation.replace("boornum.",str(index) + ".")
            WaypointText = WaypointText + NewLocation

        fwp = os.path.join(ExportSHP(project_name=self.project_name).CreateFolderToSave(),Name_File_Waypoint + ".wpt")

        with open(fwp, 'w') as file:
            # Write the string to the file
            file.write(WaypointText)

        f = ExportSHP(project_name=self.project_name).CreateFolderToSave()
        
        message = f"De cöordinaten van de laag {NameDoc} voor het project {ProjectName} werd opgeslagen in de route: {f}"
        # Display the messagebox
        messagebox.showwarning("Warning", message)


#In[]:

#Test 

# Test = ArcGIS(project_name="23121")
# Res = Test.Results()
# df = Test.get_coordinates(point_layer=Res[-1])

# Test.Download(pandas=df,ProjectName=Res[0],
#               LayerName=Res[1])
#In[]: