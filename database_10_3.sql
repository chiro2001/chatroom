PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE data (name varchar(512), passwd char(32), email varchar(512));
INSERT INTO "data" VALUES('Lance','b06a7393dad7e25ec029a864d669bdf5','lanceliang2018@163.com');
INSERT INTO "data" VALUES('extra','aff84bdf14ad3818d65684fa61baf786','371743175@qq.com');
INSERT INTO "data" VALUES('wise_world','f10efa931b523ce3998d05cfe83e63cc','1056366209@qq.com');
INSERT INTO "data" VALUES('haitu','adf4661fe6715ed47954193e68b63036','398283591@qq.com');
COMMIT;
