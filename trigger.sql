CREATE TRIGGER trig_alarm_insert
BEFORE INSERT
ON CHARACTER.ALARM FOR EACH ROW
BEGIN
IF NEW.trojanid > 0 THEN
	INSERT into CHARACTER.TRO_IP set trojan_id = NEW.trojanid, ip_addr = NEW.sip, time = now();
	IF NEW.dns_name IS NOT NULL THEN
		INSERT into CHARACTER.TRO_DNS set trojan_id = NEW.trojanid, dnsname = NEW.dns_name;
	END IF;
END IF;
END;


-- 报表的数据查询
-- 涉及到的日期值都为INT，可以通过from_unixtime()方法转换为日期类型
select username, count(username) as c, Month(from_unixtime(createdtime)) from USERS group by Month(from_unixtime(createdtime)),username order by c;

