CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_Delete(
  IN param_id int
)
BEGIN
  DELETE FROM Record
  WHERE id = param_id;
END