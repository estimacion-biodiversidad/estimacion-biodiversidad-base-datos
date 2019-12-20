from osgeo import ogr
import time


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"


def calcSpeciesRichnessDistribution():
    commands = (
        """
        UPDATE thematic_area
          SET mammalia_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET mammalia_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET aves_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET aves_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET all_distribution = 
                mammalia_distribution
              + reptilia_distribution
              + amphibia_distribution	   
              + aves_distribution	   
              + plantae_distribution;
        """,
        """
        UPDATE thematic_area
          SET all_distribution_names = 
              concat_ws(',',mammalia_distribution_names,
                            reptilia_distribution_names,
                            amphibia_distribution_names,
                            aves_distribution_names,
                            plantae_distribution_names);
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
    calcSpeciesRichnessDistribution()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
