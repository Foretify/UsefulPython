# coding: utf-8
'''
-----------------------------------------------------------------------------
Copyright 2016 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------------------

==================================================
RangeRingUtils.py
--------------------------------------------------
requirements: ArcGIS 10.3.1+, ArcGIS Pro 1.2+
author: ArcGIS Solutions
company: Esri
==================================================
description: Utilities to create range ring features
==================================================
history:
3/29/2016 - mf - design & original coding
==================================================
'''
import os
import sys
import traceback
import arcpy

acceptableDistanceUnits = ['METERS', 'KILOMETERS',
                           'MILES', 'NAUTICAL_MILES',
                           'FEET', 'US_SURVEY_FEET']

srDefault = arcpy.SpatialReference(54032) # World_Azimuthal_Equidistant

def rangeRingsFromList(centerFC, rangeList, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr):
    ''' Make range ring features from a center, and list of distances '''
    try:

        if (centerFC is None) or (rangeList is None) or (len(rangeList) == 0) \
            or (outputRingFeatures == None) :
            arcpy.AddError("Bad parameters supplied to rangeRingsFromList")
            return [None, None]

        if not sr:
            msg = r"Using default spatial reference: " + str(srDefault.name)
            arcpy.AddWarning(msg)
            print(msg)
            sr = srDefault

        rm = RingMaker(centerFC, rangeList, distanceUnits, sr)

        # Create Rings...
        numCenterPoints = arcpy.GetCount_management(centerFC).getOutput(0)

        if int(numCenterPoints) < 1:
            arcpy.AddError("At least one input center point is required")
            return [None, None]

        numRingsPerCenter = len(rangeList)
        totalNumRings = int(numCenterPoints) * int(numRingsPerCenter)
        totalNumRadials = int(numCenterPoints) * int(numRadials)
        arcpy.AddMessage("Making rings " + str(totalNumRings) + " (" + str(numRingsPerCenter) + " for " + str(numCenterPoints) + " centers)...")
        rm.makeRingsFromDistances()
        outRings = rm.saveRingsAsFeatures(outputRingFeatures)

        # Create Radials...
        arcpy.AddMessage("Making radials " + str(totalNumRadials) + " (" + str(numRadials) + " for " + str(numCenterPoints) + " centers)...")
        if (outputRadialFeatures is not None) and (numRadials > 0):
            rm.makeRadials(numRadials)
            outRadials = rm.saveRadialsAsFeatures(outputRadialFeatures)
        else:
            outRadials = None
            if (numRadials < 0):
                arcpy.AddWarning("Number of radials must be positive")

        return [outRings, outRadials]

    except arcpy.ExecuteError:
        # Get the tool error messages
        msgs = arcpy.GetMessages()
        arcpy.AddError(msgs)
        print(msgs)

    except:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + \
                "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Return python error messages for use in script tool or Python Window
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)
        # Print Python error messages for use in Python / Python Window
        print(pymsg + "\n")
        print(msgs)

def rangeRingsFromMinMax(centerFC, rangeMin, rangeMax, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr):
    ''' Make range ring features from only two distances, a minimum and a maximum '''
    if (rangeMin < 0.0) or (rangeMax <= 0.0) or (rangeMin > rangeMax):
        arcpy.AddError("Range parameters are not valid")
        return [None, None]

    rangeList = [min(rangeMin, rangeMax), max(rangeMin, rangeMax)]
    return rangeRingsFromList(centerFC, rangeList, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr)

def rangeRingsFromInterval(centerFC, numRings, distBetween, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr):

    ''' Classic range rings from number of rings, and distance between rings  '''
    if distBetween <= 0.0:
        arcpy.AddError("Distance between rings must be > 0")
        return [None, None]

    rangeList = [x * distBetween for x in range(1, numRings + 1)]
    return rangeRingsFromList(centerFC, rangeList, distanceUnits, numRadials, outputRingFeatures, outputRadialFeatures, sr)


