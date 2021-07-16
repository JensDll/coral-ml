CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_GetLoaded()
BEGIN
  SELECT
    JSON_OBJECT(
      'id', r.id,
      'modelFileName', r.modelFileName,
      'labelFileName', r.labelFileName,
      'recordTypeId', r.recordTypeId,
      'recordType', rt.recordType
    )
  FROM LoadedRecord lr
  INNER JOIN Record r
  ON lr.recordId = r.id
  INNER JOIN RecordType rt
  ON r.recordTypeId = rt.id;
END