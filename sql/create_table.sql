CREATE TABLE IF NOT EXISTS stock_data (
  symbol TEXT NOT NULL,
  date DATE NOT NULL,
  open DOUBLE PRECISION,
  high DOUBLE PRECISION,
  low DOUBLE PRECISION,
  close DOUBLE PRECISION,
  adjusted_close DOUBLE PRECISION,
  volume BIGINT,
  PRIMARY KEY (symbol, date)
);
