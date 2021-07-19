SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecordType_GetAll]
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE @count_table TABLE (
    recordTypeId INT,
    total INT
  );

  INSERT INTO @count_table
  SELECT RT.id, COUNT(R.id)
  FROM dbo.Record R
  RIGHT OUTER JOIN dbo.RecordType RT
    ON RT.id = R.recordTypeId
  GROUP BY RT.id;
  
  SELECT ISNULL(
    (
      SELECT
        RT.id,
        RT.recordType,
        CT.total
      FROM dbo.RecordType RT
      INNER JOIN @count_table CT
        ON CT.recordTypeId = RT.id
      FOR JSON PATH
    ),
    '[]'
  );
  
END
GO