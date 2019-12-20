from osgeo import ogr
import glob
import time


HOST = "localhost"
PORT = "5432"
DATABASE = "biocr20191115"
SCHEMA = "public"
USER = "gisadmin"
PASSWORD = "postgres"

DATA_DIR = "./capas-tematicas/"


def loadThematicAreas():
    connString = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
    thematic_dir = DATA_DIR

    # Open database        
    dsOut = ogr.Open(connString)
    if dsOut is None:
        print("Could not open PostGIS Database " + connString)
        return

    shp_list = sorted(glob.glob(thematic_dir + '*.shp'))
    for shapefile in shp_list:
        print(shapefile)

        if (shapefile == "./capas-tematicas/cr_provincias_wgs84_snit_ign_2019.shp"):
            layerName = "provincias"
            thematicAreaNameField = "nom_prov"
        elif (shapefile == "./capas-tematicas/cr_cantones_wgs84_snit_ign_2019.shp"):
            layerName = "cantones"
            thematicAreaNameField = "nom_cant"
        elif (shapefile == "./capas-tematicas/cr_distritos_wgs84_snit_ign_2019.shp"):
            layerName = "distritos"
            thematicAreaNameField = "nom_distr"
        elif (shapefile == "./capas-tematicas/cr_acons_wgs84_snit_sinac_2019.shp"):
            layerName = "areas_conservacion"
            thematicAreaNameField = "nombre_ac"
        elif (shapefile == "./capas-tematicas/cr_aprot_wgs84_snit_sinac_2019.shp"):
            layerName = "areas_protegidas"
            thematicAreaNameField = "nombre_asp"
        elif (shapefile == "./capas-tematicas/cr_cbiol_wgs84_fonafifo_2019.shp"):
            layerName = "corredores_biologicos"
            thematicAreaNameField = "nombre"
        elif (shapefile == "./capas-tematicas/cr_vcons_wgs84_fonafifo_2019.shp"):
            layerName = "vacios_conservacion"
            thematicAreaNameField = "desc_bloqu"
        elif (shapefile == "./capas-tematicas/cr_tindig_wgs84_fonafifo_2019.shp"):
            layerName = "territorios_indigenas"
            thematicAreaNameField = "nombre"
        elif (shapefile == "./capas-tematicas/cr_pobtipobosque_wgs84_fonafifo_2019.shp"):
            layerName = "poblacion_tipobosque"
            thematicAreaNameField = "DESCRIPC"
        elif (shapefile == "./capas-tematicas/cr_psa2018_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2018"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2017_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2017"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2016_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2016"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2015_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2015"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2014_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2014"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2013_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2013"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_psa2012_wgs84_fonafifo_2019.shp"):
            layerName = "psa_2012"
            thematicAreaNameField = "contrato"
        elif (shapefile == "./capas-tematicas/cr_refclima_wgs84_fonafifo_2019.shp"):
            layerName = "refugios_climaticos"
            thematicAreaNameField = "Id"
        elif (shapefile == "./capas-tematicas/cr_zonasvida_wgs84_atlasdigital_2019.shp"):
            layerName = "zonas_vida"
            thematicAreaNameField = "NOMBRE"
        elif (shapefile == "./capas-tematicas/cr_unidfito_wgs84_atlasdigital_2019.shp"):
            layerName = "unidades_fitogeograficas"
            thematicAreaNameField = "DESCRIP"
        elif (shapefile == "./capas-tematicas/cr_humedales_wgs84_snit_sinac_2019.shp"):
            layerName = "humedales"
            thematicAreaNameField = "nom_hum"
        print(layerName)
        print(thematicAreaNameField)

        # Open shapefile with thematic areas
        inShapefile  = shapefile
        driver       = ogr.GetDriverByName("ESRI Shapefile")
        dataSource   = driver.Open(inShapefile, 0)
        inLayer      = dataSource.GetLayer()
        
        # Get next "layer_id" value
        query = "SELECT Count(*) FROM layer;"
        print(query)
        ly = dsOut.ExecuteSQL(query)
        feat = ly.GetNextFeature()
        layerCount = feat.GetField(0)
        if layerCount == 0:
            # This is because "last_value" of a sequence returns 1 if there are no rows
            layerId = 1
        else:
            query = "SELECT last_value FROM layer_layer_id_seq;"
            print(query)
            ly = dsOut.ExecuteSQL(query)
            feat = ly.GetNextFeature()
            layerId = feat.GetField(0) + 1

        # Insert record into layer table
        query  = "INSERT INTO layer "
        query += "(name) "
        query += "VALUES('{}');".format(layerName)
        print(query)
        dsOut.ExecuteSQL(query)
        
        # Load thematic area records            
        for feature in inLayer:
            geometry = feature.geometry()
            # if geometry is None or not geometry.IsValid():
            if geometry is None:
                break
            if geometry.GetGeometryType() == ogr.wkbPolygon:
                geometry = ogr.ForceToMultiPolygon(geometry)
            geometryWKT = geometry.ExportToWkt()
            query  = "INSERT INTO thematic_area "
            query += "(layer_id, name, geom) "
            query += "VALUES({}, '{}', ST_GeomFromText('{}', 4326));".format(str(layerId), feature.GetField(thematicAreaNameField), geometryWKT)
            #print(query)
            dsOut.ExecuteSQL(query)

        # Delete invalid geometries
        query = "DELETE FROM thematic_area WHERE layer_id = {} AND NOT ST_IsValid(geom);".format(layerId)
        print(query)
        dsOut.ExecuteSQL(query)
            
    dsOut = None

if __name__ == '__main__':
    start = time.time()
    loadThematicAreas()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