class RingMaker:
    '''
    Core class for making range rings.
    '''

    def __init__(self, center, inputRangeList, distanceUnits, sr):
        ''' initialize rings '''

        self.deleteme = []

        # project center to sr, and keep it as a list of PointGeometries object
        originalGeom = arcpy.CopyFeatures_management(center, arcpy.Geometry())
        newGeom = []
        for g in originalGeom:
            newGeom.append(g.projectAs(sr))
        self.center = newGeom

        self.rangeList = self._sortList(inputRangeList)
        if distanceUnits == None or distanceUnits == "#" or distanceUnits == "":
            self.distanceUnits = sr.linearUnitName
        else:
            self.distanceUnits = distanceUnits

        if not sr == None or not sr == "#" or not sr == "":
            self.sr = sr
        else:
            self.sr = srDefault

        self.ringFeatures = None
        self.radialFeatures = None
        self.ringCount = len(self.rangeList)
        self.ringMin = min(self.rangeList)
        self.ringMax = max(self.rangeList)

    def __del__(self):
        ''' clean up rings '''
        for i in self.deleteme:
            if arcpy.Exists(i):
                arcpy.Delete_management(i)

    def _sortList(self, listToSort):
        ''' sort list of distances '''
        if len(listToSort) == 0:
            print("Empty distance list")
            return None
        return sorted(listToSort)

    def _addFieldsToTable(self, tab, fields):
        ''' add fields from dictionary: {'<fieldname>':'type'} '''
        for f in list(fields.keys()):
            arcpy.AddField_management(tab, f, fields[f])
        return tab

    def _makeTempTable(self, name, fields):
        ''' make a temporary, in_memory table '''
        tab = os.path.join("in_memory", name)
        arcpy.CreateTable_management(os.path.dirname(tab),
                                     os.path.basename(tab))
        self.deleteme.append(tab)
        if fields:
            newtab = self._addFieldsToTable(tab, fields)
        else:
            print("no fields to add")
            newtab = tab
        return newtab

    def makeRingsFromDistances(self):
        ''' make geodesic rings from distance list '''
        # make a table for TableToEllipse
        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'Range':'DOUBLE'}
        inTable = self._makeTempTable("ringTable", fields)
        cursor = arcpy.da.InsertCursor(inTable, ['x', 'y', 'Range'])
        #self.center is a list of PointGeometry
        for i in self.center:
            pt = i.firstPoint
            for r in self.rangeList:
                cursor.insertRow([pt.X, pt.Y, r * 2])

        del cursor
        self.deleteme.append(inTable)
        outFeatures = os.path.join("in_memory", "outRings")
        arcpy.TableToEllipse_management(inTable, outFeatures,
                                        'x', 'y', 'Range', 'Range',
                                        self.distanceUnits,
                                        '#', '#', '#', self.sr)

        self.deleteme.append(outFeatures)
        self.ringFeatures = outFeatures
        arcpy.CalculateField_management(outFeatures, "Range",'!Range! / 2.0','PYTHON_9.3')
        return outFeatures

    def makeRadials(self, numRadials):
        ''' make geodesic radials from number of radials '''
        segmentAngle = 360.0/float(numRadials)
        segmentAngleList = []
        a = 0.0
        while a < 360.0:
            segmentAngleList.append(a)
            a += segmentAngle

        fields = {'x':'DOUBLE', 'y':'DOUBLE', 'Bearing':'DOUBLE', 'Range':'DOUBLE'}
        tab = self._makeTempTable("radTable", fields)
        cursor = arcpy.da.InsertCursor(tab, ['x', 'y', 'Bearing', 'Range'])
        for i in self.center:
            pt = i.firstPoint
            for r in segmentAngleList:
                cursor.insertRow([pt.X, pt.Y, r, self.ringMax])
        del cursor
        self.deleteme.append(tab)
        outRadialFeatures = os.path.join("in_memory", "outRadials")
        arcpy.BearingDistanceToLine_management(tab, outRadialFeatures, 'x', 'y',
                                               'Range', self.distanceUnits, 'Bearing', "DEGREES",
                                               "GEODESIC", "#", self.sr)
        self.deleteme.append(outRadialFeatures)
        self.radialFeatures = outRadialFeatures
        return outRadialFeatures

    def saveRingsAsFeatures(self, outputFeatureClass):
        ''' save rings to featureclass '''
        arcpy.CopyFeatures_management(self.ringFeatures, outputFeatureClass)
        return outputFeatureClass

    def saveRadialsAsFeatures(self, outputFeatureClass):
        ''' save radials to featureclass '''
        arcpy.CopyFeatures_management(self.radialFeatures, outputFeatureClass)
        return outputFeatureClass
