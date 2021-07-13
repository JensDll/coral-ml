SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_SetLoaded]
  @recordId INT
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE @id INT;

  SELECT @id = id
  FROM dbo.LoadedRecord;
    
  IF @id IS NULL
  BEGIN
    INSERT INTO dbo.LoadedRecord
    VALUES (@recordId);
  END
  ELSE
  BEGIN
    UPDATE dbo.LoadedRecord
    SET recordId = @recordId;
  END
END
GO