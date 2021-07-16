CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecord_Create(
  IN param_modelFileName VARCHAR(200),
  IN param_LabelFileName VARCHAR(200),
  IN param_zipContent LONGBLOB,
  IN param_recordTypeId INT(11)
)
BEGIN
  INSERT INTO Record(
    modelFileName,
    labelFileName,
    zipContent,
    recordTypeId
  )
  VALUES
  (
    param_modelFileName,
    param_LabelFileName,
    param_zipContent,
    param_recordTypeId
  );

  SELECT LAST_INSERT_ID();
END