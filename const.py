"""Constants used by havcs."""
HAVCS_SERVICE_URL = 'https://havcs.ljr.im:8123'

ATTR_DEVICE_VISABLE  = 'visable'
ATTR_DEVICE_ID = 'device_id'
ATTR_DEVICE_ENTITY_ID = 'entity_id'
ATTR_DEVICE_TYPE = 'type'
ATTR_DEVICE_NAME = 'name'
ATTR_DEVICE_ZONE = 'zone'
ATTR_DEVICE_ICON = 'icon'
ATTR_DEVICE_ATTRIBUTES = 'attributes'
ATTR_DEVICE_ACTIONS  = 'actions'
ATTR_DEVICE_PROPERTIES = 'properties'

DATA_HAVCS_CONFIG = 'config'
DATA_HAVCS_MQTT = 'mqtt'
DATA_HAVCS_BIND_MANAGER = 'bind_manager'
DATA_HAVCS_HTTP_MANAGER = 'http_manager'
DATA_HAVCS_ITEMS = 'items'
DATA_HAVCS_SETTINGS = 'settings'
DATA_HAVCS_HANDLER = 'handler'

CONF_BROKER = 'broker'
CONF_DISCOVERY = 'discovery'
DEFAULT_DISCOVERY = False
INTEGRATION = 'havcs'
STORAGE_VERSION = 1
STORAGE_KEY = 'havcs'

CONF_ENTITY_KEY = 'entity_key'
CONF_APP_KEY = 'app_key'
CONF_APP_SECRET = 'app_secret'
CONF_URL  = 'url'
CONF_PROXY_URL = 'proxy_url'
CONF_SKIP_TEST  = 'skip_test'
CONF_DEVICE_CONFIG = 'device_config'
CONF_DEVICE_CONFIG_PATH = 'device_config_path'
CONF_SETTINGS_CONFIG_PATH = 'settings_config_path'
CONF_HA_URL = 'ha_url'

CONF_MODE = 'mode'

CLIENT_PALTFORM_DICT = {
    'jdwhale': 'https://alphadev.jd.com',
    'dueros': 'https://xiaodu.baidu.com',
    'dueros-test': 'https://xiaodu-dbp.baidu.com',
    'aligenie': 'https://open.bot.tmall.com'
}

HAVCS_ACTIONS_ALIAS = {
    'aligenie':{
        'turn_on': 'turnOn',
        'turn_off': 'turnOff',
        'increase_brightness': 'incrementBrightnessPercentage',
        'decrease_brightness': 'decrementBrightnessPercentage'
    },
    'dueros':{
        'turn_on': 'turnOn',
        'turn_off': 'turnOff',
        'increase_brightness': 'AdjustUpBrightness',
        'decrease_brightness': 'AdjustDownBrightness',
        'timing_turn_on': 'timingTurnOn',
        'timing_turn_off': 'timingTurnOff'
    },
    'jdwhale':{
        'turn_on': 'TurnOn',
        'turn_off': 'TurnOff',
        'increase_brightness': 'AdjustUpBrightness',
        'decrease_brightness': 'AdjustDownBrightness'
    }
}

