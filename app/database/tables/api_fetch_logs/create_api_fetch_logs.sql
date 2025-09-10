USE portfolioanalyzer;

CREATE TABLE api_fetch_logs (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    symbol VARCHAR(20) NOT NULL,
    fetch_type ENUM('STOCK', 'EXCHANGE') NOT NULL,
    status ENUM('SUCCESS', 'FAILED', 'PENDING', 'PARTIAL') NOT NULL DEFAULT 'PENDING',
    error_message TEXT,
    fetch_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    retry_count INT NOT NULL DEFAULT 0,
    INDEX idx_symbol (symbol),
    INDEX idx_fetch_type (fetch_type),
    INDEX idx_status (status),
    INDEX idx_fetch_time (fetch_time)
);
