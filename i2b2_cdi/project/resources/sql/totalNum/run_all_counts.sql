CREATE OR REPLACE FUNCTION runtotalnum(observationTable text, schemaName text, tableName text default '@')
  RETURNS void AS
$BODY$
DECLARE 
    curRecord RECORD;
    v_sqlstring text = '';
    v_union text = '';
    v_numpats integer;
    v_startime timestamp;
    v_duration text = '';
    denom int;
begin
    raise info 'At %, running RunTotalnum()',clock_timestamp();
    v_startime := clock_timestamp();

    for curRecord IN 
        select distinct c_table_name as sqltext
        from TABLE_ACCESS 
        where c_visualattributes like '%A%' 
    LOOP 
        raise info 'At %: Running: %',clock_timestamp(), curRecord.sqltext;

        IF tableName='@' OR tableName=curRecord.sqltext THEN
            v_sqlstring := 'select  PAT_COUNT_VISITS( '''||curRecord.sqltext||''' ,'''||schemaName||'''   )';
            execute v_sqlstring;
            v_duration := clock_timestamp()-v_startime;
            raise info '(BENCH) %,PAT_COUNT_VISITS,%',curRecord,v_duration;
            v_startime := clock_timestamp();
            
            v_sqlstring := 'select PAT_COUNT_DIMENSIONS( '''||curRecord.sqltext||''' ,'''||schemaName||''' , '''||observationTable||''' ,  ''concept_cd'', ''concept_dimension'', ''concept_path''  )';
            execute v_sqlstring;
            v_duration :=  clock_timestamp()-v_startime;
            raise info '(BENCH) %,PAT_COUNT_concept_dimension,%',curRecord,v_duration;
            v_startime := clock_timestamp();
            
            v_sqlstring := 'select PAT_COUNT_DIMENSIONS( '''||curRecord.sqltext||''' ,'''||schemaName||''' , '''||observationTable||''' ,  ''provider_id'', ''provider_dimension'', ''provider_path''  )';
            execute v_sqlstring;
            v_duration := clock_timestamp()-v_startime;
            raise info '(BENCH) %,PAT_COUNT_provider_dimension,%',curRecord,v_duration;
            v_startime := clock_timestamp();
            
            v_sqlstring := 'select PAT_COUNT_DIMENSIONS( '''||curRecord.sqltext||''' ,'''||schemaName||''' , '''||observationTable||''' ,  ''modifier_cd'', ''modifier_dimension'', ''modifier_path''  )';
            execute v_sqlstring;
            v_duration := clock_timestamp()-v_startime;
            raise info '(BENCH) %,PAT_COUNT_modifier_dimension,%',curRecord,v_duration;
            v_startime := clock_timestamp();
            
             -- New 11/20 - update counts in top levels (table_access) at the end
             execute 'update table_access set c_totalnum=(select c_totalnum from ' || curRecord.sqltext || ' x where x.c_fullname=table_access.c_fullname)';
             -- Null out cases that are actually 0 [1/21]
            execute  'update  ' || curRecord.sqltext || ' set c_totalnum=null where c_totalnum=0 and c_visualattributes like ''C%''';

        END IF;

    END LOOP;
    
      -- Cleanup (1/21)
      update table_access set c_totalnum=null where c_totalnum=0;
      -- Denominator (1/21)
      SELECT count(*) into denom from totalnum where c_fullname='\denominator\facts\' and agg_date=CURRENT_DATE;
      IF denom = 0
      THEN
          execute 'insert into totalnum(c_fullname,agg_date,agg_count,typeflag_cd)
              select ''\denominator\facts\'',CURRENT_DATE,count(distinct patient_num),''PX'' from ' || lower(schemaName) || '.'|| observationTable ;
      END IF;
    
    perform BuildTotalnumReport(10, 6.5);
    
end; 
$BODY$
  LANGUAGE plpgsql VOLATILE SECURITY DEFINER
  COST 100;
