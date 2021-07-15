SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_Create]
  @modeFilelName NVARCHAR(200),
  @labelFileName NVARCHAR(200),
  @zipContent VARBINARY(MAX),
  @recordTypeId INT
AS
BEGIN
  SET NOCOUNT ON;

  INSERT INTO dbo.Record
  OUTPUT
    inserted.Id
  VALUES
    (
      @modeFilelName,
      @labelFileName,
      @zipContent,
      @recordTypeId
    );
END
GO