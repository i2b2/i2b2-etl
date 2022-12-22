/****** Object:  Table [dbo].[BIRN]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[BIRN](
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_TABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[M_APPLIED_PATH] [varchar](700) NOT NULL,
	[UPDATE_DATE] [datetime] NOT NULL,
	[DOWNLOAD_DATE] [datetime] NULL,
	[IMPORT_DATE] [datetime] NULL,
	[SOURCESYSTEM_CD] [varchar](50) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[M_EXCLUSION_CD] [varchar](25) NULL,
	[C_PATH] [varchar](700) NULL,
	[C_SYMBOL] [varchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CUSTOM_META]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CUSTOM_META](
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_TABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[M_APPLIED_PATH] [varchar](700) NOT NULL,
	[UPDATE_DATE] [datetime] NOT NULL,
	[DOWNLOAD_DATE] [datetime] NULL,
	[IMPORT_DATE] [datetime] NULL,
	[SOURCESYSTEM_CD] [varchar](50) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[M_EXCLUSION_CD] [varchar](25) NULL,
	[C_PATH] [varchar](700) NULL,
	[C_SYMBOL] [varchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[I2B2]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[I2B2](
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_TABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[M_APPLIED_PATH] [varchar](700) NOT NULL,
	[UPDATE_DATE] [datetime] NOT NULL,
	[DOWNLOAD_DATE] [datetime] NULL,
	[IMPORT_DATE] [datetime] NULL,
	[SOURCESYSTEM_CD] [varchar](50) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[M_EXCLUSION_CD] [varchar](25) NULL,
	[C_PATH] [varchar](700) NULL,
	[C_SYMBOL] [varchar](50) NULL,
	[CONCEPT_BLOB] [varchar](max) NULL,
	[CONCEPT_TYPE] [varchar](50) NULL,
	[DEFINITION_TYPE] [varchar](50) NULL,
	[UNIT_CD] [varchar](50) NULL,
	[UPLOAD_ID] [int] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ICD10_ICD9]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ICD10_ICD9](
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_TABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[M_APPLIED_PATH] [varchar](700) NOT NULL,
	[UPDATE_DATE] [datetime] NOT NULL,
	[DOWNLOAD_DATE] [datetime] NULL,
	[IMPORT_DATE] [datetime] NULL,
	[SOURCESYSTEM_CD] [varchar](50) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[M_EXCLUSION_CD] [varchar](25) NULL,
	[C_PATH] [varchar](700) NULL,
	[C_SYMBOL] [varchar](50) NULL,
	[PLAIN_CODE] [varchar](25) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ONT_PROCESS_STATUS]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ONT_PROCESS_STATUS](
	[PROCESS_ID] [int] IDENTITY(1,1) NOT NULL,
	[PROCESS_TYPE_CD] [varchar](50) NULL,
	[START_DATE] [datetime] NULL,
	[END_DATE] [datetime] NULL,
	[PROCESS_STEP_CD] [varchar](50) NULL,
	[PROCESS_STATUS_CD] [varchar](50) NULL,
	[CRC_UPLOAD_ID] [int] NULL,
	[STATUS_CD] [varchar](50) NULL,
	[MESSAGE] [varchar](max) NULL,
	[ENTRY_DATE] [datetime] NULL,
	[CHANGE_DATE] [datetime] NULL,
	[CHANGEDBY_CHAR] [char](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[PROCESS_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PHI]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PHI](
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_TABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[M_APPLIED_PATH] [varchar](700) NOT NULL,
	[UPDATE_DATE] [datetime] NOT NULL,
	[DOWNLOAD_DATE] [datetime] NULL,
	[IMPORT_DATE] [datetime] NULL,
	[SOURCESYSTEM_CD] [varchar](50) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[M_EXCLUSION_CD] [varchar](25) NULL,
	[C_PATH] [varchar](700) NULL,
	[C_SYMBOL] [varchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[SCHEMES]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SCHEMES](
	[C_KEY] [varchar](50) NOT NULL,
	[C_NAME] [varchar](50) NOT NULL,
	[C_DESCRIPTION] [varchar](100) NULL,
 CONSTRAINT [SCHEMES_PK] PRIMARY KEY CLUSTERED 
(
	[C_KEY] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TABLE_ACCESS]    Script Date: 1/21/2022 1:34:56 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TABLE_ACCESS](
	[C_TABLE_CD] [varchar](50) NOT NULL,
	[C_TABLE_NAME] [varchar](50) NOT NULL,
	[C_PROTECTED_ACCESS] [char](1) NULL,
	[C_ONTOLOGY_PROTECTION] [varchar](max) NULL,
	[C_HLEVEL] [int] NOT NULL,
	[C_FULLNAME] [varchar](700) NOT NULL,
	[C_NAME] [varchar](2000) NOT NULL,
	[C_SYNONYM_CD] [char](1) NOT NULL,
	[C_VISUALATTRIBUTES] [char](3) NOT NULL,
	[C_TOTALNUM] [int] NULL,
	[C_BASECODE] [varchar](50) NULL,
	[C_METADATAXML] [varchar](max) NULL,
	[C_FACTTABLECOLUMN] [varchar](50) NOT NULL,
	[C_DIMTABLENAME] [varchar](50) NOT NULL,
	[C_COLUMNNAME] [varchar](50) NOT NULL,
	[C_COLUMNDATATYPE] [varchar](50) NOT NULL,
	[C_OPERATOR] [varchar](10) NOT NULL,
	[C_DIMCODE] [varchar](700) NOT NULL,
	[C_COMMENT] [varchar](max) NULL,
	[C_TOOLTIP] [varchar](900) NULL,
	[C_ENTRY_DATE] [datetime] NULL,
	[C_CHANGE_DATE] [datetime] NULL,
	[C_STATUS_CD] [char](1) NULL,
	[VALUETYPE_CD] [varchar](50) NULL,
	[UPLOAD_ID] [int] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\21\', N'21', N'N', N'LA ', NULL, N'birn:mmse21', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\21\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 21', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Education\College grad.\', N'College grad.', N'N', N'LA ', NULL, N'birn:edu4', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\College grad.\', NULL, N'oasis \ Demographics \ Education \ College grad.', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\27\', N'27', N'N', N'LA ', NULL, N'birn:mmse27', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\27\', NULL, N'oasis \ Clinical Measures \ MMSE score \ No Alzheimer''s disease \ 27', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\28\', N'28', N'N', N'LA ', NULL, N'birn:mmse28', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\28\', NULL, N'oasis \ Clinical Measures \ MMSE score \ No Alzheimer''s disease \ 28', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\29\', N'29', N'N', N'LA ', NULL, N'birn:mmse29', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\29\', NULL, N'oasis \ Clinical Measures \ MMSE score \ No Alzheimer''s disease \ 29', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\30\', N'30', N'N', N'LA ', NULL, N'birn:mmse30', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\30\', NULL, N'oasis \ Clinical Measures \ MMSE score \ No Alzheimer''s disease \ 30', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\', N'Clinical Dementia Rating (CDR)', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\', NULL, N'oasis \ Clinical Measures \ Clinical Dementia Rating (CDR)', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\nondemented\', N'nondemented', N'N', N'LA ', NULL, N'birn:cdr0', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\nondemented\', NULL, N'oasis \ Clinical Measures \ MMSE score \ nondemented', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\very mild dementia\', N'very mild dementia', N'N', N'LA ', NULL, N'birn:cdr05', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\very mild dementia\', NULL, N'oasis \ Clinical Measures \ Clinical Dementia Rating (CDR) \ very mild dementia', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\mild dementia\', N'mild dementia', N'N', N'LA ', NULL, N'birn:cdr1', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\mild dementia\', NULL, N'oasis \ Clinical Measures \ Clinical Dementia Rating (CDR) \ mild dementia', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\moderate dementia\', N'moderate dementia', N'N', N'LA ', NULL, N'birn:cdr2', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\Clinical Dementia Rating (CDR)\moderate dementia\', NULL, N'oasis \ Clinical Measures \ Clinical Dementia Rating (CDR) \ moderate dementia', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Hand Orientation\Left Handed\', N'Left Handed', N'N', N'LA ', NULL, N'birn:handl', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Hand Orientation\Left Handed\', NULL, N'oasis \ Demographics \ Hand Orientation \ Left Handed', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (2, N'\BIRN\oasis\Demographics\', N'Demographics', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\', NULL, N'oasis \ Demographics', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (2, N'\BIRN\oasis\Derived Anatomic Volumes\', N'Derived Anatomic Volumes', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Derived Anatomic Volumes\', NULL, N'oasis \ Derived Anatomic Volumes', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (2, N'\BIRN\oasis\Clinical Measures\', N'Clinical Measures', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\', NULL, N'oasis \ Clinical Measures', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Derived Anatomic Volumes\Estimated Total Intracranial Volume\', N'Est. Total Intracranial Volume', N'N', N'LA ', NULL, N'birn:etiv', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Derived Anatomic Volumes\Estimated Total Intracranial Volume\', NULL, N'oasis \ Derived Anatomic Volumes \ Est. Total Intracranial Volume', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\', N'Mild Alzheimers disease', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\14\', N'14', N'N', N'LA ', NULL, N'birn:mmse14', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\14\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 14', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\24\', N'24', N'N', N'LA ', NULL, N'birn:mmse24', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\24\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 24', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (0, N'\BIRN\', N'BIRN', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\', NULL, N'BIRN', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (1, N'\BIRN\oasis\', N'Oasis', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\', NULL, N'oasis', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Demographics\Hand Orientation\', N'Hand Orientation', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Hand Orientation\', NULL, N'oasis \ Demographics \ Hand Orientation', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Hand Orientation\Right Handed\', N'Right Handed', N'N', N'LA ', NULL, N'birn:handr', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Hand Orientation\Right Handed\', NULL, N'oasis \ Demographics \ Hand Orientation \ Right Handed', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Demographics\Education\', N'Education', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\', NULL, N'oasis \ Demographics \ Education', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Education\Less than high school grad.\', N'Less than high school grad.', N'N', N'LA ', NULL, N'birn:edu1', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\Less than high school grad.\', NULL, N'oasis \ Demographics \ Education \ Less than high school grad.', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Education\High school grad.\', N'High school grad.', N'N', N'LA ', NULL, N'birn:edu2', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\High school grad.\', NULL, N'oasis \ Demographics \ Education \ High school grad.', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Education\Some college\', N'Some college', N'N', N'LA ', NULL, N'birn:edu3', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\Some college\', NULL, N'oasis \ Demographics \ Education \ Some college', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Education\Beyond college\', N'Beyond college', N'N', N'LA ', NULL, N'birn:edu5', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Education\Beyond college\', NULL, N'oasis \ Demographics \ Education \ Beyond college', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Demographics\Socioeconomic Status\', N'Socioeconomic Status', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\', NULL, N'oasis \ Demographics \ Socioeconomic Status', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 1\', N'Status 1', N'N', N'LA ', NULL, N'birn:ses1', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 1\', NULL, N'oasis \ Demographics \ Socioeconomic Status \ Status 1', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 2\', N'Status 2', N'N', N'LA ', NULL, N'birn:ses2', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 2\', NULL, N'oasis \ Demographics \ Socioeconomic Status \ Status 2', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 3\', N'Status 3', N'N', N'LA ', NULL, N'birn:ses3', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 3\', NULL, N'oasis \ Demographics \ Socioeconomic Status \ Status 3', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 4\', N'Status 4', N'N', N'LA ', NULL, N'birn:ses4', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 4\', NULL, N'oasis \ Demographics \ Socioeconomic Status \ Status 4', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 5\', N'Status 5', N'N', N'LA ', NULL, N'birn:ses5', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Demographics\Socioeconomic Status\Status 5\', NULL, N'oasis \ Demographics \ Socioeconomic Status \ Status 5', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Clinical Measures\MMSE score\', N'MMSE score', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\', NULL, N'oasis \ Clinical Measures \ MMSE score', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\', N'Moderate Alzheimers disease', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\13\', N'13', N'N', N'LA ', NULL, N'birn:mmse13', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\13\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 13', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\15\', N'15', N'N', N'LA ', NULL, N'birn:mmse15', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\15\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 15', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\16\', N'16', N'N', N'LA ', NULL, N'birn:mmse16', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\16\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 16', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\17\', N'17', N'N', N'LA ', NULL, N'birn:mmse17', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\17\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 17', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\18\', N'18', N'N', N'LA ', NULL, N'birn:mmse18', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\18\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 18', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\19\', N'19', N'N', N'LA ', NULL, N'birn:mmse19', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Moderate Alzheimers disease\19\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Moderate Alzheimer''s disease \ 19', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\20\', N'20', N'N', N'LA ', NULL, N'birn:mmse20', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\20\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 20', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\22\', N'22', N'N', N'LA ', NULL, N'birn:mmse22', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\22\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 22', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\23\', N'23', N'N', N'LA ', NULL, N'birn:mmse23', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\23\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 23', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\25\', N'25', N'N', N'LA ', NULL, N'birn:mmse25', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\25\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 25', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\26\', N'26', N'N', N'LA ', NULL, N'birn:mmse26', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\Mild Alzheimers disease\26\', NULL, N'oasis \ Clinical Measures \ MMSE score \ Mild Alzheimer''s disease \ 26', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\', N'No Alzheimers disease', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Clinical Measures\MMSE score\No Alzheimers disease\', NULL, N'oasis \ Clinical Measures \ MMSE score \ No Alzheimer''s disease', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (2, N'\BIRN\oasis\Images\', N'Images', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\', NULL, N'oasis \ Images', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Derived Anatomic Volumes\Normalized Whole Brain Volume\', N'Normalized Whole Brain Volume', N'N', N'LA ', NULL, N'birn:nwbv', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Derived Anatomic Volumes\Normalized Whole Brain Volume\', NULL, N'oasis \ Derived Anatomic Volumes \ Normalized Whole Brain Volume', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Derived Anatomic Volumes\Atlas scaling factor\', N'Atlas scaling factor', N'N', N'LA ', NULL, N'birn:asf', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Derived Anatomic Volumes\Atlas scaling factor\', NULL, N'oasis \ Derived Anatomic Volumes \ Atlas scaling factor', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), CAST(N'2007-10-10T17:10:28.000' AS DateTime), CAST(N'2007-10-10T17:10:36.000' AS DateTime), N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Images\Raw Images\', N'Raw Images', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\', NULL, N'oasis \ Images \ Raw Images', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Images\Averaged Images\', N'Averaged Images', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Averaged Images\', NULL, N'oasis \ Images \ Averaged Images', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Images\Atlas Registered\', N'Atlas Registered', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Atlas Registered\', NULL, N'oasis \ Images \ Atlas Registered Images', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Images\Masked Atlas\', N'Masked Atlas', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Masked Atlas\', NULL, N'oasis \ Images \ Masked Atlas Images', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (3, N'\BIRN\oasis\Images\Gray/White Segmented\', N'Gray/White Segmented', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Gray/White Segmented\', NULL, N'oasis \ Images \ Gray/White Segmented', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', NULL, NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Gray/White Segmented\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:gwseg_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Gray/White Segmented\Transverse\', NULL, N'oasis \ Images \ Gray/White Segmented \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Gray/White Segmented\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:gwseg_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Gray/White Segmented\Coronal\', NULL, N'oasis \ Images \ Gray/White Segmented \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Gray/White Segmented\Sagittal\', N'Sagittal', N'N', N'LI ', NULL, N'birn:gwseg_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Gray/White Segmented\Sagittal\', NULL, N'oasis \ Images \ Gray/White Segmented \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Masked Atlas\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:maskat_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Masked Atlas\Transverse\', NULL, N'oasis \ Images \ Masked Atlas \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Masked Atlas\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:maskat_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Masked Atlas\Coronal\', NULL, N'oasis \ Images \ Masked Atlas \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Masked Atlas\Sagittal\', N'Sagittal', N'N', N'LI ', NULL, N'birn:maskat_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Masked Atlas\Sagittal\', NULL, N'oasis \ Images \ Masked Atlas \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Atlas Registered\Sagittal\', N'Sagittal', N'N', N'LI ', NULL, N'birn:atlas_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Atlas Registered\Sagittal\', NULL, N'oasis \ Images \ Atlas Registered \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Atlas Registered\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:atlas_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Atlas Registered\Coronal\', NULL, N'oasis \ Images \ Atlas Registered \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Atlas Registered\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:atlas_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Atlas Registered\Transverse\', NULL, N'oasis \ Images \ Atlas Registered \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Averaged Images\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:avg_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Averaged Images\Transverse\', NULL, N'oasis \ Images \ Averaged Images \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Averaged Images\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:avg_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Averaged Images\Coronal\', NULL, N'oasis \ Images \ Averaged Images \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Averaged Images\Sagittal\', N'Sagittal', N'N', N'LI ', NULL, N'birn:avg_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Averaged Images\Sagittal\', NULL, N'oasis \ Images \ Averaged Images \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Raw Images\Third Sample\', N'Third Sample', N'N', N'FA ', NULL, N'birn:image3', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Third Sample\', NULL, N'oasis \ Images \ Raw Images \ Third Sample', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Raw Images\Fourth Sample\', N'Fourth Sample', N'N', N'FA ', NULL, N'birn:image4', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Fourth Sample\', NULL, N'oasis \ Images \ Raw Images \ Fourth Sample', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Raw Images\First Sample\', N'First Sample', N'N', N'FA ', NULL, N'birn:image1', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\First Sample\', NULL, N'oasis \ Images \ Raw Images \ First Sample', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (4, N'\BIRN\oasis\Images\Raw Images\Second Sample\', N'Second Sample', N'N', N'FA ', NULL, N'birn:image2', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Second Sample\', NULL, N'oasis \ Images \ Raw Images \ Second Sample', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\First Sample\Sagittal\', N'Sagittal', N'N', N'LA ', NULL, N'birn:image1_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\First Sample\Sagittal\', NULL, N'oasis \ Images \ Raw Images \ First Sample \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\First Sample\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:image1_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\First Sample\Coronal\', NULL, N'oasis \ Images \ Raw Images \ First Sample \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\First Sample\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:image1_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\First Sample\Transverse\', NULL, N'oasis \ Images \ Raw Images \ First Sample \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Second Sample\Sagittal\', N'Sagittal', N'N', N'LA ', NULL, N'birn:image2_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Second Sample\Sagittal\', NULL, N'oasis \ Images \ Raw Images \ Second Sample \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Second Sample\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:image2_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Second Sample\Coronal\', NULL, N'oasis \ Images \ Raw Images \ Second Sample \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Second Sample\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:image2_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Second Sample\Transverse\', NULL, N'oasis \ Images \ Raw Images \ Second Sample \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Third Sample\Sagittal\', N'Sagittal', N'N', N'LA ', NULL, N'birn:image3_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Third Sample\Sagittal\', NULL, N'oasis \ Images \ Raw Images \ Third Sample \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Third Sample\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:image3_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Third Sample\Coronal\', NULL, N'oasis \ Images \ Raw Images \ Third Sample \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Third Sample\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:image3_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Third Sample\Transverse\', NULL, N'oasis \ Images \ Raw Images \ Third Sample \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Sagittal\', N'Sagittal', N'N', N'LA ', NULL, N'birn:image4_sag', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Sagittal\', NULL, N'oasis \ Images \ Raw Images \ Fourth Sample \ Sagittal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Coronal\', N'Coronal', N'N', N'LI ', NULL, N'birn:image4_coronal', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Coronal\', NULL, N'oasis \ Images \ Raw Images \ Third Sample \ Coronal', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
INSERT [dbo].[BIRN] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (5, N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Transverse\', N'Transverse', N'N', N'LI ', NULL, N'birn:image4_trans', NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\BIRN\oasis\Images\Raw Images\Fourth Sample\Transverse\', NULL, N'oasis \ Images \ Raw Images \ Fourth Sample \ Transverse', N'@', CAST(N'2007-10-10T17:10:01.000' AS DateTime), NULL, NULL, N'OASIS', N'IMG', NULL, NULL, NULL)
GO
INSERT [dbo].[CUSTOM_META] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (0, N'\Custom Metadata\', N'Custom Metadata', N'N', N'CAE', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\Custom Metadata\', NULL, N'Custom Metadata', N'@', CAST(N'2010-05-12T00:00:00.000' AS DateTime), NULL, NULL, NULL, NULL, NULL, NULL, NULL)
GO
_GO
INSERT [dbo].[PHI] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (1, N'\PHI\First Name\', N'First Name', N'N', N'LA ', NULL, N'PHI:FNAME', N'<?xml version="1.0" encoding="UTF-8"?><ValueMetadata><Version>3.2</Version><CreationDateTime>2011-10-19T13:32:16.198-04:00</CreationDateTime><TestID>PHI:FNAME</TestID><TestName>First Name</TestName><DataType>String</DataType><MaxStringLength>50</MaxStringLength><Flagstouse>A</Flagstouse><Oktousevalues/></ValueMetadata>', N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\PHI\First Name\', NULL, N'First Name', N'@', CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), N'PHI', NULL, NULL, NULL, NULL)
INSERT [dbo].[PHI] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (0, N'\PHI\', N'PHI', N'N', N'FA ', NULL, NULL, NULL, N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\PHI\', NULL, N'PHI', N'@', CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), N'PHI', NULL, NULL, NULL, NULL)
INSERT [dbo].[PHI] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (1, N'\PHI\Last Name\', N'Last Name', N'N', N'LA ', NULL, N'PHI:LNAME', N'<?xml version="1.0" encoding="UTF-8"?><ValueMetadata><Version>3.2</Version><CreationDateTime>2011-10-19T13:32:16.198-04:00</CreationDateTime><TestID>PHI:LNAME</TestID><TestName>Last Name</TestName><DataType>String</DataType><MaxStringLength>50</MaxStringLength><Flagstouse>A</Flagstouse><Oktousevalues/></ValueMetadata>', N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\PHI\Last Name\', NULL, N'Last Name', N'@', CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), N'PHI', NULL, NULL, NULL, NULL)
INSERT [dbo].[PHI] ([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL]) VALUES (1, N'\PHI\MRN\', N'MRN', N'N', N'LA ', NULL, N'PHI:MRN', N'<?xml version="1.0" encoding="UTF-8"?><ValueMetadata><Version>3.2</Version><CreationDateTime>2011-10-19T13:32:16.198-04:00</CreationDateTime><TestID>PHI:MRN</TestID><TestName>Medical Record Number</TestName><DataType>String</DataType><MaxStringLength>50</MaxStringLength><Flagstouse>A</Flagstouse><Oktousevalues/></ValueMetadata>', N'concept_cd', N'concept_dimension', N'concept_path', N'T', N'LIKE', N'\PHI\MRN\', NULL, N'MRN', N'@', CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), CAST(N'2007-03-20T00:00:00.000' AS DateTime), N'PHI', NULL, NULL, NULL, NULL)
GO
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'(null)', N'None', N'No scheme')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|AGE:', N'DEM|AGE', N'Age of patient from demographics data')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|DATE:', N'DEM|DATE', N'Patient date of birth from demographics data')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|LANGUAGE:', N'DEM|LANGUAGE', N'Primary language spoken by patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|MARITAL:', N'DEM|MARITAL', N'Marital Status of patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|RACE:', N'DEM|RACE', N'Race of patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|RELIGION:', N'DEM|RELIGION', N'Religion of patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|SEX:', N'DEM|SEX', N'Gender of patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|VITAL:', N'DEM|VITAL', N'Vital status of patient')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DEM|ZIPCODE:', N'DEM|ZIPCODE', NULL)
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'DSG-NLP:', N'DSG-NLP', N'Natural Language Processing Data')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'ICD10:', N'ICD10', N'ICD10 code for diagnoses')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'ICD9:', N'ICD9', N'ICD9 code for diagnoses and procedures')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'LCS-I2B2:', N'LCS-I2B2', NULL)
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'LOINC:', N'LOINC', N'Lab codes')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'NDC:', N'NDC', N'National Drug Code')
INSERT [dbo].[SCHEMES] ([C_KEY], [C_NAME], [C_DESCRIPTION]) VALUES (N'UMLS:', N'UMLS', N'United Medical Language System')
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_APPLIED_PATH_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_APPLIED_PATH_IDX] ON [dbo].[BIRN]
(
	[M_APPLIED_PATH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_FULLNAME_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_FULLNAME_IDX] ON [dbo].[BIRN]
(
	[C_FULLNAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_APPLIED_PATH_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_APPLIED_PATH_IDX] ON [dbo].[CUSTOM_META]
(
	[M_APPLIED_PATH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_FULLNAME_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_FULLNAME_IDX] ON [dbo].[CUSTOM_META]
(
	[C_FULLNAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_APPLIED_PATH_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_APPLIED_PATH_IDX] ON [dbo].[I2B2]
(
	[M_APPLIED_PATH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_EXCLUSION_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_EXCLUSION_IDX] ON [dbo].[I2B2]
(
	[M_EXCLUSION_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_FULLNAME_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_FULLNAME_IDX] ON [dbo].[I2B2]
(
	[C_FULLNAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [META_HLEVEL_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_HLEVEL_IDX] ON [dbo].[I2B2]
(
	[C_HLEVEL] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_SYNONYM_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_SYNONYM_IDX] ON [dbo].[I2B2]
(
	[C_SYNONYM_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_APPL_PATH_ICD10_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_APPL_PATH_ICD10_IDX] ON [dbo].[ICD10_ICD9]
(
	[M_APPLIED_PATH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_EXCLUSION_ICD10_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_EXCLUSION_ICD10_IDX] ON [dbo].[ICD10_ICD9]
(
	[M_EXCLUSION_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_FULLNAME_ICD10_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_FULLNAME_ICD10_IDX] ON [dbo].[ICD10_ICD9]
(
	[C_FULLNAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [META_HLEVEL_ICD10_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_HLEVEL_ICD10_IDX] ON [dbo].[ICD10_ICD9]
(
	[C_HLEVEL] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_SYNONYM_ICD10_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_SYNONYM_ICD10_IDX] ON [dbo].[ICD10_ICD9]
(
	[C_SYNONYM_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_APPLIED_PATH_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_APPLIED_PATH_IDX] ON [dbo].[PHI]
(
	[M_APPLIED_PATH] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_EXCLUSION_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_EXCLUSION_IDX] ON [dbo].[PHI]
(
	[M_EXCLUSION_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_FULLNAME_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_FULLNAME_IDX] ON [dbo].[PHI]
(
	[C_FULLNAME] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [META_HLEVEL_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_HLEVEL_IDX] ON [dbo].[PHI]
(
	[C_HLEVEL] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [META_SYNONYM_IDX]    Script Date: 1/21/2022 1:35:25 PM ******/
