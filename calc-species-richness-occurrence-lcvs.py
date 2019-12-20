from osgeo import ogr
import time


HOST = "<HOST>"
PORT = "<PORT>"
DATABASE = "<DATABASE>"
SCHEMA = "<SCHEMA>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"


def calcSpeciesRichnessOccurrenceLCVS():
    commands = (
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET mammalia_lcvs_pe_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET mammalia_lcvs_pr_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET mammalia_lcvs_pe_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Mammalia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET mammalia_lcvs_pr_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET reptilia_lcvs_pe_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET reptilia_lcvs_pr_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET reptilia_lcvs_pe_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Reptilia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET reptilia_lcvs_pr_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET amphibia_lcvs_pe_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET amphibia_lcvs_pr_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET amphibia_lcvs_pe_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Amphibia' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET amphibia_lcvs_pr_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET aves_lcvs_pe_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET aves_lcvs_pr_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET aves_lcvs_pe_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE class='Aves' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET aves_lcvs_pr_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );

        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET plantae_lcvs_pe_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET plantae_lcvs_pr_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('VE'))
        UPDATE thematic_area
          SET plantae_lcvs_ve_occurrence = (
            SELECT Count(DISTINCT scientific_name)
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('PE'))
        UPDATE thematic_area
          SET plantae_lcvs_pe_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('PR'))
        UPDATE thematic_area
          SET plantae_lcvs_pr_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        WITH occ AS (SELECT DISTINCT scientific_name, geom FROM taxon_occurrence WHERE kingdom='Plantae' AND lcvs_status IN ('VE'))
        UPDATE thematic_area
          SET plantae_lcvs_ve_occurrence_names = (
            SELECT String_agg(DISTINCT scientific_name, ',')
            FROM occ
            WHERE ST_Contains(thematic_area.geom, occ.geom)
          );
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pe_occurrence = 
                mammalia_lcvs_pe_occurrence
              + reptilia_lcvs_pe_occurrence
              + amphibia_lcvs_pe_occurrence	   
              + aves_lcvs_pe_occurrence	   
              + plantae_lcvs_pe_occurrence;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pr_occurrence = 
                mammalia_lcvs_pr_occurrence
              + reptilia_lcvs_pr_occurrence
              + amphibia_lcvs_pr_occurrence	   
              + aves_lcvs_pr_occurrence	   
              + plantae_lcvs_pr_occurrence;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_ve_occurrence = plantae_lcvs_ve_occurrence;
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pe_occurrence_names = 
              concat_ws(',',mammalia_lcvs_pe_occurrence_names,
                            reptilia_lcvs_pe_occurrence_names,
                            amphibia_lcvs_pe_occurrence_names,
                            aves_lcvs_pe_occurrence_names,
                            plantae_lcvs_pe_occurrence_names);
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_pr_occurrence_names = 
              concat_ws(',',mammalia_lcvs_pr_occurrence_names,
                            reptilia_lcvs_pr_occurrence_names,
                            amphibia_lcvs_pr_occurrence_names,
                            aves_lcvs_pr_occurrence_names,
                            plantae_lcvs_pr_occurrence_names);
        """,
        """
        UPDATE thematic_area
          SET all_lcvs_ve_occurrence_names = 
              concat_ws(',',plantae_lcvs_ve_occurrence_names);
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
    calcSpeciesRichnessOccurrenceLCVS()       
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
