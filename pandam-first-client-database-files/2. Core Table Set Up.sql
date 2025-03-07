/*
 Create the DB Schema Tables here
 */
 create table public.users(
     user_id UUID default uuid_generate_v4() primary key,
     first_name varchar(100) not null,
     middle_name varchar(100),
     last_name varchar(100) not null,
     email varchar(100) not null unique,
     username varchar(100) not null unique,
     password bytea not null,
     phone_number varchar(100),
     status varchar(20) default 'active',
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp,
     external_id varchar(255) unique
 );

insert into public.users(first_name, last_name, email, username, password, phone_number)
values ('David', 'Liu', 'ingluvious@icloud.com', 'ingluvious@icloud.com', 'Hello12345', '0221260360');

insert into public.users(first_name, last_name, email, username, password, phone_number)
values ('Jheneene', 'Amor', 'jheneenea@gmail.com', 'jheneenea@gmail.com', 'Hello12345', '0211682063');

select * from public.users;

/*
 Create the Organisation table
 */
 create table organisations(
     org_id UUID default uuid_generate_v4() primary key,
     name varchar(255),
     nzbn varchar(25) unique,
     charity_number varchar(25) unique,
     website varchar(100),
     phone_number varchar(100),
     description varchar(255),
     industry varchar(100),
     sector varchar(100),
     territory varchar(100),
     status varchar(100) check (status in ('Active', 'Closed', 'On Hold', 'Pending')) default 'Active',
     parent_organisation UUID references organisations(org_id),
     external_id varchar(255) unique,
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp
 );
insert into public.organisations (name, nzbn, website, phone_number, description, status)
values ('Marvel - Avengers', '999878945612', 'www.linkedin.com', '0221260360', 'The Avengers Primary Account with Pandam', 'Active');

insert into public.organisations (name, nzbn, website, phone_number, description, status)
values ('Mini Avengers', '999878945613', 'www.linkedin.com', '0221260360', 'The smaller team of the Avengers. Usually called upon to save cats stuck in trees and to find missing coins', 'Active');

insert into public.organisations (name, nzbn, website, phone_number, description, status)
values ('Thippy Time', '999878945614', 'www.linkedin.com', '0221260360', 'Thippys Business', 'Active');

select * from organisations;

/*
 Create the Org-Org relationship table here
 */
 create table org_org_relationship(
     org_relationship_uuid UUID default uuid_generate_v4() primary key,
     org_uuid_one UUID references organisations(org_uuid),
     org_uuid_two UUID references organisations(org_uuid),
     org_one_relationship_type varchar(50),
     org_two_relationship_type varchar(50),
     status varchar(50) check (status in ('Active', 'Not Active', 'Discontinued')) default 'Active',
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp
 );

 insert into org_org_relationship (org_uuid_one, org_uuid_two, org_one_relationship_type, org_two_relationship_type)
 values ('9956a733-1932-41a2-8803-36310e152c82', '6517d8e0-2430-48e5-a026-95b5d22bc4c4', 'Parent Company', 'Subsidiary Company')

 select * from org_org_relationship;

/*
 Create the Contacts table here
 */
 create table contact(
     contact_uuid UUID default uuid_generate_v4() primary key,
     first_name varchar(100),
     last_name varchar(100),
     date_of_birth date,
     email varchar(100),
     additional_email varchar(100),
     mobile varchar(50),
     landline varchar(50),
     linkedin varchar(100),
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp
 );

 insert into public.contact (first_name, last_name, date_of_birth, email, mobile)
 values ('David', 'Liu', '1991-01-01', 'ingluvious@icloud.com', '0221260360');

 insert into public.contact (first_name, last_name, date_of_birth, email, mobile)
 values ('Stephen', 'Strange', '1991-01-01', 'strange@icloud.com', '0221260361');

 select * from contact;

/*
 Create the Org Contact relationship table here
 */
create table org_contact_relationship(
    org_contact_uuid UUID default uuid_generate_v4() primary key,
    contact_uuid UUID references contact(contact_uuid),
    org_uuid UUID references organisations(org_uuid),
    contact_role varchar(255),
    status varchar(50) check (status in ('Active', 'Inactive')) default 'Active',
    _created_at timestamp default current_timestamp,
    _updated_at timestamp default current_timestamp
);

insert into org_contact_relationship (contact_uuid, org_uuid, contact_role)
values ('4278fe7f-1343-43a2-b638-8834a00f878e', '9956a733-1932-41a2-8803-36310e152c82', 'Supreme Overseer');

select * from org_contact_relationship;

/*
 Create the Contact Contact relationship table here
 */
 create table contact_contact_relationship(
     contact_relationship_uuid UUID default uuid_generate_v4() primary key,
     contact_one_uuid UUID references contact(contact_uuid),
     contact_two_uuid UUID references contact(contact_uuid),
     contact_one_role varchar(50),
     contact_two_role varchar(50),
     status varchar(50) check (status in ('Active', 'Inactive')) default 'Active',
     relationship_creation_method varchar(50) check (relationship_creation_method in ('Primary','Inverted')) default 'Primary',
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp
 );

insert into contact_contact_relationship (contact_one_uuid, contact_two_uuid, contact_one_role, contact_two_role)
values ('4278fe7f-1343-43a2-b638-8834a00f878e', '109a24ce-0513-4ed5-8521-e3db5da8b66b', 'Client', 'Doctor');

insert into contact_contact_relationship (contact_one_uuid, contact_two_uuid, contact_one_role, contact_two_role, relationship_creation_method)
values ('109a24ce-0513-4ed5-8521-e3db5da8b66b','4278fe7f-1343-43a2-b638-8834a00f878e', 'Doctor', 'Client', 'Inverted');

select * from contact_contact_relationship;

--Create the Comments and Emails table

create table email(
     email_uuid UUID default uuid_generate_v4() primary key,
     email_origin varchar(50) check (email_origin in ('Contact', 'Organisation')) not null,
     email_origin_uuid UUID not null,
     email_attachment_link text,
     _created_at timestamp default current_timestamp,
     _updated_at timestamp default current_timestamp
);

insert into email (email_origin, email_origin_uuid, email_attachment_link)
values ('Contact', '4278fe7f-1343-43a2-b638-8834a00f878e', 'https://linkhere.com');

insert into email (email_origin, email_origin_uuid, email_attachment_link)
values ('Organisation', '9956a733-1932-41a2-8803-36310e152c82', 'https://somethinglinkhere.com');

select * from email;

-- Create the Comments Table here --
create table comments(
    comment_uuid UUID default uuid_generate_v4() primary key,
    comment_origin_uuid UUID not null,
    comment_origin varchar(50) check (comment_origin in ('Organisation', 'Contact', 'Support Item', 'Opportunity')) not null,
    comment text,
    _created_at timestamp default current_timestamp,
    _updated_at timestamp default current_timestamp
);

insert into comments (comment_origin_uuid, comment_origin, comment)
values ('4278fe7f-1343-43a2-b638-8834a00f878e', 'Contact', 'This person is amazing!');

select * from comments;