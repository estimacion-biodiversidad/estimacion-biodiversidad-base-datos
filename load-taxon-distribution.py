from osgeo import ogr
import glob
import time


HOST = "localhost"
PORT = "5432"
DATABASE = "biocr20191115"
SCHEMA = "public"
USER = "gisadmin"
PASSWORD = "postgres"

DATA_DIR = "./areas-distribucion/"


def loadTaxonDistribution():
    connString = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
    distribution_dir = DATA_DIR

    # Open database        
    dsOut = ogr.Open(connString)
    if dsOut is None:
        print("Could not open PostGIS Database " + connString)
        return

    shp_list = sorted(glob.glob(distribution_dir + '*.shp'))
    for shapefile in shp_list:
        print(shapefile)

        # Open shapefile with areas
        inShapefile  = shapefile
        driver       = ogr.GetDriverByName("ESRI Shapefile")
        dataSource   = driver.Open(inShapefile, 0)
        inLayer      = dataSource.GetLayer()
           
        # Load thematic area records            
        for feature in inLayer:
            geometry = feature.geometry()
            # if geometry is None or not geometry.IsValid():
            if geometry is None:
                break
            if geometry.GetGeometryType() == ogr.wkbPolygon:
                geometry = ogr.ForceToMultiPolygon(geometry)
            geometryWKT = geometry.ExportToWkt()
            query  = "INSERT INTO taxon_distribution "
            query += '(kingdom, phylum, class, "order", family, genus, scientific_name, geom) '
            query += "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', ST_GeomFromText('{}', 4326));".format(str(feature.GetField("kingdom")).capitalize(),
                                                                                                              str(feature.GetField("phylum")).capitalize(),
                                                                                                              str(feature.GetField("class")).capitalize(), 
                                                                                                              str(feature.GetField("order_")).capitalize(),
                                                                                                              str(feature.GetField("family")).capitalize(),
                                                                                                              str(feature.GetField("genus")).capitalize(),
                                                                                                              str(feature.GetField("sciname")).capitalize(),
                                                                                                              geometryWKT
                                                                                                             )

            #print(query)
            dsOut.ExecuteSQL(query)

        # Delete invalid geometries
        query = "DELETE FROM taxon_distribution WHERE NOT ST_IsValid(geom);"
        #print(query)
        dsOut.ExecuteSQL(query)
            
    dsOut = None

if __name__ == '__main__':
    start = time.time()
    loadTaxonDistribution()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
