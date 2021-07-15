CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_Download(
  IN param_id int
)
BEGIN
  SELECT zipContent
  FROM Record r
  WHERE r.id = param_id;
END