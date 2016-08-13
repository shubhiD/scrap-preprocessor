import csv
import logging
import glob
import os
import time
from geopy import geocoders

class geocoderTest():
    def __init__(self, geo_type='google'):
        if geo_type == 'googleV3':
            self.geoCoder = geocoders.GoogleV3("AIzaSyCgs8C71RqvWoeO69XBXVPQH006i7v4IkM");
        else:
            self.geoCoder = geocoders.get_geocoder_for_service(geo_type)();
        self.rows = []
        self.FIELDS = ["Name","Phone1","Phone2","Phone3","Phone4","Phone5","Street Address","Locality","Pincode","City","Country","Mail","Website","listing_person","Working Hours","Services Offered","Details","Images URL","Keywords"]

    def process(self):
        fileNames = glob.glob('./*.csv');
        for fileName in fileNames:
            fileBaseName = os.path.basename(fileName);
            self._readCSV(fileBaseName);
            self._addLocation();
            self._addGeocoding();
            self._addFeaturedImage();
            self._writeCSV(fileBaseName+"_processed");

    def _readCSV(self, fileName):
        inputFile = open(fileName, 'r')
        sample_text = ''.join(inputFile.readline() for x in range(3))
        dialect = csv.Sniffer().sniff(sample_text);
        inputFile.seek(0);
        reader = csv.DictReader(inputFile, dialect=dialect)
        # skip the head row
        # next(reader)
        # append new columns
        reader.fieldnames.extend(["lat", "lng", "fullAddress", "featured_image", "listing_locations"]);
        self.FIELDS = reader.fieldnames;
        self.rows.extend(reader);
        inputFile.close();
                
    def _addLocation(self):
        for row in self.rows:
            row["City"] = row["City"].title()
            row["Locality"] = row["Locality"].title()
            row["listing_locations"] = row["Locality"] +", "+ row["City"]

    def _addGeocoding(self):
        geoLocationAdded = 0;
        for row in self.rows:
            if (row["lat"] is None or row["lat"] == ""):
                address = "%s %s, %s, %s, %s" % (row["Street Address"],row["Locality"],row["City"],row["Pincode"],row["Country"])
                row["fullAddress"] = address;
                try:
                    time.sleep(1) # To prevent error from Google API for concurrent calls
                    place, (lat, lng) = self.geoCoder.geocode(address, False)[0]
                    row["lat"] = lat
                    row["lng"] = lng
                except Exception as err:
                    noLocationFoundErrorMessage = "'NoneType' object has no attribute '__getitem__'";
                    if err.message == noLocationFoundErrorMessage:
                        #logging.warning("Geocode API was unable to find the lat and long for : '"+address+"' - Trying by adding name now");
                        try:
                            address = "%s %s %s %s %s" % (row["Street Address"],row["Locality"],row["Pincode"],row["City"],row["Country"])
                            place, (lat, lng) = self.geoCoder.geocode(row["Name"]+", "+address, False)[0]
                            row["lat"] = lat
                            row["lng"] = lng
                        except Exception as err:
                            logging.warning("---- Trying by adding name is also failed");
                            row["lat"] = 0;
                            row["lng"] = 0;
                    else:
                        logging.exception("Something awful happened when processing '"+address+"'");
                geoLocationAdded+=1
                if (geoLocationAdded%20==0):
                     print "Records added: ",geoLocationAdded
        time.sleep(1) # To prevent error from Google API for concurrent calls


    def _addFeaturedImage(self):
        for row in self.rows:
            if not row["Images URL"]:
                row['featured_image'] = '';
            else:
                row['featured_image'] = row['Images URL'].split(",")[0].strip();
         
    def _writeCSV(self, fileName):
        try:
            # DictWriter
            csvFile = open(fileName, 'w');
            writer = csv.DictWriter(csvFile, fieldnames=self.FIELDS);
            # write header
            writer.writerow(dict(zip(self.FIELDS, self.FIELDS)));

            for row in self.rows:
                writer.writerow(row)

            csvFile.close()
        except Exception as err:
            logging.exception("Something awful happened when processing result.csv");

if __name__ == '__main__':
    f = geocoderTest()
    f.process()
