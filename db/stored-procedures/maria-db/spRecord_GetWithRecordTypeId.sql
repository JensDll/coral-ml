CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_GetWithRecordTypeId(IN param_skip INT, IN param_take INT, IN param_recordTypeId INT, OUT param_total int)
BEGIN
  SELECT
    IFNULL(
      JSON_ARRAYAGG(
        JSON_OBJECT(
          'id', r.id,
          'modelFileName', r.modelFileName,
          'labelFileName', r.labelFileName,
          'recordTypeId', r.recordTypeId,
          'recordType', rt.recordType
        )
      ),
      '[]'
    )
  FROM Record r
  INNER JOIN RecordType rt
  ON r.recordTypeId = rt.id
  WHERE param_recordTypeId = r.recordTypeId
  ORDER BY r.id
  LIMIT param_skip, param_take;

  SELECT COUNT(*) INTO param_total
  FROM Record r
  WHERE r.recordTypeId = param_recordTypeId;
END