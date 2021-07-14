SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[spRecord_Download]
  @id int
AS
BEGIN
  SET NOCOUNT ON;

  SELECT zipContent
  FROM dbo.Record
  WHERE id = @id;
END
GO