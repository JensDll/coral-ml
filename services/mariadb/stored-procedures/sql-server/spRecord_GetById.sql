SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_GetById]
  @id INT
AS
BEGIN
  SET NOCOUNT ON;

  SELECT
    R.id,
    R.modelFileName,
    R.labelFileName,
    R.recordTypeId,
    RT.recordType
  FROM dbo.Record R
  INNER JOIN dbo.RecordType RT
    ON RT.id = R.recordTypeId
  WHERE R.id = @id
  FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
END
GO