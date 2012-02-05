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

