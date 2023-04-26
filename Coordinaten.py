#In[]

from arcgis.gis import GIS
import pandas as pd
import os 

#In[]: 

class ArcGIS:
    
    def __init__(self,project_name='Project Mh Poly'):

        self.project_name = project_name

    def Results(self):

        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com/", "TSCMHPoly", "n1H1p1*HZEO3")

        # Search for the feature layer by its name
        feature_layer_name = self.project_name
        results = gis.content.search(query=feature_layer_name, item_type="Feature Layer")

        global LayerName
        Names = [x.name for x in results]
        for i in range(len(Names)):
            if Names[i] == 'Boringen_HBR':
                NP = results[i].id
                LayerName = "Boringen_HBR"
                return NP
                break
            if Names[i] == '22131N1-TE02 WBO IJmuiden Uitvoering WF':
                NP = results[i].id
                return NP
                LayerName = "Boringen_IJmuiden"
                break

        NP = results[0].id
        item = gis.content.get(NP)
        LayerName = item.name
        return NP

            
    def get_coordinates(self,NP):

                
        # Connect to your ArcGIS Online organization
        gis = GIS("https://mhpoly.maps.arcgis.com/", "TSCMHPoly", "n1H1p1*HZEO3")
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

    
    def filter_dataframe(self, pandas, SpecificProject, Format_Output="punt scheidingsteken"):
        filtered_df = pandas[pandas['Project'] == SpecificProject]
        global HBR_Project
        HBR_Project = SpecificProject
        self.Download(filtered_df, format=Format_Output)


        
    def Download(self,pandas,format="punt scheidingsteken"):
        if LayerName == "Boringen_HBR" or LayerName == "Boringen_IJmuiden":
            NameDoc = HBR_Project
        else:
            NameDoc = LayerName
        try:
            pandas = pandas.drop('Project', axis=1)
        except:
            pass 
        # Define the destination folder path
        userhome = os.path.expanduser('~')
        downloads_folder = os.path.join(userhome, 'Downloads')
        Name_File = "NR.X.Y v1.0 Coördinaten_" + NameDoc 
        f = os.path.join(downloads_folder, Name_File)
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

#In[]: