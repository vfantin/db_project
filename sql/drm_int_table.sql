DROP TABLE IF EXISTS #VIEWS
SELECT TABLE_SCHEMA VIEW_SCHEMA,TABLE_NAME VIEW_NAME, RIGHT(TABLE_NAME,LEN(TABLE_NAME)-2) T_NAME
INTO #VIEWS 
FROM INFORMATION_SCHEMA.VIEWS ORDER BY TABLE_SCHEMA,TABLE_NAME

--SELECT * 
--FROM #VIEWS V
--LEFT JOIN INFORMATION_SCHEMA.TABLES T ON V.T_NAME = T.TABLE_NAME 
--WHERE T.TABLE_NAME IS NOT NULL AND T.TABLE_NAME like 'index_%'
--AND T.TABLE_SCHEMA = 'merrill' AND V.VIEW_SCHEMA = 'service_snp' AND T.TABLE_NAME = 'index_summary'

DROP TABLE IF EXISTS #RESULTS
SELECT CONCAT(TABLE_SCHEMA,'.[',TABLE_NAME,']') AS OBJECT_NAME, 'base_file_date' AS FIELD_NAME,VIEW_SCHEMA,VIEW_NAME
INTO #RESULTS
FROM #VIEWS V
INNER JOIN INFORMATION_SCHEMA.TABLES T ON V.T_NAME = T.TABLE_NAME 

--Double index_summary on snp & merrill
DELETE FROM #RESULTS WHERE VIEW_SCHEMA = 'service_merrill' AND OBJECT_NAME = 'snp.[index_summary]' 
DELETE FROM #RESULTS WHERE VIEW_SCHEMA = 'service_snp' AND OBJECT_NAME = 'merrill.[index_summary]' 

--No match ... 
--SELECT * FROM #VIEWS V
--LEFT JOIN INFORMATION_SCHEMA.TABLES T ON V.T_NAME = T.TABLE_NAME 
--WHERE TABLE_NAME IS NULL
--ORDER BY 1,2
--Add manually when no match
INSERT INTO #RESULTS VALUES ('data_cdpq.[manual]','base_file_date','cdpq','v_sous_jacents_fonds_placement_prive')
--D.base_file_name = 'CDPQ4_DBPRI_TXT_BRUT'
INSERT INTO #RESULTS VALUES ('data_dbrs.[mixed]','base_file_date','dbrs','v_dbpri')
--D.base_file_name = 'CDPQ4_MBPRF_TXT_BRUT'
INSERT INTO #RESULTS VALUES ('data_dbrs.[mixed]','base_file_date','dbrs','v_mbprf')
--AND D.Tenor IS NULL
INSERT INTO #RESULTS VALUES ('data_ihs_markit.[equity_volatility]','base_file_date','ihs_markit','v_equity_volatility_fixed_maturity')
--AND D.Tenor IS NOT NULL
INSERT INTO #RESULTS VALUES ('data_ihs_markit.[equity_volatility]','base_file_date','ihs_markit','v_equity_volatility_floating_maturity')

INSERT INTO #RESULTS VALUES ('cck.[cck_bank_centers]','base_file_date','service_cck','v_bank_centers')
INSERT INTO #RESULTS VALUES ('cck.[cck_currencies]','base_file_date','service_cck','v_currencies')
INSERT INTO #RESULTS VALUES ('cck.[cck_exch_sett]','base_file_date','service_cck','v_exch_sett')
INSERT INTO #RESULTS VALUES ('cck.[cck_exch_trdg]','base_file_date','service_cck','v_exch_trdg')

INSERT INTO #RESULTS VALUES ('data_rimes.[equity_constituent_level]','base_file_date','service_rimes','v_indice_compositions_actions')
INSERT INTO #RESULTS VALUES ('data_rimes.[fixed_income_constituent_level]','base_file_date','service_rimes','v_indice_compositions_obligations')
INSERT INTO #RESULTS VALUES ('data_rimes.[equity_index_level]','base_file_date','service_rimes','v_indice_niveaux_actions')
INSERT INTO #RESULTS VALUES ('data_rimes.[fixed_income_index_level]','base_file_date','service_rimes','v_indice_niveaux_obligations')

SELECT OBJECT_NAME,FIELD_NAME,VIEW_SCHEMA,VIEW_NAME
FROM #RESULTS
ORDER BY 1,3

--DROP TABLE IF EXISTS ##RESULTS
--DROP TABLE IF EXISTS #VIEWS

