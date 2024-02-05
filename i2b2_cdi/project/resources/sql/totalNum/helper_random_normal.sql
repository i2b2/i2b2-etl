CREATE OR REPLACE FUNCTION random_normal(
    mean DOUBLE PRECISION DEFAULT 0.0,
    stddev DOUBLE PRECISION DEFAULT 1.0,
    threshold integer default 10
    ) RETURNS DOUBLE PRECISION
      RETURNS NULL ON NULL INPUT AS $BODY$
        DECLARE
            u DOUBLE PRECISION;
            v DOUBLE PRECISION;
            s DOUBLE PRECISION;
        BEGIN
            WHILE true LOOP
           
                u = RANDOM() * 2 - 1; -- range: -1.0 <= u < 1.0
                v = RANDOM() * 2 - 1; -- range: -1.0 <= v < 1.0
                s = u^2 + v^2;

                IF s != 0.0 AND s < 1.0 THEN
                    s = SQRT(-2 * LN(s) / s);
    
                    IF stddev * s * u > threshold THEN 
                        RETURN  mean + threshold;
                    ELSIF stddev * s * u < -1 * threshold THEN 
                        RETURN  mean - threshold;
                    ELSE
                        RETURN  mean + stddev * s * u;
                    END IF;
                    
                END IF;
            END LOOP;
        END;
$BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
