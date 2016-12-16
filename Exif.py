import os
from PIL import Image
from PIL.ExifTags import TAGS

path = 'C:\\Users\\Joe\\OneDrive - University of New Haven\\Fall 2016\\Adv Python\\Forensics\\ExifTool\\Images\\'

Lat = []
Lon = []

for root, dir, files in os.walk(path):
    for fp in files:
        if".JPG"in fp.upper():
            # open a file and extract exif
            fn = root + fp
            try:
                print(fn)
                i = Image.open(fn)
                info = i._getexif()
                exif={}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif[decoded]=value
                print(exif)
                # from the exif data, extract gps
                exifGPS = exif['GPSInfo']
                if len(exifGPS) != 0:
                    latData = exifGPS[2]
                    lonData = exifGPS[4]
                    # calculate the lat / long
                    latDeg = latData[0][0] /float(latData[0][1])
                    latMin = latData[1][0] /float(latData[1][1])
                    latSec = latData[2][0] /float(latData[2][1])
                    lonDeg = lonData[0][0] /float(lonData[0][1])
                    lonMin = lonData[1][0] /float(lonData[1][1])
                    lonSec = lonData[2][0] /float(lonData[2][1])
                    # correct the lat/lon based on N/E/W/S
                    Lat = (latDeg + (latMin + latSec/60.0)/60.0)
                    if exifGPS[1] =='S':
                        Lat = Lat * -1
                    Lon = (lonDeg + (lonMin + lonSec/60.0)/60.0)
                    if exifGPS[3] =='W':
                        Lon = Lon * -1
                    # print file
                    msg = fp +" located at "+str(Lat)+","+str(Lon)
                    print(msg)
                else:
                    print('No GPS Coords')
            except RuntimeError as e:
                print('Error')
