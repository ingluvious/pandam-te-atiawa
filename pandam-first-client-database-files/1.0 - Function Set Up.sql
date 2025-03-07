/*
 Function and Trigger Creation Script
 */

-- Create the Extensions on New DB Instance --
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the function that enables the encoding of the password field on the User --
create or replace function encode_base64_password()
returns trigger as $$
begin
    new.password := encode(pgp_sym_encrypt(new.password::text, 'mysecretkey'), 'base64');
    return new;
end;
$$ language plpgsql;

-- Create the trigger so that when a new password is created or updated, it will encode --
create trigger encode_password_before_insert
before insert or update on public.users
for each row execute function encode_base64_password();