CREATE NONCLUSTERED INDEX [META_SYNONYM_IDX] ON [dbo].[PHI]
(
	[C_SYNONYM_CD] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[PAT_COUNT_DIMENSIONS]    Script Date: 1/21/2022 1:35:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- Originally Developed by Griffin Weber, Harvard Medical School
-- Contributors: Mike Mendis, Jeff Klann, Lori Phillips

-- Count by concept
-- Multifact support by Jeff Klann, PhD 05-18
CREATE PROCEDURE [dbo].[PAT_COUNT_DIMENSIONS]  (@metadataTable varchar(50), @schemaName varchar(50),
@observationTable varchar(50), 
 @facttablecolumn varchar(50), @tablename varchar(50), @columnname varchar(50)

 )

AS BEGIN
declare @sqlstr nvarchar(4000)


    if exists (select 1 from sysobjects where name='conceptCountOnt') drop table conceptCountOnt
    if exists (select 1 from sysobjects where name='finalCountsByConcept') drop table finalCountsByConcept


-- Modify this query to select a list of all your ontology paths and basecodes.

set @sqlstr = 'select c_fullname, c_basecode
	into conceptCountOnt
	from ' + @metadataTable + 
' where lower(c_facttablecolumn)= ''' + @facttablecolumn + '''
		and lower(c_tablename) = ''' + @tablename + '''
		and lower(c_columnname) = ''' + @columnname + '''
		and lower(c_synonym_cd) = ''n''
		and lower(c_columndatatype) = ''t''
		and lower(c_operator) = ''like''
		and m_applied_path = ''@''
        and c_fullname is not null'

		
execute sp_executesql @sqlstr;

print @sqlstr

if exists(select top 1 NULL from conceptCountOnt)
BEGIN

-- Convert the ontology paths to integers to save space

select c_fullname, isnull(row_number() over (order by c_fullname),-1) path_num
	into #Path2Num
	from (
		select distinct isnull(c_fullname,'') c_fullname
		from conceptCountOnt
		where isnull(c_fullname,'')<>''
	) t

alter table #Path2Num add primary key (c_fullname)

-- Create a list of all the c_basecode values under each ontology path

select distinct isnull(c_fullname,'') c_fullname, isnull(c_basecode,'') c_basecode
	into #PathConcept
	from conceptCountOnt
	where isnull(c_fullname,'')<>'' and isnull(c_basecode,'')<>''

alter table #PathConcept add primary key (c_fullname, c_basecode)

select distinct c_basecode, path_num
	into #ConceptPath
	from #Path2Num a
		inner join #PathConcept b
			on b.c_fullname like a.c_fullname+'%'

alter table #ConceptPath add primary key (c_basecode, path_num)

-- Create a list of distinct concept-patient pairs

SET @sqlstr = 'select distinct concept_cd, patient_num
	into ##ConceptPatient
	from '+@schemaName + '.' + @observationTable+' f with (nolock)'
EXEC sp_executesql @sqlstr

ALTER TABLE ##ConceptPatient  ALTER COLUMN [PATIENT_NUM] int NOT NULL
ALTER TABLE ##ConceptPatient  ALTER COLUMN [concept_cd] varchar(50) NOT NULL

alter table ##ConceptPatient add primary key (concept_cd, patient_num)

-- Create a list of distinct path-patient pairs

select distinct c.path_num, f.patient_num
	into #PathPatient
	from ##ConceptPatient f
		inner join #ConceptPath c
			on f.concept_cd = c.c_basecode


ALTER TABLE #PathPatient  ALTER COLUMN [PATIENT_NUM] int NOT NULL
alter table #PathPatient add primary key (path_num, patient_num)


-- Determine the number of patients per path

select path_num, count(*) num_patients
	into #PathCounts
	from #PathPatient
	group by path_num

alter table #PathCounts add primary key (path_num)

-- This is the final counts per ont path

select o.*, isnull(c.num_patients,0) num_patients into finalCountsByConcept
	from conceptCountOnt o
		left outer join #Path2Num p
			on o.c_fullname = p.c_fullname
		left outer join #PathCounts c
			on p.path_num = c.path_num
	order by o.c_fullname

	set @sqlstr='update a set c_totalnum=b.num_patients from '+@metadataTable+' a, finalCountsByConcept b '+
	'where a.c_fullname=b.c_fullname ' +
 ' and lower(a.c_facttablecolumn)= ''' + @facttablecolumn + ''' ' +
	' and lower(a.c_tablename) = ''' + @tablename + ''' ' +
	' and lower(a.c_columnname) = ''' + @columnname + ''' '

--	print @sqlstr
	execute sp_executesql @sqlstr

    DROP TABLE ##CONCEPTPATIENT


    END

END;
GO
/****** Object:  StoredProcedure [dbo].[PAT_COUNT_VISITS]    Script Date: 1/21/2022 1:35:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- Originally Developed by Griffin Weber, Harvard Medical School
-- Contributors: Mike Mendis, Jeff Klann, Lori Phillips
 
CREATE PROCEDURE [dbo].[PAT_COUNT_VISITS] (@tabname varchar(50), @schemaName varchar(50))
AS BEGIN

declare @sqlstr nvarchar(4000),
		@folder varchar(1200),
        @concept varchar(1200),
		@facttablecolumn varchar(50),
		 @tablename varchar(50),
		 @columnname varchar(50),
		 @columndatatype varchar(50), 
		 @operator varchar(10),
		 @dimcode varchar(1200)


    if exists (select 1 from sysobjects where name='ontPatVisitDims') drop table ontPatVisitDims

-- pat_dim , visit_dim queries

	set @sqlstr='select c_fullname, c_basecode, c_facttablecolumn, c_tablename, c_columnname, c_operator, c_dimcode into ontPatVisitDims from ' + @tabname
        + ' where  m_applied_path = ''@'' and c_tablename in (''patient_dimension'', ''visit_dimension'') '
    execute sp_executesql @sqlstr

	alter table ontPatVisitDims add numpats int

    if exists(select top 1 NULL from ontPatVisitDims)
    BEGIN

--------------  start of cursor e -------------------------------
	Declare e CURSOR
		Local Fast_Forward
		For
			select c_fullname, c_facttablecolumn, c_tablename, c_columnname, c_operator, c_dimcode from ontPatVisitDims
	Open e
		fetch next from e into @concept, @facttablecolumn, @tablename, @columnname, @operator, @dimcode
	WHILE @@FETCH_STATUS = 0
	Begin
		begin
			if lower(@operator) = 'like'
			begin
				set @dimcode =  '''' + replace(@dimcode,'''','''''') + '%''' 
			end
			if lower(@operator) = 'in'
			begin
				set @dimcode = '(' + @dimcode + ')'
			end
			if lower(@operator) = '='
			begin
				set @dimcode = '''' +  replace(@dimcode,'''','''''') + ''''
			end
			set @sqlstr='update ontPatVisitDims set 
             numpats =  (select count(distinct(patient_num)) from ' + @schemaName + '.' + @tablename + 
               ' where ' + @facttablecolumn + ' in (select ' + @facttablecolumn + ' from ' +   @schemaName + '.' + @tablename + ' where '+ @columnname + ' ' + @operator +' ' + @dimcode +' ))
            where c_fullname = ' + ''''+ @concept + ''''+ ' and numpats is null'

		--	print @sqlstr
			execute sp_executesql @sqlstr
		end

		fetch next from e into @concept, @facttablecolumn, @tablename, @columnname, @operator, @dimcode

	End
	close e
	deallocate e

--------------  end of cursor e -------------------------------
 

	set @sqlstr='update a set c_totalnum=b.numpats from '+@tabname+' a, ontPatVisitDims b '+
	'where a.c_fullname=b.c_fullname '
--	print @sqlstr
	execute sp_executesql @sqlstr


END

END;
GO
/****** Object:  StoredProcedure [dbo].[RunTotalnum]    Script Date: 1/21/2022 1:35:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-----------------------------------------------------------------------------------------------------------------
-- Function to run totalnum counts on all tables in table_access 
-- By Mike Mendis and Jeff Klann, PhD
-----------------------------------------------------------------------------------------------------------------

CREATE PROCEDURE [dbo].[RunTotalnum]  (@observationTable varchar(50) = 'observation_fact', @schemaname varchar(50) = 'dbo') as  

DECLARE @sqlstr NVARCHAR(4000);
DECLARE @sqltext NVARCHAR(4000);
DECLARE @sqlcurs NVARCHAR(4000);

--IF COL_LENGTH('table_access','c_obsfact') is NOT NULL 
--declare getsql cursor local for
--select 'exec run_all_counts '+c_table_name+','+c_obsfact from TABLE_ACCESS where c_visualattributes like '%A%' 
--ELSE 
declare getsql cursor local for select distinct c_table_name from TABLE_ACCESS where c_visualattributes like '%A%'


-- select distinct 'exec run_all_counts '+c_table_name+','+@schemaname+','+@obsfact   from TABLE_ACCESS where c_visualattributes like '%A%'


begin
OPEN getsql;
FETCH NEXT FROM getsql INTO @sqltext;
WHILE @@FETCH_STATUS = 0
BEGIN
	print @sqltext
    SET @sqlstr = 'update '+ @sqltext +' set c_totalnum=null';
    EXEC sp_executesql @sqlstr;
    exec PAT_COUNT_VISITS @sqltext , @schemaName   
    exec PAT_COUNT_DIMENSIONS @sqltext , @schemaName, @observationTable ,  'concept_cd', 'concept_dimension', 'concept_path'  
    exec PAT_COUNT_DIMENSIONS  @sqltext , @schemaName,  @observationTable ,  'provider_id', 'provider_dimension', 'provider_path'  
    exec PAT_COUNT_DIMENSIONS  @sqltext , @schemaName, @observationTable ,  'modifier_cd', 'modifier_dimension', 'modifier_path'  

--	exec sp_executesql @sqltext
	FETCH NEXT FROM getsql INTO @sqltext;	
END

CLOSE getsql;
DEALLOCATE getsql;
end
GO
