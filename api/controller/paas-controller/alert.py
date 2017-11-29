import requests
import json
import time
import datetime
from log import LOG

class AlertLevel:
    WARN = 1
    ERROR = 2
    FATAL = 4

class AlertType:
    MEM = 'ContainerMemory'

class Alert:
    URL = 'https://api.alert'
    AUTH = ('test', 'test')
    MAX_SMS_COUNT_PER_DAY = 2
    session = requests.Session()
    mem_alert_history = dict()
    sms_count_today = 0
    sms_last_date = None

    @staticmethod
    def clear_alert_history():
        delete_list = []
        for key, record in Alert.mem_alert_history.items():
            if time.time() - record.timestamp >= 4 * 3600:
                delete_list.append(key)
        for key in delete_list:
            Alert.mem_alert_history.pop(key)

    @staticmethod
    def remove_alert_history(key):
        if key in Alert.mem_alert_history:
            Alert.mem_alert_history.pop(key)

    @staticmethod
    def can_alert(alert_record):
        if alert_record.alert_level == AlertLevel.ERROR or alert_record.alert_level == AlertLevel.FATAL:
            if Alert.sms_last_date is None:
                return True
            now = datetime.datetime.now()
            if (now - Alert.sms_last_date).days > 0:
                return True
            elif Alert.sms_count_today < Alert.MAX_SMS_COUNT_PER_DAY:
                return True
            else:
                return False

        old_alert_record = Alert.mem_alert_history.get(alert_record.key, None)
        if old_alert_record is None:
            return True
        if alert_record.alert_level > old_alert_record.alert_level:
            return True
        elif alert_record.alert_level < old_alert_record.alert_level:
            return False

        # here, level is the same, lets compare interval
        time_delta = alert_record.timestamp - old_alert_record.timestamp
        if alert_record.alert_level == AlertLevel.WARN and time_delta > 5 * 60 and old_alert_record.times <= 5:
            return True

        return False

    @staticmethod
    def alert(record):
        Alert.clear_alert_history()
        if not Alert.can_alert(record):
            return False

        post_data = { 
            "hostname": record.hostname,
            "service": record.alert_type,
            "alert_level": record.alert_level,
            "ts_utc": record.timestamp,
            "err_msg": record.msg,
            "to_mail": ';'.join(record.mail_list),
            "to_phone": ';'.join(record.phone_list)
        }
        r = Alert.session.post(Alert.URL,
                auth=Alert.AUTH,
                data=json.dumps(post_data),
                verify=False,
                headers={'content-type': 'application/json'})
        if r.status_code != 201:
            LOG.error('Failed to send mail for message: {}'.format(record.msg))
            return False

        old_alert_record = Alert.mem_alert_history.get(record.key, None)
        if old_alert_record is not None:
            record.times = old_alert_record.times + 1
        else:
            record.times = 1
        Alert.mem_alert_history[record.key] = record

        if record.alert_level >= AlertLevel.ERROR:
            now = datetime.datetime.now()
            if Alert.sms_last_date is None or (now - Alert.sms_last_date).days > 0:
                Alert.sms_count_today = 1
            else:
                Alert.sms_count_today += 1
            Alert.sms_last_date = now
            LOG.info('Alert.sms_count_today = {}'.format(Alert.sms_count_today))
        return True

class AlertRecord:
    def __init__(self, key, alert_type, alert_level, msg, timestamp, hostname='', mail_list=None, phone_list=None):
        self.key = key
        self.alert_type = alert_type
        self.alert_level = alert_level
        self.timestamp = timestamp
        self.mail_list = mail_list
        self.hostname = hostname
        self.phone_list = phone_list
        self.msg = msg
        self.times = 0

class AlertManagerPod:
    def __init__(self):
        pass

    def check_pod(self, pod, app_controller):
        if not pod['is_ready'] or not pod['is_running']:
            return

        if app_controller.memory_controller is None:
            return

        memory_percent = round(float(pod['mem_usage'] - pod['mem_cache']) / float(pod['max_mem_limit']) * 100, 1)
        if memory_percent >= app_controller.memory_controller.warn_percent:
            msg = '{}:{}:cache={},usage={},percent={}%'.format(app_controller.name, pod['name'], pod['mem_cache'], pod['mem_usage'], memory_percent)
            alert_record = AlertRecord(key = pod['name'],
                                       alert_type = AlertType.MEM,
                                       alert_level = AlertLevel.WARN,
                                       timestamp = int(time.time()),
                                       msg = msg,
                                       hostname = pod['host_IP'],
                                       mail_list = app_controller.mail_list,
                                       phone_list = app_controller.phone_list)
            if Alert.alert(alert_record):
                LOG.info('sent mail: {}'.format(msg))
            LOG.warn(msg)
        else:
            Alert.remove_alert_history(pod['name'])

