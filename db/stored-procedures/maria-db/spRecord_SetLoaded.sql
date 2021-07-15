CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_SetLoaded(
  IN param_recordId INT
)
BEGIN
  DECLARE loaded_record_id int;

  SELECT lr.id INTO loaded_record_id
  FROM LoadedRecord lr;

  IF loaded_record_id IS NULL
  THEN
    INSERT INTO LoadedRecord(recordId)
    VALUES (param_recordId);
  ELSE
    UPDATE LoadedRecord lr
    SET lr.recordId = param_recordId;
  END IF;
END