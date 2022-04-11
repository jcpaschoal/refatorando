INSERT INTO role (description, name)
VALUES ('default_user_permissions', 'user');

INSERT INTO role (description, name)
VALUES ('owner_permissions', 'owner');

INSERT INTO role (description, name)
VALUES ('manager_permissions', 'manager');

/* Basic user permissions*/
INSERT INTO role_permission (role_id, permission_id)
VALUES (1, 4);
INSERT INTO role_permission (role_id, permission_id)
VALUES (1, 7);
INSERT INTO role_permission (role_id, permission_id)
VALUES (1, 12);

/* Basic owner permissions.*/
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 5);
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 6);
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 8);
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 9);
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 10);
INSERT INTO role_permission (role_id, permission_id)
VALUES (2, 11);


/* Basic manager permissions*/
INSERT INTO role_permission (role_id, permission_id)
VALUES (3, 1);
INSERT INTO role_permission (role_id, permission_id)
VALUES (3, 2);
INSERT INTO role_permission (role_id, permission_id)
VALUES (3, 3);