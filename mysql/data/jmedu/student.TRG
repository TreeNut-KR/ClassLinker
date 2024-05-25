TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER before_student_update\nBEFORE UPDATE ON student\nFOR EACH ROW\nBEGIN\n    SET NEW.updated_at = NOW();\nEND'
sql_modes=1436549152
definers='root@localhost'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='utf8mb4_unicode_ci'
created=171652754158
