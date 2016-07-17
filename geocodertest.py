import csv
import logging
from geopy import geocoders


class geocoderTest():
    def __init__(self, geo_type='google'):
        self.g = geocoders.get_geocoder_for_service(geo_type)()
        self.rows = []
        self.FIELDS = ["Name","Phone1","Phone2","Phone3","Phone4","Phone5","Street Address","Locality","Pincode","City","Country","Mail","Website","Person to Contact","Working Hours","Services Offered","Details","Images URL","Keywords"]

    def process(self):
        self._readCSV()
        self._addGeocoding()
        self._writeCSV()

    def _readCSV(self):
        # append new columns
        self.FIELDS.extend(["lat", "lng", "fullAddress"])

        inputFile = open('sample.csv', 'r')
        sample_text = ''.join(inputFile.readline() for x in range(3))
        dialect = csv.Sniffer().sniff(sample_text);
        inputFile.seek(0);
        reader = csv.DictReader(inputFile, dialect=dialect)
        # skip the head row
        next(reader)
        reader.fieldnames.extend(["lat", "lng", "fullAddress"]);
        self.rows.extend(reader);
        inputFile.close();

    def _addGeocoding(self):
        for row in self.rows:
            if (row["lat"] is None or row["lat"] == ""):
                address = "%s %s %s %s %s" % (row["Street Address"],row["Locality"],row["Pincode"],row["City"],row["Country"])
                try:
                    place, (lat, lng) = self.g.geocode(address, False)[0]
                    row["lat"] = lat
                    row["lng"] = lng
                    row["fullAddress"] = address
                except Exception as err:
                    logging.exception("Something awful happened when processing '"+address+"'");

    def _writeCSV(self):
        try:
            # DictWriter
            csvFile = open('result.csv', 'w')
            writer = csv.DictWriter(csvFile, fieldnames=self.FIELDS)
            # write header
            writer.writerow(dict(zip(self.FIELDS, self.FIELDS)))

            for row in self.rows:
                writer.writerow(row)

            csvFile.close()
        except Exception as err:
            logging.exception("Something awful happened when processing result.csv");

if __name__ == '__main__':
    f = geocoderTest()
    f.process()
