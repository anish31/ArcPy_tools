#-------------------------------------------------------------------------------
# Name:        Clipping tool for multiple raster
# Purpose:     Clips multuiple raster and exports the attribute table
#
# Author:      anish
#
# Created:     18/11/2020
# Copyright:   (c) anish 2020
# Licence:     ArcGIS 10.x with spatial analyst extension
#-------------------------------------------------------------------------------
# import the required modules (Toolbox code)
import arcpy,os
from arcpy.sa import *

# Setting the input and output workspace
arcpy.env.workspace=arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput=True
maskAr=arcpy.GetParameterAsText(2)
outWs=arcpy.GetParameterAsText(1)

# Start of try-error block
try:
    # Checks the availability of Arcpy spatial analyst extension
    if arcpy.CheckExtension("Spatial")=="Available":
        arcpy.CheckOutExtension("Spatial")

        # Selecting raster file in input and running through it
        raster = arcpy.ListRasters()

        # For each raster the data is extracted through mask, attribute table saved as .csv
        for r in raster:
            masRas = ExtractByMask(r,maskAr)
            arcpy.GetMessages(2)
            arcpy.AddMessage("Extracting by mask raster "+r)
            out = (r.replace (".tif",""))
            arcpy.TableToTable_conversion(masRas,outWs,out+".csv")
            arcpy.GetMessages(2)
            arcpy.AddMessage("Extracting the attribute table to "+ out + ".csv")
            masRas.save(os.path.join(outWs,"clipped "+r))

        arcpy.CheckInExtension("Spatial")
    else:
        arcpy.AddMessage("Spatial Analyst Extention not available")

except arcpy.ExecuteError:
    arcpy.AddError("An error has occured in GP tool")
    print("An critical error occured: \n{0}".format(arcpy.GetMessages(2)))

finally:
    arcpy.AddMessage("Process Completed")



