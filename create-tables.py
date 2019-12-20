import psycopg2 as pg
import time


HOST = "localhost"
PORT = "5432"
DATABASE = "biocr20191115"
USER = "gisadmin"
PASSWORD = "postgres"


def create_tables():
    commands = (
        """
        DROP TABLE IF EXISTS layer CASCADE;
        """,
        """
        CREATE TABLE layer (
            layer_id SERIAL PRIMARY KEY,
            name     TEXT
        );
        """,
        """
        DROP TABLE IF EXISTS thematic_area;
        """,
        """
        CREATE TABLE thematic_area (
            thematic_area_id                            SERIAL PRIMARY KEY,
            layer_id                                    INTEGER REFERENCES layer(layer_id),        
            name                                        TEXT,
            all_occurrence                              INTEGER DEFAULT 0,
            all_occurrence_names                        TEXT,
            all_distribution                            INTEGER DEFAULT 0,
            all_distribution_names                      TEXT,
            mammalia_occurrence                         INTEGER DEFAULT 0,
            mammalia_occurrence_names                   TEXT,
            mammalia_distribution                       INTEGER DEFAULT 0,
            mammalia_distribution_names                 TEXT,
            aves_occurrence                             INTEGER DEFAULT 0,
            aves_occurrence_names                       TEXT,
            aves_distribution                           INTEGER DEFAULT 0,
            aves_distribution_names                     TEXT,
            reptilia_occurrence                         INTEGER DEFAULT 0,
            reptilia_occurrence_names                   TEXT,
            reptilia_distribution                       INTEGER DEFAULT 0,
            reptilia_distribution_names                 TEXT,
            amphibia_occurrence                         INTEGER DEFAULT 0,
            amphibia_occurrence_names                   TEXT,
            amphibia_distribution                       INTEGER DEFAULT 0,
            amphibia_distribution_names                 TEXT,
            plantae_occurrence                          INTEGER DEFAULT 0,
            plantae_occurrence_names                    TEXT,
            plantae_distribution                        INTEGER DEFAULT 0,
            plantae_distribution_names                  TEXT,
            all_iucn_threatened_occurrence              INTEGER DEFAULT 0,
            all_iucn_threatened_occurrence_names        TEXT,
            all_iucn_threatened_distribution            INTEGER DEFAULT 0,
            all_iucn_threatened_distribution_names      TEXT,		
            mammalia_iucn_threatened_occurrence         INTEGER DEFAULT 0,
            mammalia_iucn_threatened_occurrence_names   TEXT,
            mammalia_iucn_threatened_distribution       INTEGER DEFAULT 0,
            mammalia_iucn_threatened_distribution_names TEXT,		
            aves_iucn_threatened_occurrence             INTEGER DEFAULT 0,
            aves_iucn_threatened_occurrence_names       TEXT,
            aves_iucn_threatened_distribution           INTEGER DEFAULT 0,
            aves_iucn_threatened_distribution_names     TEXT,		
            reptilia_iucn_threatened_occurrence         INTEGER DEFAULT 0,
            reptilia_iucn_threatened_occurrence_names   TEXT,
            reptilia_iucn_threatened_distribution       INTEGER DEFAULT 0,
            reptilia_iucn_threatened_distribution_names TEXT,		
            amphibia_iucn_threatened_occurrence         INTEGER DEFAULT 0,
            amphibia_iucn_threatened_occurrence_names   TEXT,
            amphibia_iucn_threatened_distribution       INTEGER DEFAULT 0,
            amphibia_iucn_threatened_distribution_names TEXT,		
            plantae_iucn_threatened_occurrence          INTEGER DEFAULT 0,
            plantae_iucn_threatened_occurrence_names    TEXT,
            plantae_iucn_threatened_distribution        INTEGER DEFAULT 0,
            plantae_iucn_threatened_distribution_names  TEXT,
            all_lcvs_pe_occurrence                      INTEGER DEFAULT 0,
            all_lcvs_pr_occurrence                      INTEGER DEFAULT 0,
            all_lcvs_ve_occurrence                      INTEGER DEFAULT 0,                                
            all_lcvs_pe_occurrence_names                TEXT,
            all_lcvs_pr_occurrence_names                TEXT,
            all_lcvs_ve_occurrence_names                TEXT,
            all_lcvs_pe_distribution                    INTEGER DEFAULT 0,
            all_lcvs_pr_distribution                    INTEGER DEFAULT 0,
            all_lcvs_ve_distribution                    INTEGER DEFAULT 0,
            all_lcvs_pe_distribution_names              TEXT,
            all_lcvs_pr_distribution_names              TEXT,
            all_lcvs_ve_distribution_names              TEXT,								
            mammalia_lcvs_pe_occurrence                 INTEGER DEFAULT 0,
            mammalia_lcvs_pr_occurrence                 INTEGER DEFAULT 0,
            mammalia_lcvs_pe_occurrence_names           TEXT,
            mammalia_lcvs_pr_occurrence_names           TEXT,
            mammalia_lcvs_pe_distribution               INTEGER DEFAULT 0,
            mammalia_lcvs_pr_distribution               INTEGER DEFAULT 0,
            mammalia_lcvs_pe_distribution_names         TEXT,
            mammalia_lcvs_pr_distribution_names         TEXT,				
            aves_lcvs_pe_occurrence                     INTEGER DEFAULT 0,
            aves_lcvs_pr_occurrence                     INTEGER DEFAULT 0,
            aves_lcvs_pe_occurrence_names               TEXT,
            aves_lcvs_pr_occurrence_names               TEXT,
            aves_lcvs_pe_distribution                   INTEGER DEFAULT 0,
            aves_lcvs_pr_distribution                   INTEGER DEFAULT 0,
            aves_lcvs_pe_distribution_names             TEXT,
            aves_lcvs_pr_distribution_names             TEXT,				
            reptilia_lcvs_pe_occurrence                 INTEGER DEFAULT 0,
            reptilia_lcvs_pr_occurrence                 INTEGER DEFAULT 0,
            reptilia_lcvs_pe_occurrence_names           TEXT,
            reptilia_lcvs_pr_occurrence_names           TEXT,
            reptilia_lcvs_pe_distribution               INTEGER DEFAULT 0,
            reptilia_lcvs_pr_distribution               INTEGER DEFAULT 0,
            reptilia_lcvs_pe_distribution_names         TEXT,
            reptilia_lcvs_pr_distribution_names         TEXT,				
            amphibia_lcvs_pe_occurrence                 INTEGER DEFAULT 0,
            amphibia_lcvs_pr_occurrence                 INTEGER DEFAULT 0,
            amphibia_lcvs_pe_occurrence_names           TEXT,
            amphibia_lcvs_pr_occurrence_names           TEXT,
            amphibia_lcvs_pe_distribution               INTEGER DEFAULT 0,
            amphibia_lcvs_pr_distribution               INTEGER DEFAULT 0,
            amphibia_lcvs_pe_distribution_names         TEXT,
            amphibia_lcvs_pr_distribution_names         TEXT,				
            plantae_lcvs_pe_occurrence                  INTEGER DEFAULT 0,
            plantae_lcvs_pr_occurrence                  INTEGER DEFAULT 0,
            plantae_lcvs_ve_occurrence                  INTEGER DEFAULT 0,
            plantae_lcvs_pe_occurrence_names            TEXT,
            plantae_lcvs_pr_occurrence_names            TEXT,
            plantae_lcvs_ve_occurrence_names            TEXT,
            plantae_lcvs_pe_distribution                INTEGER DEFAULT 0,
            plantae_lcvs_pr_distribution                INTEGER DEFAULT 0,
            plantae_lcvs_ve_distribution                INTEGER DEFAULT 0,
            plantae_lcvs_pe_distribution_names          TEXT,
            plantae_lcvs_pr_distribution_names          TEXT,
            plantae_lcvs_ve_distribution_names          TEXT				
        );
        """,
        """
        SELECT AddGeometryColumn('public', 'thematic_area', 'geom', 4326, 'MULTIPOLYGON', 2);
        """,
        """
        CREATE INDEX idx_thematic_area_geom ON thematic_area USING gist(geom);
        """,
        """
        DROP TABLE IF EXISTS taxon_occurrence;
        """,
        """
        CREATE TABLE taxon_occurrence (
            kingdom         TEXT,		 
            phylum          TEXT,		        
            class           TEXT,		
            "order"         TEXT,		
            family          TEXT,		
            genus           TEXT,		        
            scientific_name TEXT,
            iucn_status     CHAR(2),		
            lcvs_status     CHAR(2)
        );
        """,
        """
        SELECT AddGeometryColumn ('public', 'taxon_occurrence', 'geom', 4326, 'POINT', 2);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_kingdom         ON taxon_occurrence (kingdom);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_phylum          ON taxon_occurrence (phylum);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_class           ON taxon_occurrence (class);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_order           ON taxon_occurrence ("order");
        """,
        """
        CREATE INDEX idx_taxon_occurrence_family          ON taxon_occurrence (family);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_genus           ON taxon_occurrence (genus);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_scientific_name ON taxon_occurrence (scientific_name);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_iucn_status     ON taxon_occurrence (iucn_status);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_lcvs_status     ON taxon_occurrence (lcvs_status);
        """,
        """
        CREATE INDEX idx_taxon_occurrence_geom            ON taxon_occurrence USING gist(geom);
        """,
        """
        DROP TABLE IF EXISTS taxon_distribution;
        """,
        """
        CREATE TABLE taxon_distribution (
            kingdom          TEXT,
            phylum           TEXT,
            class            TEXT,
            "order"          TEXT,
            family           TEXT,
            genus            TEXT,
            scientific_name  TEXT,
            iucn_status      CHAR(2),
            lcvs_status      CHAR(2)
        );
        """,
        """
        SELECT AddGeometryColumn ('public', 'taxon_distribution', 'geom', 4326, 'MULTIPOLYGON', 2);
        """,
        """
        CREATE INDEX idx_taxon_distribution_kingdom         ON taxon_distribution (kingdom);
        """,
        """
        CREATE INDEX idx_taxon_distribution_phylum          ON taxon_distribution (phylum);
        """,
        """
        CREATE INDEX idx_taxon_distribution_class           ON taxon_distribution (class);
        """,
        """
        CREATE INDEX idx_taxon_distribution_order           ON taxon_distribution ("order");
        """,
        """
        CREATE INDEX idx_taxon_distribution_family          ON taxon_distribution (family);
        """,
        """
        CREATE INDEX idx_taxon_distribution_genus           ON taxon_distribution (genus);
        """,
        """
        CREATE INDEX idx_taxon_distribution_scientific_name ON taxon_distribution (scientific_name);
        """,
        """
        CREATE INDEX idx_taxon_distribution_iucn_status     ON taxon_distribution (iucn_status);
        """,
        """
        CREATE INDEX idx_taxon_distribution_lcvs_status     ON taxon_distribution (lcvs_status);
        """,
        """
        CREATE INDEX idx_taxon_distribution_geom            ON taxon_distribution USING gist(geom);
        """)
    try:
        conn = pg.connect("host='" + HOST + "' port=" + PORT + " dbname=" + DATABASE + " user=" + USER + " password=" + PASSWORD)

        cur = conn.cursor()
        for command in commands:
            print(command)
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()    

if __name__ == '__main__':
    start = time.time()
    create_tables()
    end = time.time()

    print("Tiempo de inicio:", start)
    print("Tiempo de finalización:", end)
    print("Tiempo de ejecución:", end - start, "segundos")
