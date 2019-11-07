create user 'forex'@'%' identified by 'forex';
grant all on *.* to 'forex'@'%';

create database if not exists forex;
CREATE TABLE IF NOT EXISTS forex.pairs (
    CODE VARCHAR(16) NOT NULL,
    BASE_CURRENCY VARCHAR(16) NOT NULL,
    QUOTE_CURRENCY VARCHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS forex.trades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CODE VARCHAR(16) NOT NULL,
    PURCHASE VARCHAR(16),
    ENTRY FLOAT(8,5),
    SL1 FLOAT(8,5),
    SL2 FLOAT(8,5),
    SL3 FLOAT(8,5),
    SL4 FLOAT(8,5),
    SL5 FLOAT(8,5),
    SL_COUNT INT,
    TP1 FLOAT(8,5),
    TP2 FLOAT(8,5),
    TP3 FLOAT(8,5),
    TP4 FLOAT(8,5),
    TP5 FLOAT(8,5),
    TP_COUNT INT,
    ORIGIN VARCHAR(255),
    STRATGEY VARCHAR(255),
    COMMENT VARCHAR(255),
    STATE VARCHAR(255),
    TG_MESSAGE_ID LONG,
    TG_SENDER_ID LONG,
    TG_DATE DATETIME,
    MT4_TICKET_ID LONG,
    MT4_OPEN_TIME DATETIME
);


insert into forex.pairs(CODE, BASE_CURRENCY, QUOTE_CURRENCY)
VALUES
    ("AUDUSD", "AUD", "USD"),
    ("AUDJPY", "AUD", "JPY"),
    ("AUDNZD", "AUD", "NZD"),
    ("AUDCAD", "AUD", "CAD"),
    ("AUDCHF", "AUD", "CHF"),
    ("CADJPY", "CAD", "JPY"),
    ("CADCHF", "CAD", "CHF"),
    ("CHFJPY", "CHF", "JPY"),
    ("EURNOK", "EUR", "NOK"),
    ("EURUSD", "EUR", "USD"),
    ("EURCHF", "EUR", "CHF"),
    ("EURTRY", "EUR", "TRY"),
    ("EURGBP", "EUR", "GBP"),
    ("EURJPY", "EUR", "JPY"),
    ("EURAUD", "EUR", "AUD"),
    ("EURCAD", "EUR", "CAD"),
    ("EURNZD", "EUR", "NZD"),
    ("EURSEK", "EUR", "SEK"),
    ("GBPJPY", "GBP", "JPY"),
    ("GBPNZD", "GBP", "NZD"),
    ("GBPAUD", "GBP", "AUD"),
    ("GBPCHF", "GBP", "CHF"),
    ("GBPUSD", "GBP", "USD"),
    ("GBPCAD", "GBP", "CAD"),
    ("NZDCHF", "NZD", "CHF"),
    ("NZDJPY", "NZD", "JPY"),
    ("NZDUSD", "NZD", "USD"),
    ("NZDCAD", "NZD", "CAD"),
    ("TRYJPY", "TRY", "JPY"),
    ("USDHKD", "USD", "HKD"),
    ("USDNOK", "USD", "NOK"),
    ("USDSEK", "USD", "SEK"),
    ("USDZAR", "USD", "ZAR"),
    ("USDMXN", "USD", "MXN"),
    ("USDTRY", "USD", "TRY"),
    ("USDCAD", "USD", "CAD"),
    ("USDCHF", "USD", "CHF"),
    ("USDJPY", "USD", "JPY"),
    ("USDCNH", "USD", "CNH"),
    ("ZARJPY", "ZAR", "JPY");
