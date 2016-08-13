import csv
import logging
import glob
import os
import time
import googlemaps

class geocoderTest():
    def __init__(self, geo_type='google'):
        self.gmaps = googlemaps.Client(key='AIzaSyCgs8C71RqvWoeO69XBXVPQH006i7v4IkM');
        self.rows = []
        self.FIELDS = [];

    def process(self):
        fileNames = glob.glob('./input/*.csv');
        for fileName in fileNames:
            fileBaseName = os.path.basename(fileName);
            self._readCSV(fileName);
            self._addGeocoding();
            self._addLocationPhoto();
            self._addFeaturedImage();
            self._writeCSV("./output/processed_"+fileBaseName);

    def _readCSV(self, fileName):
        inputFile = open(fileName, 'r')
        sample_text = ''.join(inputFile.readline() for x in range(3))
        dialect = csv.Sniffer().sniff(sample_text);
        inputFile.seek(0);
        reader = csv.DictReader(inputFile, dialect=dialect)
        # skip the head row
        # next(reader)
        # append new columns
        reader.fieldnames.extend(["listing_locations", "featured_image", "location_image", "fullAddress", "lat", "lng"]);
        self.FIELDS = reader.fieldnames;
        self.rows.extend(reader);
        inputFile.close();

    def _addGeocoding(self):
        geoLocationAdded = 0;
        geoLocationFailed = 0;
        for row in self.rows:
            if (row["lat"] is None or row["lat"] == ""):
                address = "%s %s, %s, %s, %s" % (row["Street Address"],row["Locality"],row["City"],row["Pincode"],row["Country"])
                row["fullAddress"] = address;
                row["Locality"] = row["Locality"].title()
                row["City"] = row["City"].title()
                row["listing_locations"] = row["Locality"] + ", " + row["City"];
                try:
                    time.sleep(1); # To prevent error from Google API for concurrent calls
                    geocode_result = self.gmaps.geocode(address);
                    if(len(geocode_result)>0):
                        row["lat"] = geocode_result[0]['geometry']['location']['lat'];
                        row["lng"] = geocode_result[0]['geometry']['location']['lng'];
                    else:
                        logging.warning("Geocode API failure for : '" + address + "'");
                        geocode_result = self.gmaps.geocode(row["Name"] + ", " + address);
                        if (len(geocode_result) > 0):
                            row["lat"] = geocode_result[0]['geometry']['location']['lat'];
                            row["lng"] = geocode_result[0]['geometry']['location']['lng'];
                        else:
                            logging.warning("---- Trying by adding name also failed");
                            geoLocationFailed+=1;
                            row["lat"] = 0;
                            row["lng"] = 0;
                except Exception as err:
                    logging.exception("Something awful happened when processing '"+address+"'");
                    geoLocationFailed+=1;
                    row["lat"] = 0;
                    row["lng"] = 0;
                geoLocationAdded+=1;
                if (geoLocationAdded%10==0):
                    print("Processed "+str(geoLocationAdded)+" rows.");
        time.sleep(3); # To prevent error from Google API for concurrent calls
        print("Successfully completed processing of (" + str(geoLocationAdded-geoLocationFailed) + "/" + str(geoLocationAdded) + ") rows.");

    def _addLocationPhoto(self):
        for row in self.rows:
            if row["lat"]==0:
                row['location_image'] = '';
            else:
                #myLocation = (row["lat"], row["lng"]);
                #locationResult = self.gmaps.places_nearby(myLocation);
                #photoReference = locationResult['results'][0]['photos'][0]['photo_reference'];
                #placesPhoto = self.gmaps.places_photo(photoReference, max_width=100);
                row['location_image'] = "mylocationImage.jpg";

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
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    f = geocoderTest()
    f.process()