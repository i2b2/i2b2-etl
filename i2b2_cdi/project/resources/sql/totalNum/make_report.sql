CREATE OR REPLACE FUNCTION BuildTotalnumReport(threshold int, sigma float) RETURNS void AS
$BODY$
BEGIN

    truncate table totalnum_report;

    insert into totalnum_report(c_fullname, agg_count, agg_date)
     select c_fullname, case sign(agg_count - threshold + 1 ) when 1 then (round(agg_count/5.0,0)*5)+round(random_normal(0,sigma,threshold)) else -1 end agg_count, 
       to_char(agg_date,'YYYY-MM-DD') agg_date from 
       (select * from 
           (select row_number() over (partition by c_fullname order by agg_date desc) rn,c_fullname, agg_count,agg_date from totalnum where typeflag_cd like 'P%') x where rn=1) y;

    update totalnum_report set agg_count=-1 where agg_count<threshold;

END;
$BODY$
 LANGUAGE plpgsql VOLATILE SECURITY DEFINER;