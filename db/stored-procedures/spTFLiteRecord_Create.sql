SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spTFLiteRecord_Create]
  @modelName NVARCHAR(200),
  @zipContent VARBINARY(MAX)
AS
BEGIN
  SET NOCOUNT ON;

  INSERT INTO dbo.TFLiteRecord
  OUTPUT
    inserted.Id
  VALUES
    (@modelName, @zipContent, 0);
END
GO