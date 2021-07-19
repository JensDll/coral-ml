SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_GetWithRecordTypeId]
  @skip INT,
  @take INT,
  @total INT OUTPUT,
  @recordTypeId INT
AS
BEGIN
  SET NOCOUNT ON;

  SELECT ISNULL(
    (
      SELECT
        R.id,
        R.modelFileName,
        R.labelFileName,
        R.recordTypeId,
        RT.recordType
      FROM dbo.Record as R
      INNER JOIN dbo.RecordType RT
        ON RT.id = R.recordTypeId
      WHERE R.recordTypeId = @recordTypeId
      ORDER BY R.id
        OFFSET @skip ROWS
        FETCH NEXT @take ROWS ONLY
      FOR JSON PATH
    ),
    '[]'
  );

  SELECT @total = COUNT(id)
  FROM dbo.Record
  WHERE recordTypeId = @recordTypeId;
END
GO