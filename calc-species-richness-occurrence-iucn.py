from osgeo import ogr
import time


HOST = "localhost"
PORT = "5432"
DATABASE = "biocr20191115"
SCHEMA = "public"
USER = "gisadmin"
PASSWORD = "postgres"


def calcSpeciesRichnessOccurrenceIUCN():
    commands = (
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET mammalia_iucn_threatened_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET mammalia_iucn_threatened_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET reptilia_iucn_threatened_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET reptilia_iucn_threatened_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET amphibia_iucn_threatened_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET amphibia_iucn_threatened_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET aves_iucn_threatened_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET aves_iucn_threatened_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET plantae_iucn_threatened_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND iucn_status IN ('VU', 'EN', 'CR'))
        UPDATE thematic_area
          SET plantae_iucn_threatened_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET all_iucn_threatened_occurrence = 
                mammalia_iucn_threatened_occurrence
              + reptilia_iucn_threatened_occurrence
              + amphibia_iucn_threatened_occurrence	   
              + aves_iucn_threatened_occurrence	   
              + plantae_iucn_threatened_occurrence;
        """,
        """
        UPDATE thematic_area
          SET all_iucn_threatened_occurrence_names = 
              concat_ws(',',mammalia_iucn_threatened_occurrence_names,
                            reptilia_iucn_threatened_occurrence_names,
                            amphibia_iucn_threatened_occurrence_names,
                            aves_iucn_threatened_occurrence_names,
                            plantae_iucn_threatened_occurrence_names);
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
    calcSpeciesRichnessOccurrenceIUCN()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
