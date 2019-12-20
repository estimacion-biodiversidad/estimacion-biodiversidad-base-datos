from osgeo import ogr
import glob
import time
import csv


HOST = "localhost"
PORT = "5432"
DATABASE = "biocr20191115"
SCHEMA = "public"
USER = "gisadmin"
PASSWORD = "postgres"

DATA_DIR = "./registros-presencia/"


def loadTaxonOccurrence():
    connString = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
    occurrence_dir = DATA_DIR

    # Open database        
    dsOut = ogr.Open(connString)
    if dsOut is None:
        print("Could not open PostGIS Database " + connString)
        return

    txt_list = sorted(glob.glob(occurrence_dir + '*.txt'))
    for textfile in txt_list:
        print(textfile)

        outLayer     = dsOut.GetLayerByName("taxon_occurrence")
        outLayerDefn = outLayer.GetLayerDefn()
        
        with open(textfile, encoding="utf8") as f:
            records = csv.reader(f, delimiter='\t')
            
            i = 0
            j = 0
            
            query  = 'INSERT INTO taxon_occurrence '
            query += '(kingdom, phylum, class, "order", family, genus, scientific_name, geom) '
            query += 'VALUES'
		    
            remaining_inserts = False
            for record in records:
                print(i)
                remaining_inserts = True
            
                if i == 0: # header
                    print(str(record))  
                    taxonRank_field = -1
                    kingdom_field = -1
                    phylum_field = -1
                    class_field = -1
                    order_field = -1
                    family_field = -1
                    genus_field = -1
                    scientificName_field = -1
                    decimalLongitude_field = -1
                    decimalLatitude_field = -1

      
                    field_index = 0
                    for field in record:
                        if field.lower() == "taxonrank":
                            taxonRank_field = field_index
                        elif field.lower() == "kingdom":
                            kingdom_field = field_index
                        elif field.lower() == "phylum":
                            phylum_field = field_index
                        elif field.lower() == "class":
                            class_field = field_index
                        elif field.lower() == "order":
                            order_field = field_index
                        elif field.lower() == "family":
                            family_field = field_index
                        elif field.lower() == "genus":
                            genus_field = field_index
                        elif field.lower() == "species": # primero se revisa si hay un campo "species" (lo usa solo GBIF) y si no se usa el de scientificName
                            scientificName_field = field_index
                        elif field.lower() == "scientificname":
                            scientificName_field = field_index
                        elif field.lower() == "decimallongitude":
                            decimalLongitude_field = field_index
                        elif field.lower() == "decimallatitude":
                            decimalLatitude_field = field_index

                        field_index += 1

                    print("taxonRank", taxonRank_field)
                    print("kingdom", kingdom_field)
                    print("phylum", phylum_field)
                    print("class", class_field)
                    print("order", order_field)
                    print("family", family_field)
                    print("genus", genus_field)
                    print("scientificName", scientificName_field)

                    # break                    
                else:
                    # Check if DwC fields have been found and assign values to variables

                    # Taxon rank
                    if taxonRank_field == -1:
                        print("Registro sin rango taxonómico")
                        continue
                    else:
                        taxon_rank = record[taxonRank_field]
                        # Check if the record is identified at species or subspecies level
                        if taxon_rank.lower() not in ('species', 'subspecies', 'variety', 'form'):
                            print("Registro sin rango taxonómico")
                            continue

                    # Coordinates
                    if decimalLongitude_field != -1:
                        decimal_longitude = record[decimalLongitude_field]
                    else:
                        print("Registro sin longitud")
                        continue
                    if decimalLatitude_field != -1:
                        decimal_latitude = record[decimalLatitude_field]
                    else:
                        print("Registro sin latitud")
                        continue

                    # Taxonomy
                    if kingdom_field != -1:
                        kingdom = record[kingdom_field]
                    else:
                        kingdom = None
                    if phylum_field != -1:
                        phylum = record[phylum_field]
                    else:
                        phylum = None
                    if class_field != -1:
                        clase = record[class_field]
                    else:
                        clase = None
                    if order_field != -1:
                        order = record[order_field]
                    else:
                        order_name = None
                    if family_field != -1:
                        family = record[family_field]
                    else:
                        family_name = None
                    if genus_field != -1:
                        genus = record[genus_field]
                    else:
                        genus_name = None
                    if scientificName_field != -1:
                        scientific_name = record[scientificName_field]
                    else:
                        scientific_name = None

                    print(scientific_name + " " + str(decimal_longitude) + " " + str(decimal_latitude))  

                    # Assemble VALUES clause of INSERT statement
                    query += "('{}', '{}', '{}', '{}', '{}', '{}', '{}', ST_GeomFromText('POINT ({} {})', 4326)),".format(kingdom, 
                                                                                                                          phylum, 
                                                                                                                          clase, 
                                                                                                                          order, 
                                                                                                                          family, 
                                                                                                                          genus,
                                                                                                                          scientific_name,
                                                                                                                          str(decimal_longitude), str(decimal_latitude)
                                                                                                                         )

                    if j <= 999:
                        j += 1
                    else:
                        query = query[:-1]
                        query += ";"
                        print(query)
                        dsOut.ExecuteSQL(query)  
                        j = 0
                        remaining_inserts = False
                        query  = 'INSERT INTO taxon_occurrence '
                        query += '(kingdom, phylum, class, "order", family, genus, scientific_name, geom) '
                        query += 'VALUES'         
                        # break
         
                i = i + 1
                    
            if remaining_inserts:
                query = query[:-1]
                query += ";"            
                #print(query)
                dsOut.ExecuteSQL(query)  
            
                
    dsOut = None

if __name__ == '__main__':
    start = time.time()
    loadTaxonOccurrence()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
