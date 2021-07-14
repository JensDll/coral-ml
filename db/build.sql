USE [master]
GO
/****** Object:  Database [RecordDb]    Script Date: 14/07/2021 10:32:08 ******/
CREATE DATABASE [RecordDb]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ModelDb', FILENAME = N'/var/opt/mssql/data/ModelDb.mdf' , SIZE = 335872KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ModelDb_log', FILENAME = N'/var/opt/mssql/data/ModelDb_log.ldf' , SIZE = 270336KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [RecordDb] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [RecordDb].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [RecordDb] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [RecordDb] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [RecordDb] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [RecordDb] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [RecordDb] SET ARITHABORT OFF 
GO
ALTER DATABASE [RecordDb] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [RecordDb] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [RecordDb] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [RecordDb] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [RecordDb] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [RecordDb] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [RecordDb] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [RecordDb] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [RecordDb] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [RecordDb] SET  DISABLE_BROKER 
GO
ALTER DATABASE [RecordDb] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [RecordDb] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [RecordDb] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [RecordDb] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [RecordDb] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [RecordDb] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [RecordDb] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [RecordDb] SET RECOVERY FULL 
GO
ALTER DATABASE [RecordDb] SET  MULTI_USER 
GO
ALTER DATABASE [RecordDb] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [RecordDb] SET DB_CHAINING OFF 
GO
ALTER DATABASE [RecordDb] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [RecordDb] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [RecordDb] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [RecordDb] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'RecordDb', N'ON'
GO
ALTER DATABASE [RecordDb] SET QUERY_STORE = OFF
GO
USE [RecordDb]
GO
/****** Object:  Table [dbo].[LoadedRecord]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LoadedRecord](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[recordId] [int] NOT NULL,
 CONSTRAINT [PK_LoadedModel] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Record]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Record](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[modelFileName] [nvarchar](200) NOT NULL,
	[labelFileName] [nvarchar](200) NOT NULL,
	[zipContent] [varbinary](max) NOT NULL,
	[recordTypeId] [int] NOT NULL,
 CONSTRAINT [PK_Model] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[RecordType]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[RecordType](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[recordType] [nvarchar](200) NOT NULL,
 CONSTRAINT [PK_ModelType] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[LoadedRecord]  WITH CHECK ADD  CONSTRAINT [FK__LoadedRecord__recordId__Record__id] FOREIGN KEY([recordId])
REFERENCES [dbo].[Record] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[LoadedRecord] CHECK CONSTRAINT [FK__LoadedRecord__recordId__Record__id]
GO
ALTER TABLE [dbo].[Record]  WITH NOCHECK ADD  CONSTRAINT [FK__Record__recordTypeId__RecordType__id] FOREIGN KEY([recordTypeId])
REFERENCES [dbo].[RecordType] ([id])
GO
ALTER TABLE [dbo].[Record] CHECK CONSTRAINT [FK__Record__recordTypeId__RecordType__id]
GO
/****** Object:  StoredProcedure [dbo].[spModelType_GetAll]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spModelType_GetAll]
AS
BEGIN
  SET NOCOUNT ON;

  DECLARE @count_table TABLE (
    modelTypeId INT,
    total INT
  );

  INSERT INTO @count_table
  SELECT MT.id, COUNT(TFL.id)
  FROM dbo.TFLiteRecord TFL
  RIGHT OUTER JOIN dbo.ModelType MT
    ON MT.id = TFL.modelTypeId
  GROUP BY MT.id;
  
  SELECT ISNULL(
    (
      SELECT
        Mt.id,
        MT.modelType,
        CT.total
      FROM dbo.ModelType MT
      INNER JOIN @count_table CT
        ON CT.modelTypeId = MT.id
      FOR JSON PATH
    ),
    '[]'
  );
  
END
GO
/****** Object:  StoredProcedure [dbo].[spRecord_Create]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_Create]
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
/****** Object:  StoredProcedure [dbo].[spRecord_Delete]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_Delete]
  @id int
AS
BEGIN
  SET NOCOUNT ON;

  DELETE FROM dbo.Record
  WHERE id = @id;
END
GO
/****** Object:  StoredProcedure [dbo].[spRecord_Download]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_Download]
  @id int
AS
BEGIN
  SET NOCOUNT ON;

  SELECT zipContent
  FROM dbo.Record
  WHERE id = @id;
END
GO
/****** Object:  StoredProcedure [dbo].[spRecord_GetAll]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_GetAll]
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
        RT.recordType
      FROM dbo.Record as R
      INNER JOIN dbo.RecordType RT
        ON RT.id = R.recordTypeId
      WHERE R.recordTypeId = @recordTypeId
      ORDER BY Id
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
/****** Object:  StoredProcedure [dbo].[spRecord_GetById]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_GetById]
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
/****** Object:  StoredProcedure [dbo].[spRecord_GetLoaded]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_GetLoaded]
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
/****** Object:  StoredProcedure [dbo].[spRecord_GetWithRecordTypeId]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_GetWithRecordTypeId]
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
/****** Object:  StoredProcedure [dbo].[spRecord_SetLoaded]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecord_SetLoaded]
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
/****** Object:  StoredProcedure [dbo].[spRecordType_GetAll]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spRecordType_GetAll]
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
/****** Object:  StoredProcedure [dbo].[spTFLiteRecord_Create]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spTFLiteRecord_Create]
  @modeFilelName NVARCHAR(200),
  @labelFileName NVARCHAR(200),
  @zipContent VARBINARY(MAX),
  @modelTypeId INT
AS
BEGIN
  SET NOCOUNT ON;

  INSERT INTO dbo.TFLiteRecord
  OUTPUT
    inserted.Id
  VALUES
    (
      @modeFilelName,
      @labelFileName,
      @zipContent,
      @modelTypeId
    );
END
GO
/****** Object:  StoredProcedure [dbo].[spTFLiteRecord_Delete]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spTFLiteRecord_Delete]
  @id int
AS
BEGIN
  SET NOCOUNT ON;

  DELETE FROM dbo.TFLiteRecord
  WHERE id = @id;
END
GO
/****** Object:  StoredProcedure [dbo].[spTFLiteRecord_Download]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spTFLiteRecord_Download]
  @id int
AS
BEGIN
  SET NOCOUNT ON;

  SELECT zipContent
  FROM dbo.TFLiteRecord
  WHERE id = @id;
END
GO
/****** Object:  StoredProcedure [dbo].[spTFLiteRecord_GetAll]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spTFLiteRecord_GetAll]
  @skip INT,
  @take INT,
  @total INT OUTPUT,
  @modelTypeId INT
AS
BEGIN
  SET NOCOUNT ON;

  SELECT ISNULL(
    (
      SELECT
        TFL.id,
        TFL.modelFileName,
        TFL.labelFileName,
        MT.modelType
      FROM dbo.TFLiteRecord TFL
      INNER JOIN dbo.ModelType MT
        ON MT.id = TFL.modelTypeId
      WHERE TFL.modelTypeId = @modelTypeId
      ORDER BY Id
        OFFSET @skip ROWS
        FETCH NEXT @take ROWS ONLY
      FOR JSON PATH
    ),
    '[]'
  );

  SELECT @total = COUNT(id)
  FROM dbo.TFLiteRecord;
END
GO
/****** Object:  StoredProcedure [dbo].[spTFLiteRecord_GetById]    Script Date: 14/07/2021 10:32:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   PROCEDURE [dbo].[spTFLiteRecord_GetById]
  @id INT
AS
BEGIN
  SET NOCOUNT ON;

  SELECT
    TFL.id,
    TFL.modelFileName,
    TFL.labelFileName,
    MT.modelType
  FROM dbo.TFLiteRecord TFL
  INNER JOIN dbo.ModelType MT
    ON MT.id = TFL.modelTypeId
  WHERE TFL.id = @id
  FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
END
GO
USE [master]
GO
ALTER DATABASE [RecordDb] SET  READ_WRITE 
GO
