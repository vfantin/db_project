DROP TABLE IF EXISTS #TABLES

SELECT CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS OBJECT_NAME,'base_file_date' as FIELD_NAME 
INTO #TABLES FROM INFORMATION_SCHEMA.VIEWS ORDER BY TABLE_SCHEMA,TABLE_NAME

UPDATE #TABLES SET FIELD_NAME = 'date_import' WHERE OBJECT_NAME = 'service_bbgbo.v_credit_risk_dbrs_out'
UPDATE #TABLES SET FIELD_NAME = 'date_import' WHERE OBJECT_NAME = 'service_bbgbo.v_credit_risk_moody_out'
UPDATE #TABLES SET FIELD_NAME = 'date_import' WHERE OBJECT_NAME = 'service_bbgbo.v_credit_risk_sp_out'
SELECT * FROM #TABLES ORDER BY 1