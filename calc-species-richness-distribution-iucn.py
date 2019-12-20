from osgeo import ogr
import time


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"


def calcSpeciesRichnessDistributionIUCN():
    commands = (
        """
        UPDATE thematic_area
          SET mammalia_iucn_threatened_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET mammalia_iucn_threatened_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_iucn_threatened_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_iucn_threatened_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_iucn_threatened_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_iucn_threatened_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_iucn_threatened_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_iucn_threatened_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_iucn_threatened_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_iucn_threatened_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND iucn_status IN ('VU', 'EN', 'CR')
          );
        """,
        """
        UPDATE thematic_area
          SET all_iucn_threatened_distribution = 
                mammalia_iucn_threatened_distribution
              + reptilia_iucn_threatened_distribution
              + amphibia_iucn_threatened_distribution	   
              + aves_iucn_threatened_distribution	   
              + plantae_iucn_threatened_distribution;
        """,
        """
        UPDATE thematic_area
          SET all_iucn_threatened_distribution_names = 
              concat_ws(',',mammalia_iucn_threatened_distribution_names,
                            reptilia_iucn_threatened_distribution_names,
                            amphibia_iucn_threatened_distribution_names,
                            aves_iucn_threatened_distribution_names,
                            plantae_iucn_threatened_distribution_names);
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
    calcSpeciesRichnessDistributionIUCN()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
