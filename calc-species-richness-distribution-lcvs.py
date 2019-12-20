from osgeo import ogr
import time


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"


def calcSpeciesRichnessDistributionLCVS():
    commands = (
        """
        UPDATE thematic_area
          SET mammalia_lcvs_pe_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET mammalia_lcvs_pr_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET mammalia_lcvs_pe_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET mammalia_lcvs_pr_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Mammalia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_lcvs_pe_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_lcvs_pr_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_lcvs_pe_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET reptilia_lcvs_pr_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Reptilia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_lcvs_pe_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_lcvs_pr_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_lcvs_pe_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET amphibia_lcvs_pr_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Amphibia' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_lcvs_pe_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_lcvs_pr_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_lcvs_pe_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET aves_lcvs_pr_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE class = 'Aves' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_pe_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_pr_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_ve_distribution = (
            SELECT Count(DISTINCT scientific_name)
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('VE')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_pe_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PE')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_pr_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('PR')
          );
        """,
        """
        UPDATE thematic_area
          SET plantae_lcvs_ve_distribution_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM taxon_distribution d
            WHERE kingdom = 'Plantae' AND ST_Intersects(thematic_area.geom, d.geom) AND lcvs_status IN ('VE')
          );
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pe_distribution = 
                mammalia_lcvs_pe_distribution
              + reptilia_lcvs_pe_distribution
              + amphibia_lcvs_pe_distribution	   
              + aves_lcvs_pe_distribution	   
              + plantae_lcvs_pe_distribution;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pr_distribution = 
                mammalia_lcvs_pr_distribution
              + reptilia_lcvs_pr_distribution
              + amphibia_lcvs_pr_distribution	   
              + aves_lcvs_pr_distribution	   
              + plantae_lcvs_pr_distribution;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_ve_distribution = plantae_lcvs_ve_distribution;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pe_distribution_names = 
              concat_ws(',',mammalia_lcvs_pe_distribution_names,
                            reptilia_lcvs_pe_distribution_names,
                            amphibia_lcvs_pe_distribution_names,
                            aves_lcvs_pe_distribution_names,
                            plantae_lcvs_pe_distribution_names);
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pr_distribution_names = 
              concat_ws(',',mammalia_lcvs_pr_distribution_names,
                            reptilia_lcvs_pr_distribution_names,
                            amphibia_lcvs_pr_distribution_names,
                            aves_lcvs_pr_distribution_names,
                            plantae_lcvs_pr_distribution_names);
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_ve_distribution_names = 
              concat_ws(',',plantae_lcvs_ve_distribution_names);
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
    calcSpeciesRichnessDistributionLCVS()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
