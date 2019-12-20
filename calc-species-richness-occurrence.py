from osgeo import ogr
import time


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"


def calcSpeciesRichnessOccurrence():
    commands = (
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia')
        UPDATE thematic_area
          SET mammalia_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia')
        UPDATE thematic_area
          SET mammalia_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia')
        UPDATE thematic_area
          SET reptilia_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia')
        UPDATE thematic_area
          SET reptilia_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia')
        UPDATE thematic_area
          SET amphibia_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia')
        UPDATE thematic_area
          SET amphibia_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves')
        UPDATE thematic_area
          SET aves_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves')
        UPDATE thematic_area
          SET aves_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae')
        UPDATE thematic_area
          SET plantae_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae')
        UPDATE thematic_area
          SET plantae_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET all_occurrence = 
                mammalia_occurrence
              + reptilia_occurrence
              + amphibia_occurrence	   
              + aves_occurrence	   
              + plantae_occurrence;
        """,
        """
        UPDATE thematic_area
          SET all_occurrence_names = 
              concat_ws(',',mammalia_occurrence_names,
                            reptilia_occurrence_names,
                            amphibia_occurrence_names,
                            aves_occurrence_names,
                            plantae_occurrence_names);
        """)
    try:
        conn = "PG: host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " active_schema=" + SCHEMA + " user=" + USER + " password=" + PASSWORD
        ds = ogr.Open(conn)
        for command in commands:
            print(command)
            ds.ExecuteSQL(command)
    except (Exception) as error:
        print(error)
    finally:
        ds = None


if __name__ == '__main__':
    ogr.UseExceptions()

    start = time.time()
    calcSpeciesRichnessOccurrence()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
