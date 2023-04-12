# CoordinatenApp
 This App will allow the users to fetch the information from ArcGIS Online based on a project number and then extract the coordinates of points and export it in a specfic format 
 
 # Primero que nada, Buenos días
 
Estoy usando pyinstaller. El código es el siguiente: 

pyinstaller --onefile UI.py Coordinaten.py --hidden-import=arcgis

Sin embargo, siempre encuentro este error: https://drive.google.com/drive/folders/1yo1vN0SDY-i5dsechr-HrLM8vzxepO8h

# Respuesta de ESRI

Le escribí a ESRI (la compañia a la cual se le paga la licencia) acerca del incoveniente, y me respondieron lo siguiente: 

![image](https://user-images.githubusercontent.com/127189008/231406339-32774fb8-e7a6-4a6a-aed8-b9ac559a1508.png)

Resumen: El modulo arcgis.gis se instala cuando instalas ArcGIS. El objetivo de este modulo es poder hacer todo lo que haces en el programa mediante Python. No sé si sea muy loco lo que voy a decir pero: ¿Es posible que haya alguna restricción para compartir este modulo? Porque si este modulo se pudiera compartir libremente, no necesitaríamos pagar los 5000 euros de licencia anual de ArcGIS, porque todo lo podría hacer a través del modulo de Python. 

Lo que ellos proponen (aunque creo que no entendieron mi pregunta), es instalar mediante Conda el modulo, y  correr la App desde un IDE. Me gustaría evitar esto porque a mi equipo no es muy fan de ver código (por más simple que sea). 

# ❤️Zulu, el mejor❤️
