SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_GetLoaded]
AS
BEGIN
  SET NOCOUNT ON;

  SELECT
    R.id,
    R.modelFileName,
    R.labelFileName,
    R.recordTypeId,
    RT.recordType
  FROM dbo.LoadedRecord LR
  INNER JOIN dbo.Record R
    ON R.id = LR.recordId
  INNER JOIN dbo.RecordType RT
    ON RT.id = R.recordTypeId
  FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
END
GO