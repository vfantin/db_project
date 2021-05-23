USE [DRM_DV1_CTL]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS [control].[WebAPILog_Prod]
CREATE TABLE [control].[WebAPILog_Prod](
	[WebAPILogID] [int] IDENTITY(1,1) NOT NULL,
	/*To be sure*/
	[LineNumber] [int] NOT NULL,
	/*More details with datetime2*/
	[Date] [datetime2] NULL,
	[CorrelationGuid] [char](36) NULL,
	[ThreadID] [int] NULL,
	[Level] [varchar](10) NULL,
	[Logger] [varchar](max) NULL,
	[Message] [varchar](max) NULL,
 CONSTRAINT [PK_WebAPILog_Prod] PRIMARY KEY CLUSTERED ([WebAPILogID] ASC))
GO


