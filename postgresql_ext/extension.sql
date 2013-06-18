-- Table: layer_metadata

DROP TABLE IF EXISTS layer_metadata;

CREATE TABLE layer_metadata
(
  f_table_catalog character varying(256) NOT NULL,
  f_table_schema character varying(256) NOT NULL,
  f_table_name character varying(256) NOT NULL,
  metadata xml,
  CONSTRAINT layer_metadata_pk PRIMARY KEY (f_table_catalog, f_table_schema, f_table_name)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE layer_metadata OWNER TO postgres;
GRANT ALL ON TABLE layer_metadata TO postgres;

-- GRANT ALL ON TABLE layer_metadata TO "GisAdmin";
-- GRANT ALL ON TABLE layer_metadata TO "GisUser";




-- Function: addlayermetadata(character varying, character varying, character varying, character varying, integer, character varying, integer)
-- DROP FUNCTION addlayermetadata(character varying, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION addlayermetadata(character varying, character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    catalog_name alias for $1;
    schema_name alias for $2;
    table_name alias for $3;
    meta_text alias for $4;

    -- meta_xml xml;
    real_schema name;
    sql text;
BEGIN
    -- Verify schema
    IF ( schema_name IS NOT NULL AND schema_name != '' ) THEN
        sql := 'SELECT nspname FROM pg_namespace ' ||
            'WHERE text(nspname) = ' || quote_literal(schema_name) ||
            'LIMIT 1';
        RAISE DEBUG '%', sql;
        EXECUTE sql INTO real_schema;

        IF ( real_schema IS NULL ) THEN
            RAISE EXCEPTION 'Schema % is not a valid schemaname', quote_literal(schema_name);
            RETURN 'fail';
        END IF;
    END IF;

    IF ( real_schema IS NULL ) THEN
        RAISE DEBUG 'Detecting schema';
        sql := 'SELECT n.nspname AS schemaname ' ||
            'FROM pg_catalog.pg_class c ' ||
              'JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace ' ||
            'WHERE c.relkind = ' || quote_literal('r') ||
            ' AND n.nspname NOT IN (' || quote_literal('pg_catalog') || ', ' || quote_literal('pg_toast') || ')' ||
            ' AND pg_catalog.pg_table_is_visible(c.oid)' ||
            ' AND c.relname = ' || quote_literal(table_name);
        RAISE DEBUG '%', sql;
        EXECUTE sql INTO real_schema;

        IF ( real_schema IS NULL ) THEN
            RAISE EXCEPTION 'Table % does not occur in the search_path', quote_literal(table_name);
            RETURN 'fail';
        END IF;
    END IF;

    -- Validate XML
    --not need
    --meta_xml := XMLPARSE( DOCUMENT meta_text);

    -- Delete stale record in layer_metadata (if any)
    sql := 'DELETE FROM layer_metadata WHERE
        f_table_catalog = ' || quote_literal('') ||
        ' AND f_table_schema = ' ||
        quote_literal(real_schema) ||
        ' AND f_table_name = ' || quote_literal(table_name);
    RAISE DEBUG '%', sql;
    EXECUTE sql;


    -- Add record in layer_metadata
    sql := 'INSERT INTO layer_metadata (f_table_catalog,f_table_schema,f_table_name,metadata)' ||
                       ' VALUES (' ||
                                   quote_literal('') || ',' ||
                                   quote_literal(real_schema) || ',' ||
                                   quote_literal(table_name) || ',' ||
                                   'XMLPARSE( DOCUMENT ' || quote_literal(meta_text) || ') )';
    RAISE DEBUG '%', sql;
    EXECUTE sql;

    RETURN
        real_schema || '.' ||
        table_name;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION addlayermetadata(character varying, character varying, character varying, character varying) OWNER TO postgres;



-- Function: addlayermetadata(character varying, character varying, character varying)

-- DROP FUNCTION addlayermetadata(character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION addlayermetadata(character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT addlayermetadata('',$1,$2,$3) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION addlayermetadata(character varying, character varying, character varying) OWNER TO postgres;



-- Function: addlayermetadata(character varying, character varying)

-- DROP FUNCTION addlayermetadata(character varying, character varying);

CREATE OR REPLACE FUNCTION addlayermetadata(character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT addlayermetadata('', '', $1,$2) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION addlayermetadata(character varying, character varying) OWNER TO postgres;









-- Function: droplayermetadata(character varying, character varying, character varying)

-- DROP FUNCTION droplayermetadata(character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION droplayermetadata(character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    catalog_name alias for $1;
    schema_name alias for $2;
    table_name alias for $3;
    real_schema name;

BEGIN

    IF ( schema_name = '' ) THEN
        SELECT current_schema() into real_schema;
    ELSE
        real_schema = schema_name;
    END IF;

    -- Remove refs from layer_metadata table
    EXECUTE 'DELETE FROM layer_metadata WHERE ' ||
        'f_table_schema = ' || quote_literal(real_schema) ||
        ' AND ' ||
        ' f_table_name = ' || quote_literal(table_name);
    RETURN
        'Metadata for ' || real_schema || '.' ||
        table_name ||' dropped.';

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION droplayermetadata(character varying, character varying, character varying) OWNER TO postgres;


-- Function: droplayermetadata(character varying, character varying)
-- DROP FUNCTION droplayermetadata(character varying, character varying);

CREATE OR REPLACE FUNCTION droplayermetadata(character varying, character varying)
  RETURNS text AS
$BODY$ SELECT droplayermetadata('',$1,$2) $BODY$
  LANGUAGE sql VOLATILE STRICT
  COST 100;
ALTER FUNCTION droplayermetadata(character varying, character varying) OWNER TO postgres;


-- Function: droplayermetadata(character varying)
-- DROP FUNCTION droplayermetadata(character varying);

CREATE OR REPLACE FUNCTION droplayermetadata(character varying)
  RETURNS text AS
$BODY$ SELECT droplayermetadata('','',$1) $BODY$
  LANGUAGE sql VOLATILE STRICT
  COST 100;
ALTER FUNCTION droplayermetadata(character varying) OWNER TO postgres;






-- Function: updatelayermetadata(character varying, character varying, character varying, character varying)

-- DROP FUNCTION updatelayermetadata(character varying, character varying, character varying, character varying);
CREATE OR REPLACE FUNCTION updatelayermetadata(character varying, character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    catalog_name alias for $1;
    schema_name alias for $2;
    table_name alias for $3;
    meta_text alias for $4;

    real_schema name;
    okay boolean;
    myrec RECORD;
BEGIN
    -- Find, check or fix schema_name
    IF ( schema_name != '' ) THEN
        okay = 'f';

        FOR myrec IN SELECT nspname FROM pg_namespace WHERE text(nspname) = schema_name LOOP
            okay := 't';
        END LOOP;

        IF ( okay <> 't' ) THEN
            RAISE EXCEPTION 'Invalid schema name';
        ELSE
            real_schema = schema_name;
        END IF;
    ELSE
        SELECT INTO real_schema current_schema()::text;
    END IF;



    -- Update ref from layer_metadata table
    EXECUTE 'UPDATE layer_metadata SET metadata = XMLPARSE( DOCUMENT '  || quote_literal(meta_text) || ')' ||
        ' where f_table_schema = ' ||
        quote_literal(real_schema) || ' and f_table_name = ' ||
        quote_literal(table_name);

    RETURN real_schema || '.' || table_name || '.' || ' metadata changed';

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION updatelayermetadata(character varying, character varying, character varying, character varying) OWNER TO postgres;






-- Function: updatelayermetadata(character varying, character varying, character varying)

-- DROP FUNCTION updatelayermetadata(character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION updatelayermetadata(character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT updatelayermetadata('',$1,$2,$3) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION updatelayermetadata(character varying, character varying, character varying) OWNER TO postgres;


-- Function: updatelayermetadata(character varying, character varying)
-- DROP FUNCTION updatelayermetadata(character varying, character varying);

CREATE OR REPLACE FUNCTION updatelayermetadata(character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT updatelayermetadata('','',$1,$2) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION updatelayermetadata(character varying, character varying) OWNER TO postgres;
















-- Function: getlayermetadata(character varying, character varying, character varying)

-- DROP FUNCTION getlayermetadata(character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION getlayermetadata(character varying, character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    catalog_name alias for $1;
    schema_name alias for $2;
    table_name alias for $3;

    real_schema name;
    okay boolean;
    myrec RECORD;
    sql text;
    ret text;
BEGIN
    -- Find, check or fix schema_name
    IF ( schema_name != '' ) THEN
        okay = 'f';

        FOR myrec IN SELECT nspname FROM pg_namespace WHERE text(nspname) = schema_name LOOP
            okay := 't';
        END LOOP;

        IF ( okay <> 't' ) THEN
            RAISE EXCEPTION 'Invalid schema name';
        ELSE
            real_schema = schema_name;
        END IF;
    ELSE
        SELECT INTO real_schema current_schema()::text;
    END IF;


    -- Update ref from layer_metadata table
    sql := 'SELECT XMLSERIALIZE(DOCUMENT metadata as TEXT) FROM layer_metadata WHERE ' ||
           'f_table_schema = ' || quote_literal(real_schema) ||
           ' and f_table_name = ' || quote_literal(table_name) || ' LIMIT 1';
    EXECUTE sql INTO ret;
    RETURN ret;
    --RETURN XMLSERIALIZE(DOCUMENT ret as TEXT);

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION getlayermetadata(character varying, character varying, character varying) OWNER TO postgres;





-- Function: getlayermetadata(character varying, character varying)

-- DROP FUNCTION getlayermetadata(character varying, character varying);

CREATE OR REPLACE FUNCTION getlayermetadata(character varying, character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT getlayermetadata('',$1,$2) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION updatelayermetadata(character varying, character varying) OWNER TO postgres;


-- Function: getlayermetadata(character varying)

-- DROP FUNCTION getlayermetadata(character varying);

CREATE OR REPLACE FUNCTION getlayermetadata(character varying)
  RETURNS text AS
$BODY$
DECLARE
    ret  text;
BEGIN
    SELECT getlayermetadata('','',$1) into ret;
    RETURN ret;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION getlayermetadata(character varying) OWNER TO postgres;