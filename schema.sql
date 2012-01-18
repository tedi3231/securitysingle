-- Copyright 2009 FriendFeed
--
-- Licensed under the Apache License, Version 2.0 (the "License"); you may
-- not use this file except in compliance with the License. You may obtain
-- a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
-- WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
-- License for the specific language governing permissions and limitations
-- under the License.

-- To create the database:
--   CREATE DATABASE blog;
--   GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost' IDENTIFIED BY 'blog';
--
-- To reload the tables:
--   mysql --user=blog --password=blog --database=blog < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    userpass VARCHAR(50) NOT NULL,
    permission VARCHAR(512) NULL,
    createtime INT NOT NULL,
    remark VARCHAR(255) NOT NULL    
);

DROP TABLE IF EXISTS DNS_LIST;
CREATE TABLE DNS_LIST(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dnsname VARCHAR(255) NOT NULL,
    type INT NOT NULL,
    describ VARCHAR(255)
);

DROP TABLE IF EXISTS EVILIP_LIST;
CREATE TABLE EVILIP_LIST(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    startip BIGINT NOT NULL,
    endip BIGINT NOT NULL,
    describ varchar(255) 
);

DROP TABLE IF EXISTS TRO_IP;
CREATE TABLE TRO_IP(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ip_addr BIGINT NOT NULL,
    time INT NOT NULL,
    describ varchar(255) 
);

DROP TABLE IF EXISTS TRO_DNS;
CREATE TABLE TRO_DNS(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dnsname varchar(255) NOT NULL,    
    describ varchar(255) 
);

DROP TABLE IF EXISTS GLOBALPARA;
CREATE TABLE GLOBALPARA(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    beaterror INT DEFAULT 3,
    beatcount INT DEFAULT 5,
    dnsttl INT DEFAULT 60,
    tcplasted INT DEFAULT 60,
    tcpdivide INT DEFAULT 5,
    tcpcount INT DEFAULT 5000,
    httpsenddivide INT DEFAULT 5,
    httppostdivide INT DEFAULT 5,    
    describ varchar(255) 
);

DROP TABLE IF EXISTS ALARM;
CREATE TABLE ALARM(
    id    INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rid   INT NOT NULL,
    type  INT NOT NULL,
    class INT NOT NULL,
    trojanid INT NOT NULL,
    dip BIGINT NOT NULL,
    dmac varchar(18) NOT NULL,
    sip BIGINT NOT NULL,
    scc varchar(64) NOT NULL,
    time INT NOT NULL,    
    alarm_msg varchar(512) NOT NULL 
);

DROP TABLE IF EXISTS ALARM_EVENT;
CREATE TABLE ALARM_EVENT(
    alarm_id INT NOT NULL,
    event_id INT NOT NULL
);

DROP TABLE IF EXISTS EVENT;
CREATE TABLE EVENT(
    id    INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pid INT ,
    psid INT, 
    time INT,
    risk INT,
    sip BIGINT,
    sport INT,
    dip BIGINT,
    dmac varchar(18) ,
    dport INT,
    pro INT,
    sflag INT,
    extradata varchar(255),
    dns_name varchar(255)
);

DROP TABLE IF EXISTS RELATE_RULE;
CREATE TABLE RELATE_RULE(
    id    INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type INT,
    class INT,
    issequence INT,
    is_semicolon INT,
    rule VARCHAR(255) ,
    timeslice INT,
    direction INT,
    describ varchar(255),
    isuse INT
);

DROP TABLE IF EXISTS USER_TROJAN_RULE;
CREATE TABLE USER_TROJAN_RULE(
	id    INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	srcip BIGINT,
    sport VARCHAR(11),
	dstip BIGINT,
	dport VARCHAR(11),
	offset INT,
	dept   INT,
	proto  INT,
	signature VARCHAR(255),
	troname VARCHAR(32) NOT NULL,
	isuser INT NOT NULL,
	special INT NOT NULL,
	desrib VARCHAR(512)
);
