USE [DRM_DV1_CTL]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
DROP TABLE IF EXISTS [control].[PerformanceResults]
CREATE TABLE [control].[PerformanceResults](
	[PerformanceResultsID] [int] IDENTITY(1,1) NOT NULL,
	[BatchID] [int] NOT NULL,
	[DB] [varchar](max) NULL,
	[DBObject] [char](256) NULL,
	[RequestType] [varchar](128) NULL,
    [Request] [varchar](max) NULL,
	[Results] [varchar](max) NULL,
	[ExecutionTimeInSecond] decimal(32,6) NULL,
	[ExecutionDate] datetime2 NULL,
	
 CONSTRAINT [PerformanceResultsID] PRIMARY KEY CLUSTERED ([PerformanceResultsID] ASC))
GO

DROP TABLE IF EXISTS [control].[PerformanceResults2]
CREATE TABLE [control].[PerformanceResults2](
	[PerformanceResultsID] [int] IDENTITY(1,1) NOT NULL,
	[BatchGuid] [varchar](32) NOT NULL,
	[BatchType] [varchar](64) NULL,
	[DB] [varchar](max) NULL,
	[DBObject] [char](256) NULL,
	[RequestName] [varchar](64) NULL,
	[Request] [varchar](max) NULL,
    [Results] [varchar](max) NULL,
	[ExecutionTimeInSecond] decimal(32,6) NULL,
	[ExecutionDate] datetime2 NULL,
	
 CONSTRAINT [PerformanceResults2_PerformanceResultsID] PRIMARY KEY CLUSTERED ([PerformanceResultsID] ASC))
GO
