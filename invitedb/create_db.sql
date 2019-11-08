create table archive_types
(
    id          serial not null
        constraint archive_types_pk
            primary key,
    type        text   not null,
    description text
);

alter table archive_types
    owner to postgres;

create unique index archive_types_id_uindex
    on archive_types (id);

create unique index archive_types_type_uindex
    on archive_types (type);

create table invitations
(
    creator_name  text                  not null,
    creator_email text                  not null,
    uuid          uuid                  not null,
    sensitive     boolean default false not null,
    archive_type  text                  not null,
    id            serial                not null
        constraint invitations_pk
            primary key
);

alter table invitations
    owner to postgres;

create unique index invitations_uuid_uindex
    on invitations (uuid);

create unique index invitations_id_uindex
    on invitations (id);

