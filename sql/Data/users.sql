USE portfolioanalyzer;

INSERT INTO users (username, userpwd, is_admin) VALUES
    ('admin', 'pbkdf2:sha256:600000$mHGADYJ8Yq8VfDrp$64e941a1caf1f99ffc81223062ccdaf57dc6e61eb6ebd606add179f034373d23', TRUE),
    ('testuser', 'pbkdf2:sha256:600000$DkcKNFq0fwqNwxH9$f222257bd2c7bfa18a74d41e2d6e6c7c8e54ac4a554f4d21df6f98e7509ac6d2', FALSE);