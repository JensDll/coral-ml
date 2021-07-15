CREATE 
	DEFINER = 'root'@'%'
PROCEDURE RecordDb.spRecordType_GetAll()
BEGIN
  CREATE TEMPORARY TABLE count_table(
    recordTypeId int,
    total int
  );
   
  INSERT INTO count_table
  SELECT rt.id, COUNT(r.id)
  FROM Record r
  RIGHT OUTER JOIN RecordType rt
  ON rt.id = r.recordTypeId
  GROUP BY rt.id;

  SELECT
    IFNULL(
      JSON_ARRAYAGG(
        JSON_OBJECT(
          'id', rt.id,
          'recordType', rt.recordType,
          'total', ct.total
        )
      ),
      '[]'
    )
  FROM RecordType rt
  INNER JOIN count_table ct
  ON rt.id = ct.recordTypeId;
END