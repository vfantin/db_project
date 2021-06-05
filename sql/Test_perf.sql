USE DRM_INT

--5 mn
SELECT COUNT(1) FROM service_mstar.v_etf_holding_detail WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM service_bbgbo.v_equity_out WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM service_bbgbo.v_equity_px WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM rimes.v_equity_constituent_level WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM service_rimes.v_indice_compositions_actions WHERE base_file_date = '2021-05-21'

--30s
SELECT COUNT(1) FROM mstar.etf_holding_detail WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM bbgbo.equity_out WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM bbgbo.equity_px WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM data_rimes.equity_constituent_level WHERE base_file_date = '2021-05-21'
SELECT COUNT(1) FROM data_rimes.equity_constituent_level WHERE base_file_date = '2021-05-21'