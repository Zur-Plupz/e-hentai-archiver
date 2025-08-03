-- 2021_03_30_051448_create_galleries_table.php
CREATE TABLE IF NOT EXISTS galleries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    gid INTEGER NOT NULL,
    token VARCHAR(50) NOT NULL,
    credits SMALLINT NULL,
    gp SMALLINT NULL,
    favorited TIMESTAMP NULL,
    archived TINYINT DEFAULT '0' NOT NULL,
    archive_path VARCHAR(255) NULL,
    archiver_key VARCHAR(100) NULL,
    category VARCHAR(50) NULL,
    thumb VARCHAR(255) NULL,
    uploader VARCHAR(255) NULL,
    posted INTEGER NULL,
    filecount SMALLINT NULL,
    filesize INTEGER NULL,
    expunged TINYINT DEFAULT '0' NULL,
    rating VARCHAR(255) NULL,
    torrentcount SMALLINT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);


CREATE TABLE IF NOT EXISTS torrents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gallery_id INTEGER NOT NULL,
    hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    size VARCHAR(50) NOT NULL,
    seeds SMALLINT NULL,
    peers SMALLINT NULL,
    completed SMALLINT DEFAULT '0' NOT NULL,
    downloads SMALLINT DEFAULT '0' NOT NULL,
    posted_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);


-- 2021_03_30_053524_create_tags_table.php
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namespace VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);

-- 2021_03_30_061813_create_gallery_taggings_table.php
CREATE TABLE IF NOT EXISTS gallery_taggings (
    gallery_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (gallery_id) REFERENCES galleries (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);

-- 2021_03_31_041330_create_groups_table.php
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);

-- 2021_03_31_042814_create_gallery_groups_table.php
CREATE TABLE IF NOT EXISTS gallery_groups (
    gallery_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (gallery_id) REFERENCES galleries (id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE
);

-- 2021_04_25_022257_create_credit_logs_table.php
CREATE TABLE IF NOT EXISTS credit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
