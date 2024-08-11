CREATE TABLE `node` (
	`node_name`	varchar(50)	NOT NULL,
	PRIMARY KEY (`node_name`)
);

CREATE TABLE `detected_ip` (
	`ip_addr`	varchar(50)	NOT NULL,
	`country`	varchar(50)	NULL,
	PRIMARY KEY (`ip_addr`)
);

CREATE TABLE `rule` (
	`filter`	varchar(50)	NOT NULL,
	`node_name`	varchar(50)	NOT NULL,
	`notify_found`	bool	NOT NULL,
	`notify_ban`	bool	NOT NULL,
	PRIMARY KEY (`filter`, `node_name`),
	FOREIGN KEY (`node_name`) REFERENCES `node`(`node_name`)
);

CREATE TABLE `log` (
	`log_id`	integer	NOT NULL AUTO_INCREMENT,
	`detected_at`	datetime	NOT NULL,
	`filter`	varchar(50)	NOT NULL,
	`node_name`	varchar(50)	NOT NULL,
	`ip_addr`	varchar(50)	NOT NULL,
	`action`	varchar(10)	NOT NULL,
	PRIMARY KEY (`log_id`),  -- Make log_id the primary key
    INDEX (`detected_at`),   -- Optionally index detected_at if needed
	FOREIGN KEY (`filter`, `node_name`) REFERENCES `rule`(`filter`, `node_name`),
	FOREIGN KEY (`ip_addr`) REFERENCES `detected_ip`(`ip_addr`)
);
