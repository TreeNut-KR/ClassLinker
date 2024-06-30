TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER before_teacher_update\nBEFORE UPDATE ON teacher\nFOR EACH ROW\nBEGIN\n    SET NEW.updated_at = NOW();\nEND'
sql_modes=1436549152
definers='root@localhost'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='utf8mb4_unicode_ci'
created=171783379077
