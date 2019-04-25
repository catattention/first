
UPDATE lddb.up_sec_role_user a
SET a.role_id = (WITH b AS (
SELECT r.id roleid
,r.name
--,decode(r.name,'“ªº∂…Û∫À','ff8080816a446f6e016a543e4b22000d','∂˛º∂…Û∫À','ff8080816a446f6e016a543e446c000c') rolename
,t.type_id,t.name,s.id userid FROM lddb.up_org_user s
INNER JOIN lddb.up_org_unit t ON s.org_id = t.id
INNER JOIN lddb.up_sec_role_user rs ON rs.user_id = s.id
INNER JOIN lddb.up_sec_busi_role r ON r.id = rs.role_id
WHERE r.name LIKE '%…Û∫À%'
  AND INSTR(TYPE_ID,'04') = 0
)
SELECT b.rolename FROM b WHERE a.role_id = b.roleid
    AND a.user_id = b.userid)
WHERE EXISTS(WITH b AS (
SELECT r.id roleid
,decode(r.name,'“ªº∂…Û∫À','ff8080816a446f6e016a543e4b22000d','∂˛º∂…Û∫À','ff8080816a446f6e016a543e446c000c') rolename
,t.type_id,t.name,s.id userid FROM lddb.up_org_user s
INNER JOIN lddb.up_org_unit t ON s.org_id = t.id
INNER JOIN lddb.up_sec_role_user rs ON rs.user_id = s.id
INNER JOIN lddb.up_sec_busi_role r ON r.id = rs.role_id
WHERE r.name LIKE '%…Û∫À%'
  AND INSTR(TYPE_ID,'04') > 0
)SELECT 1 FROM b WHERE a.role_id = b.roleid AND a.user_id = b.userid)

/*SELECT * FROM lddb.up_sec_busi_role r
WHERE r.name LIKE '%…Û∫À%'

ff8080816a446f6e016a543e4b22000d
ff8080816a446f6e016a543e446c000c*/
