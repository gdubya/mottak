create table archive_id
(
    id          serial       not null
        constraint archive_types_pk
            primary key,
    type        text         not null,
    description text,
    created_at  timestamp(0) not null,
    updated_at  timestamp(0) not null
);

alter table archive_id
    owner to postgres;

create table invitations
(
    creator_name  text                  not null,
    creator_email text                  not null,
    uuid          uuid                  not null,
    sensitive     boolean default false not null,
    archive_id    integer               not null
        constraint invitations_archive_id_id_fk
            references archive_id,
    id            serial                not null
        constraint invitations_pk
            primary key,
    created_at    timestamp(0)          not null,
    updated_at    timestamp(0)          not null,
    checksum      text                  not null
);

alter table invitations
    owner to postgres;

create unique index invitations_uuid_uindex
    on invitations (uuid);

create unique index invitations_id_uindex
    on invitations (id);

create unique index archive_types_id_uindex
    on archive_id (id);

create unique index archive_types_type_uindex
    on archive_id (type);

