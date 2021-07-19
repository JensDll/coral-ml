CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_GetById(
  IN param_id int
)
BEGIN
  SELECT
    JSON_OBJECT(
      'id', r.id,
      'modelFileName', r.modelFileName,
      'labelFileName', r.labelFileName,
      'recordTypeId', r.recordTypeId,
      'recordType', rt.recordType
    )
  FROM Record r
  INNER JOIN RecordType rt
  ON r.recordTypeId = rt.id
  WHERE r.id = param_id;
END