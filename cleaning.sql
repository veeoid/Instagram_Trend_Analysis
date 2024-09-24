-- Addresses after cleaning
create table final."Addresses"
(
    address_id   bigint generated always as identity
        constraint "Addresses_pk"
            primary key,
    sid          integer not null,
    zip          text,
    city         text,
    street       text,
    country_code text
);

alter table final."Addresses"
    owner to postgres;

insert into big_data_project.final."Addresses"(
                              sid,
                              zip,
                              city,
                              street,
                              country_code)

select cast(sid as integer),
       zip,
       city,
       street,
       cd
    from big_data_project.temp.locations
where city != '' and street != '' and cd !='';


-- locations after cleaning
create table final."Locations"
(
    location_id bigint
        constraint "Locations_pk"
            primary key,
    address_id  bigint
        constraint "Locations_Addresses_address_id_fk"
            references final."Addresses",
    name        text,
    timestamp   timestamp,
    sid         integer not null
);

alter table final."Locations"
    owner to postgres;


insert into big_data_project.final."Locations"(location_id,
                              address_id,
                              name,
                              timestamp,
                              sid)

select cast(l.id as bigint),
       a.address_id,
       l.name,
       cast(cts as timestamp),
       a.sid
       from big_data_project.temp.locations l
inner join big_data_project.final."Addresses" a
on cast(l.sid as int) = a.sid;


-- Profiles after cleaning
create table final."Profiles"
(
    profile_id          bigint not null
        constraint "Profiles_pk"
            primary key,
    sid                 bigint,
    profile_name        text,
    first_name          text,
    last_name           text,
    n_followers         integer,
    n_posts             integer,
    is_business_account boolean
);

alter table final."Profiles"
    owner to postgres;

insert into big_data_project.final."Profiles"(profile_id,
                             sid,
                             profile_name,
                             name,
                             n_followers,
                             n_posts,
                             is_business_account)
select case when profile_id = ''
        then null
        else cast(profile_id as bigint)
            end ,
       cast(sid as bigint),
    case when profile_name = ''
        then null
        else profile_name
            end,
    case when firstname_lastname = ''
        then null
        else
            firstname_lastname
            end,
    case
        when followers = ''
        then null
        else cast(followers as integer)
        end,
    case
        when n_posts = ''
        then null
        else cast(n_posts as integer)
        end,
    case when is_business_account = ''
         then null
         else cast(is_business_account as boolean)
        end
    from big_data_project.temp.profiles;


-- posts
create table final."Posts"
(
    post_id      text,
    location_id  bigint not null,
    profile_id   bigint    not null,
    sid          bigint not null,
    sid_profiles bigint,
    post_type    integer,
    description  text,
    numbr_likes  integer,
    timestamp    timestamp
);

alter table final."Posts"
    owner to postgres;

insert into big_data_project.final."Posts"(post_id,
                          location_id,
                          profile_id,
                          sid,
                          sid_profiles,
                          post_type,
                          description,
                          numbr_likes,
                          "timestamp")
select post_id,
        cast(location_id as bigint),
       cast(profile_id as bigint),
       cast(sid as bigint),
       cast(sid_profile as bigint),
       cast(post_type as integer),
       description,
       cast(numbr_likes as integer),
       cast(cts as timestamp)
    from big_data_project.temp.posts
where location_id is not null and profile_id is not null
and cast(location_id as bigint) in
    (select cast(location_id as bigint) from final."Locations");



