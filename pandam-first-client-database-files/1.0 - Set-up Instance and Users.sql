/*
 Create the admin users of the DB here
 */
create user ingluvious;
    grant rds_replication to ingluvious with admin option;
    grant rds_password to ingluvious with admin option;
    grant pg_monitor to ingluvious with admin option;
    grant pg_signal_backend to ingluvious with admin option;
    grant pg_checkpoint to ingluvious with admin option;
    grant pg_use_reserved_connections to ingluvious with admin option;
    grant pg_read_all_data to ingluvious with admin option;
    grant pg_write_all_data to ingluvious with admin option;
    grant pg_create_subscription to ingluvious with admin option;
    grant pg_maintain to ingluvious with admin option;
alter user ingluvious with password 'Hello12345';
create user jheneene;
    grant rds_replication to jheneene with admin option;
    grant rds_password to jheneene with admin option;
    grant pg_monitor to jheneene with admin option;
    grant pg_signal_backend to jheneene with admin option;
    grant pg_checkpoint to jheneene with admin option;
    grant pg_use_reserved_connections to jheneene with admin option;
    grant pg_read_all_data to jheneene with admin option;
    grant pg_write_all_data to jheneene with admin option;
    grant pg_create_subscription to jheneene with admin option;
    grant pg_maintain to jheneene with admin option;
alter user jheneene with password 'Hello12345';
