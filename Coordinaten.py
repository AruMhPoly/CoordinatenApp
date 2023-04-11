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
        gis = #Deleted due to privacy reasons

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
                LayerName = "Boringen_IJmuiden"
                return NP
                break

        NP = results[0].id
        item = gis.content.get(NP)
        LayerName = item.name
        return NP

            
    def get_coordinates(self,NP):

                
        # Connect to your ArcGIS Online organization
        gis = #Deleted due to privacy reasons

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
            Project.append(attributes['Opmerking'])

        df = pd.DataFrame(coords, columns=['X', 'Y'])
        df =df.round(0).astype(int)
        df['NR'] = labels
        df['Project'] = Project
        df.set_index('NR',inplace=True)
        return df 

    
    def filter_dataframe(self,pandas,SpecificProject):
        filtered_df = pandas[pandas['Project'] == SpecificProject]
        # return(filtered_df)
        self.Download(filtered_df)
        
    def Download(self,pandas):
        # Define the destination folder path
        userhome = os.path.expanduser('~')
        downloads_folder = os.path.join(userhome, 'Downloads')
        Name_File = "NR.X.Y v1.0 Coördinaten_" + LayerName + ".txt"
        f = os.path.join(downloads_folder, Name_File)
        # write the DataFrame to a text file with values separated by a "."
        # pandas = pandas.drop('Project', axis=1)
        pandas.to_csv(f, sep='.', index=True)
        # Open the file for reading
        with open(f, 'r') as file:
            # Read the contents of the file
            contents = file.read()
            # Replace double quotes with a space
            contents = contents.replace('"', ' ')
        # Open the file for writing
        with open(f, 'w') as file:
            # Write the modified contents to the file
            file.write(contents)

#In[]: