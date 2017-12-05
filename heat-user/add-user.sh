keystone tenant-create --name tenant-1 --description "Tenant-1" 

 keystone user-create --name t1-user --tenant tenant-1  --pass 111111 --email test1@aaa.cc

  keystone user-role-add --user t1-user --tenant tenant-1 --role heat_stack_owner