DEVICE_PLATFORM_DICT = {    
    'dueros': {
        'cn_name': '小度'
    },
    'aligenie': {
        'cn_name': '天猫精灵'
    },
    'jdwhale': {
        'cn_name': '小京鱼'
    },
    'weixin': {
        'cn_name': '企业微信'
    }
}
DEVICE_TYPE_DICT = {
    'airpurifier': {
        'cn_name': '空气净化器',
        'icon': 'mdi-air-conditioner'
    },
    'climate': {
        'cn_name': '空调',
        'icon': 'mdi-air-conditioner'
    },
    'fan': {
        'cn_name': '风扇',
        'icon': 'mdi-pinwheel'
    },
    'light': {
        'cn_name': '灯',
        'icon': 'mdi-lightbulb'
    },
    'media_player': {
        'cn_name': '播放器',
        'icon': 'mdi-television-classic'
    },
    'switch': {
        'cn_name': '开关',
        'icon': 'mdi-toggle-switch'
    },
    'sensor': {
        'cn_name': '传感器',
        'icon': 'mdi-access-point-network'
    },
    'cover': {
        'cn_name': '窗帘',
        'icon': 'mdi-window-shutter'
    },
    'vacuum': {
        'cn_name': '扫地机',
        'icon': 'mdi-robot-vacuum-variant'
    },
    'humidifier': {
        'cn_name': '除湿机/加湿器',
        'icon': 'mdi:air-purifier'
    }
}
DEVICE_ACTION_DICT ={
    'turn_on': {
        'cn_name': '打开'
    },
    'turn_off': {
        'cn_name': '关闭'
    },
    'timing_turn_on': {
        'cn_name': '延时打开'
    },
    'timing_turn_off': {
        'cn_name': '延时关闭'
    },
    'query_temperature': {
        'cn_name': '查询温度'
    },
    'query_humidity': {
        'cn_name': '查询湿度'
    },
    'query_target_temperature': {
        'cn_name': '查询目标温度'
    },
    'query_target_humidity': {
        'cn_name': '查询目标湿度'
    },
    'query_state': {
        'cn_name': '查询设备状态'
    },
    'query_pm25': {
        'cn_name': '查询PM2.5'
    },
    'query_pm10': {
        'cn_name': '查询PM10'
    },
    'query_co2': {
        'cn_name': '查询二氧化碳含量'
    },
    'query_aqi': {
        'cn_name': '查询空气质量'
    },
    'query_location': {
        'cn_name': '查询设备所在位置'
    },
    'increase_brightness': {
        'cn_name': '调高亮度'
    },
    'decrease_brightness': {
        'cn_name': '调低亮度'
    },
    'set_mode': {
        'cn_name': '设置模式'
    },
    'play': {
        'cn_name': '播放'
    },
    'pause': {
        'cn_name': '暂停'
    },
    'continue': {
        'cn_name': '继续'
    },
    'increase_temperature': {
        'cn_name': '调高温度'
    },
    'decrease_temperature': {
        'cn_name': '调低温度'
    },
    'set_temperature': {
        'cn_name': '设置温度'
    },
    'increase_speed': {
        'cn_name': '增加风速'
    },
    'decrease_speed': {
        'cn_name': '减小风速'
    },
    'set_percentage': {
        'cn_name': '设置风速'
    },
    'set_humidity': {
        'cn_name': '设置湿度'
    },
    'set_hvac_mode': {
        'cn_name': '空调设置模式'
    },
    'set_oscillate': {
        'cn_name': '风扇摆风模式'
    },
    'unset_oscillate': {
        'cn_name': '风扇取消摆风模式'
    },
    'volume_up': {
        'cn_name': '调高音量'
    },
    'volume_down': {
        'cn_name': '调低音量'
    },
    'volume_set': {
        'cn_name': '设置音量'
    },
    'volume_mute': {
        'cn_name': '设置静音'
    },
    'tv_down': {
        'cn_name': '上一个频道'
    },
    'tv_up': {
        'cn_name': '下一个频道'
    }      
}

DEVICE_ATTRIBUTE_DICT = {
    'power_state': {
        'scale': '',
        'legalValue': '(ON, OFF)',
        'cn_name': '电源'
    },    
    'temperature': {
        'scale': '°C',
        'legalValue': 'DOUBLE',
        'cn_name': '温度'
    },
    'brightness': {
        'scale': '%',
        'legalValue': '[0.0, 100.0]',
        'cn_name': '亮度'
    },
    'illumination': {
        'scale': 'lm',
        'legalValue': '[0.0, 1000.0]',
        'cn_name': '照度'
    },
    'humidity': {
        'scale': '%',
        'legalValue': '[0.0, 100.0]',
        'cn_name': '湿度'
    },
    'hcho': {
        'scale': 'mg/m3',
        'legalValue': 'DOUBLE',
        'cn_name': '甲醛浓度'
    },
    'pm25': {
        'scale': 'μg/m3',
        'legalValue': '[0.0, 1000.0]',
        'cn_name': 'PM2.5浓度'
    },
    'pm10': {
        'scale': 'μg/m3',
        'legalValue': '[0.0, 10000.0]',
        'cn_name': 'PM10浓度'
    },
    'co2': {
        'scale': 'ppm',
        'legalValue': 'INTEGER',
        'cn_name': '二氧化碳浓度'
    },
    'mode': {
        'scale': '',
        'legalValue': '',
        'cn_name': '工作模式'
    },
    'havcmode': {
        'scale': '',
        'legalValue': '',
        'cn_name': '空调模式'
    },
    'fanspeed': {
        'scale': '',
        'legalValue': '',
        'cn_name': '风速'
    },
}