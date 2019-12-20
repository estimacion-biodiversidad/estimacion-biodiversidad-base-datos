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

DATA_DIR = "./cites-ii/"


def updateTaxaCites():
    connString = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
    cites_dir = DATA_DIR

    # Open database        
    dsOut = ogr.Open(connString)
    if dsOut is None:
        print("Could not open PostGIS Database " + connString)
        return

    csv_list = sorted(glob.glob(cites_dir + '*.csv'))
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
                    taxonRank_field = -1
      
                    field_index = 0
                    for field in record:
                        if field.lower() == "fullname":
                            scientificName_field = field_index
                        elif field.lower() == "rankname":
                            taxonRank_field = field_index

                        field_index += 1

                    print("scientificName", scientificName_field)
                    print("taxonRank", taxonRank_field)

                    # break                    
                else:
                    if scientificName_field != -1:
                        scientific_name = record[scientificName_field]
                    else:
                        continue
                    if taxonRank_field != -1:
                        taxonRank = record[taxonRank_field]
                    else:
                        continue

                    if taxonRank.lower() == "family":
                        taxonRank_name = "family_name"
                    elif taxonRank.lower() == "genus":
                        taxonRank_name = "genus_name"
                    elif taxonRank.lower() == "species":
                        taxonRank_name = "scientific_name"

                    print(scientific_name + " " + taxonRank_name)  

                    # Assemble SQL statement
                    query_occurrences = "UPDATE taxon_occurrence SET lcvs_status = 'PR' WHERE {} = '{}';".format(taxonRank_name, scientific_name)
                    print(query_occurrences)
                    dsOut.ExecuteSQL(query_occurrences)
                    query_distribution = "UPDATE taxon_distribution SET lcvs_status = 'PR' WHERE {} = '{}';".format(taxonRank_name, scientific_name)
                    print(query_distribution)
                    dsOut.ExecuteSQL(query_distribution)

                i = i + 1
                                   
    dsOut = None

if __name__ == '__main__':
    start = time.time()
    updateTaxaCites()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
