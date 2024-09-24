-- We used this query to limit our data as our hardware wasn't able to process
-- such huge data.
create table final.tempPosts as select * from final."Posts"
where sid_profiles != -1;


-- We used this query to find out distinct city names and country code
-- in frequent item set mining
select distinct a.city, a.country_code from final."Locations" l
         inner join final."Addresses" a
         on l.address_id = a.address_id
where location_id in (select location1 from l3
                                       union
                    select location2 from l3
                                        union
                        select location3 from l3);