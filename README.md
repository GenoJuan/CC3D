# CC3D

Este repositorio contiene scripts que pretender servir como la base para el desarrollo de funciones en CC3D.

HandleOutputData_cc3d.py is a python script aimed to be useful as an CC3D steppable. The script helps to print cell attributes, chemical fields and cell interactions.

In order to employ it one has to write:


  from HandleOutputData_cc3d import HandleOutputDataClass
  HandleOutputDataClassInstance=HandleOutputDataClass(sim,_frequency=10)
  steppableRegistry.registerSteppable(HandleOutputDataClassInstance)

in the cc3d_project_file_name.py (do not confund it with cc3d_project_file_nameSteppables.py). 

Note that _frequency is a customizable parameter.
