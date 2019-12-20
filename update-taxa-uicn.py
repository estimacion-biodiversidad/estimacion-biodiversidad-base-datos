from osgeo import ogr
import glob
import time
import csv


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"

DATA_DIR = "./amenazadas-iucn/"


def updateTaxaIUCN():
    connString = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
    iucn_dir = DATA_DIR

    # Open database        
    dsOut = ogr.Open(connString)
    if dsOut is None:
        print("Could not open PostGIS Database " + connString)
        return

    csv_list = sorted(glob.glob(iucn_dir + '*.csv'))
    for csvfile in csv_list:
        print(csvfile)

        with open(csvfile, encoding="utf8") as f:
            records = csv.reader(f, delimiter=',')
            
            i = 0
            for record in records:
                print(i)
            
                if i == 0: # header
                    print(str(record))  
                    scientificName_field = -1
                    redListCategory_field = -1
      
                    field_index = 0
                    for field in record:
                        if field.lower() == "scientificname":
                            scientificName_field = field_index
                        elif field.lower() == "redlistcategory":
                            redListCategory_field = field_index

                        field_index += 1

                    print("scientificName", scientificName_field)
                    print("redlistCategory", redListCategory_field)

                    # break                    
                else:
                    if scientificName_field != -1:
                        scientific_name = record[scientificName_field]
                    else:
                        continue
                    if redListCategory_field != -1:
                        redListCategory_name = record[redListCategory_field]
                    else:
                        continue

                    if redListCategory_name.lower() == "vulnerable":
                        redListCategory_abbr = "VU"
                    elif redListCategory_name.lower() == "endangered":
                        redListCategory_abbr = "EN"
                    elif redListCategory_name.lower() == "critically endangered":
                        redListCategory_abbr = "CR"

                    print(scientific_name + " " + redListCategory_name)  

                    # Assemble SQL statement
                    query_occurrences = "UPDATE taxon_occurrence SET iucn_status = '{}' WHERE scientific_name = '{}';".format(redListCategory_abbr, scientific_name)
                    print(query_occurrences)
                    dsOut.ExecuteSQL(query_occurrences)
                    query_distribution = "UPDATE taxon_distribution SET iucn_status = '{}' WHERE scientific_name = '{}';".format(redListCategory_abbr, scientific_name)
                    print(query_distribution)
                    dsOut.ExecuteSQL(query_distribution)

                i = i + 1
                                   
    dsOut = None

if __name__ == '__main__':
    start = time.time()
    updateTaxaIUCN()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
