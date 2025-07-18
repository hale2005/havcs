import json
import uuid
import time
import logging

from .util import decrypt_device_id, encrypt_device_id
from .helper import VoiceControlProcessor, VoiceControlDeviceManager
from .const import DATA_HAVCS_BIND_MANAGER, INTEGRATION, ATTR_DEVICE_ACTIONS

_LOGGER = logging.getLogger(__name__)
# _LOGGER.setLevel(logging.DEBUG)

DOMAIN = 'dueros'
LOGGER_NAME = 'dueros'

async def createHandler(hass, entry):
    mode = ['handler']
    return VoiceControlDueros(hass, mode, entry)

class PlatformParameter:
    device_attribute_map_h2p = {
        'temperature': 'temperatureReading',
        'targettemperature': 'targetTemperature',
        'brightness': 'brightness',
        'humidity': 'humidity',
        'targethumidity': 'humidity',
        'pm25': 'PM25',
        'pm10': 'PM10',
        'co2': 'ppm',
        'hcho': 'hcho',
        'turnonstate': 'turnOnState',
        'mode': 'mode',
        'havc_mode': 'havcmode',
        'percentage': 'fanspeed',
        'state': 'state',
    }
    
    device_action_map_h2p ={
        'turn_on': 'turnOn',   #打开
        'turn_off': 'turnOff', #关闭
        'timing_turn_on': 'timingTurnOn',   #定时打开
        'timing_turn_off': 'timingTurnOff', #定时关闭
        'increase_brightness': 'incrementBrightnessPercentage',  #调亮灯光
        'decrease_brightness': 'decrementBrightnessPercentage',  #调暗灯光
        'set_brightness': 'setBrightnessPercentage',             #设置灯光亮度
        'set_color': 'setColor',                                #设置颜色
        'increase_temperature': 'incrementTemperature',         #升高温度
        'decrease_temperature': 'decrementTemperature',         #降低温度
        'set_temperature': 'setTemperature',                    #设置温度
        'increase_speed': 'incrementFanSpeed',                  #增加风速
        'decrease_speed': 'decrementFanSpeed',                  #减小风速
        'set_percentage': 'setFanSpeed',                        #设置风速        
        'pause': 'pause',                                       #暂停        
        'set_humidity': 'setHumidity',                          #设置湿度模式       
        'set_hvac_mode': 'setMode',                             #设置模式
        'set_oscillate': 'setMode',                         #设置模式
        'unset_oscillate': 'unSetMode',                     #取消设置的模式
        'volume_up': 'incrementVolume',                     #调高音量
        'volume_down': 'decrementVolume',                   #调低音量
        'volume_set': 'setVolume',                          #设置音量
        'volume_mute': 'setVolumeMute',                     #设置静音状态
        'tv_down': 'decrementTVChannel',                    #上一个频道
        'tv_up': 'incrementTVChannel',                      #下一个频道
        'media_pause': 'pause',
        'media_play': 'continue',
        'query_temperature': 'getTemperatureReading',           #查询当前温度
        'query_humidity': 'getHumidity',                        #查询湿度
        'query_targettemperature': 'getTargetTemperature',     #查询目标温度
        'query_targethumidity': 'getTargetHumidity',           #查询目标湿度 
        'query_state': 'getState',                #查询设备所有状态
        'query_pm25': 'getAirPM25',                    #查询PM2.5
        'query_pm10': 'getAirPM10',          #查询PM10
        'query_co2': 'getCO2Quantity',          #查询二氧化碳含量
        'query_aqi': 'getAirQualityIndex',      #查询空气质量
        'query_location': 'getLocation',        #查询设备所在位置
        'query_turnonstate': 'getTurnOnState',    #查询开关状态
        'set_colortemperature': 'setColorTemperature' ,  #设置灯光色温
        'increment_colortemperature': 'incrementColorTemperature' ,  #增高灯光色温
        'decrement_colortemperature': 'decrementColorTemperature' ,  #降低灯光色温
        # ' ': 'setPower' ,  #设置功率
        # ' ': 'incrementPower' ,  #增大功率
        # ' ': 'decrementPower' ,  #减小功率
        # ' ': 'setGear' ,  #设置档位
        # ' ': 'timingSetMode' ,  #定时设置模式
        # ' ': 'timingUnsetMode' ,  #定时取消设置的模式
        # ' ': 'setTVChannel' ,  #设置频道
        # ' ': 'returnTVChannel' ,  #返回上个频道
        # ' ': 'chargeTurnOn' ,  #开始充电
        # ' ': 'chargeTurnOff' ,  #停止充电
        # ' ': 'getOilCapacity' ,  #查询油量
        # ' ': 'getElectricityCapacity' ,  #查询电量
        # ' ': 'setLockState' ,  #上锁/解锁
        # ' ': 'getLockState' ,  #查询锁状态
        # ' ': 'setSuction' ,  #设置吸力
        # ' ': 'setWaterLevel' ,  #设置水量
        # ' ': 'setCleaningLocation' ,  #设置清扫位置
        # ' ': 'setComplexActions' ,  #执行自定义复杂动作
        # ' ': 'setDirection' ,  #设置移动方向
        # ' ': 'submitPrint' ,  #打印
        # 'increment_humidity': 'incrementHumidity',              #增大湿度
        # 'decrement_humidity': 'decrementHumidity',              #降低湿度 
        # ' ': 'getWaterQuality' ,  #查询水质
        # ' ': 'getTimeLeft' ,  #查询剩余时间
        # ' ': 'getRunningStatus' ,  #查询运行状态
        # ' ': 'getRunningTime' ,  #查询运行时间
        # ' ': 'setTimer' ,  #设备定时
        # ' ': 'timingCancel' ,  #取消设备定时
        # ' ': 'reset' ,  #设备复位
        # ' ': 'incrementHeight' ,  #升高高度
        # ' ': 'decrementHeight' ,  #降低高度
        # ' ': 'setSwingAngle' ,  #设置摆风角度
        # ' ': 'getFanSpeed' ,  #查询风速
        # ' ': 'incrementMist' ,  #增大雾量
        # ' ': 'decrementMist' ,  #见效雾量
        # ' ': 'setMist' ,  #设置雾量
        # ' ': 'startUp' ,  #设备启动
        # ' ': 'setFloor' ,  #设置电梯楼层
        # ' ': 'decrementFloor' ,  #电梯按下
        # ' ': 'incrementFloor' ,  #电梯按上
        # ' ': 'incrementSpeed' ,  #增加速度
        # ' ': 'decrementSpeed' ,  #降低速度
        # ' ': 'setSpeed' ,  #设置速度
        # ' ': 'getSpeed' ,  #获取速度
        # ' ': 'getMotionInfo' ,  #获取跑步信息
        # ' ': 'turnOnBurner' ,  #打开灶眼
        # ' ': 'turnOffBurner' ,  #关闭灶眼
        # ' ': 'timingTurnOnBurner' ,  #定时打开灶眼
        # ' ': 'timingTurnOffBurner' ,  #定时关闭灶眼
    }
    _device_type_alias = {
        "LIGHT": "电灯",
        "AIR_CONDITION": "空调",
        "CURTAIN": "窗帘",
        "CURT_SIMP": "窗纱",
        "SOCKET": "插座",
        "SWITCH": "开关",
        "FRIDGE": "冰箱",
        "WATER_PURIFIER": "净水器",
        "HUMIDIFIER": "加湿器",
        "DEHUMIDIFIER": "除湿器",
        "INDUCTION_COOKER": "电磁炉",
        "AIR_PURIFIER": "空气净化器",
        "WASHING_MACHINE": "洗衣机",
        "WATER_HEATER": "热水器",
        "GAS_STOVE": "燃气灶",
        "TV_SET": "电视机",
        "OTT_BOX": "网络盒子",
        "RANGE_HOOD": "油烟机",
        "FAN": "电风扇",
        "PROJECTOR": "投影仪",
        "SWEEPING_ROBOT": "扫地机器人",
        "KETTLE": "热水壶",
        "MICROWAVE_OVEN": "微波炉",
        "PRESSURE_COOKER": "压力锅",
        "RICE_COOKER": "电饭煲",
        "HIGH_SPEED_BLENDER": "破壁机",
        "AIR_FRESHER": "新风机",
        "CLOTHES_RACK": "晾衣架",
        "OVEN": "烤箱设备",
        "STEAM_OVEN": "蒸烤箱",
        "STEAM_BOX": "蒸箱",
        "HEATER": "电暖器",
        "WINDOW_OPENER": "开窗器",
        "WEBCAM": "摄像头",
        "CAMERA": "相机",
        "ROBOT": "机器人",
        "PRINTER": "打印机",
        "WATER_COOLER": "饮水机",
        "FISH_TANK": "鱼缸",
        "WATERING_DEVICE": "浇花器",
        "SET_TOP_BOX": "机顶盒",
        "AROMATHERAPY_MACHINE": "香薰机",
        "DVD": "DVD",
        "SHOE_CABINET": "鞋柜",
        "WALKING_MACHINE": "走步机",
        "TREADMILL": "跑步机",
        "BED": "床",
        "YUBA": "浴霸",
        "SHOWER": "花洒",
        "BATHTUB": "浴缸",
        "DISINFECTION_CABINET": "消毒柜",
        "DISHWASHER": "洗碗机",
        "SOFA": "沙发品类",
        "DOOR_BELL": "门铃",
        "ELEVATOR": "电梯",
        "WEIGHT_SCALE": "体重秤",
        "BODY_FAT_SCALE": "体脂秤",
        "WALL_HUNG_GAS_BOILER": "壁挂炉",
        "SCENE_TRIGGER": "描述特定设备的组合场景，设备之间没有相互关联，无特定操作顺序",
        "ACTIVITY_TRIGGER": "描述特定设备的组合场景。场景中的设备必须以指定顺序操作。如“观看优酷视频”场景中必须先打开电视机，然后打开HDMI1。"
    }


    device_type_map_h2p = {
        'climate': 'AIR_CONDITION',
        'fan': 'FAN',
        'light': 'LIGHT',
        'media_player': 'TV_SET',
        'switch': 'SWITCH',
        'sensor': 'SENSOR',
        'cover': 'CURTAIN',
        'vacuum': 'SWEEPING_ROBOT',
        'humidifier': 'DEHUMIDIFIER',
        }

    _service_map_p2h = {
        # 模式和平台设备类型不影响
        'fan': {
            'IncrementFanSpeedRequest': lambda state, attributes, payload: (['fan'], ['increase_speed'], [{'percentage_step': 20}]),
            'DecrementFanSpeedRequest': lambda state, attributes, payload: (['fan'], ['decrease_speed'], [{'percentage_step': 20}]),
            'SetFanSpeedRequest': lambda state, attributes, payload: (['fan'], ['set_percentage'], [{'percentage': min(payload['fanSpeed']['value']*25,100)}]),
            'SetModeRequest': lambda state, attributes, payload: (['fan'], [payload['mode']['value'].lower().replace('swing','oscillate')], [{'oscillating': 'true'}]),
            'UnsetModeRequest': lambda state, attributes, payload: (['fan'], [payload['mode']['value'].lower().replace('swing','oscillate')], [{'oscillating': 'false'}]),
        },
        'climate': {
            'TurnOnRequest':  'turn_on',
            'TurnOffRequest': 'turn_off',
            'TimingTurnOnRequest': 'turn_on',
            'TimingTurnOffRequest': 'turn_off',
            'SetTemperatureRequest': lambda state, attributes, payload: (['climate'], ['set_temperature'], [{'temperature': payload['targetTemperature']['value']}]),
            'IncrementTemperatureRequest': lambda state, attributes, payload: (['climate'], ['set_temperature'],[ {'temperature': min(state.attributes['temperature'] + payload['deltaValue']['value'], 30)}]),
            'DecrementTemperatureRequest': lambda state, attributes, payload: (['climate'], ['set_temperature'], [{'temperature': max(state.attributes['temperature'] - payload['deltaValue']['value'], 16)}]),
            'SetModeRequest': lambda state, attributes, payload: (['climate'], ['set_hvac_mode'], [{'hvac_mode': payload['mode']['value'].lower().replace('fan','fan_only').replace('dehumidification','dry')}]),
            'SetFanSpeedRequest': lambda state, attributes, payload: (['climate'], ['set_fan_mode'], [{'fan_mode': payload['fanSpeed']['level'].replace('middle','medium').replace('_','-').replace('quite','Quiet').replace('min','Quiet').replace('powerful','Turbo')}]), 
        },
        'media_player': {
            'TurnOnRequest':  'turn_on',
            'TurnOffRequest': 'turn_off',
            'TimingTurnOnRequest': 'turn_on',
            'TimingTurnOffRequest': 'turn_off', 
            'PauseRequest': 'media_pause',
            'ContinueRequest': 'media_play',
            'IncrementTVChannelRequest': lambda state, attributes, payload: (['wukongtv'], ['tv_up']),
            'DecrementTVChannelRequest': lambda state, attributes, payload: (['wukongtv'], ['tv_down']),
            'IncrementVolumeRequest': 'volume_up',
            'DecrementVolumeRequest': 'volume_down',
            'SetVolumeRequest': lambda state, attributes, payload: (['media_player'], ['volume_set'], [{'volume_level': payload['deltaValue']['value']}]),
            'SetVolumeMuteRequest': 'volume_mute',
        },
        'humidifier': {
            'TurnOnRequest':  'turn_on',
            'TurnOffRequest': 'turn_off',
            'TimingTurnOnRequest': 'turn_on',
            'TimingTurnOffRequest': 'turn_off', 
            'SetHumidityRequest': lambda state, attributes, payload: (['humidifier'], ['set_humidity'], [{'temperature': payload['deltValue']['value']}]),
        },
        'cover': {
            'TurnOnRequest':  'open_cover',
            'TurnOffRequest': 'close_cover',
            'TimingTurnOnRequest': 'open_cover',
            'TimingTurnOffRequest': 'close_cover', 
            'PauseRequest': 'stop_cover',
        },
        'vacuum': {
            'TurnOnRequest':  'start',
            'TurnOffRequest': 'return_to_base',
            'TimingTurnOnRequest': 'start',
            'TimingTurnOffRequest': 'return_to_base',
            'SetSuctionRequest': lambda state, attributes, payload: (['vacuum'], ['set_fan_speed'], [{'fan_speed': 90 if payload['suction']['value'] == 'STRONG' else 60}]),
        },
        'switch': {
            'TurnOnRequest': 'turn_on',
            'TurnOffRequest': 'turn_off',
            'TimingTurnOnRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'on', 'duration': int(payload['timestamp']['value']) - int(time.time())}]),
            'TimingTurnOffRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'off', 'duration': int(payload['timestamp']['value']) - int(time.time())}])
        },
        'light': {
            'TurnOnRequest': 'turn_on',
            'TurnOffRequest': 'turn_off',
            'TimingTurnOnRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'on', 'duration': int(payload['timestamp']['value']) - int(time.time())}]),
            'TimingTurnOffRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'off', 'duration': int(payload['timestamp']['value']) - int(time.time())}]),
            'SetBrightnessPercentageRequest': lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': payload['brightness']['value']}]),
            'IncrementBrightnessPercentageRequest': lambda state, attributes, payload: (['light'], ['turn_on'],[ {'brightness_pct': min(state.attributes['brightness'] / 255 * 100 + payload['deltaPercentage']['value'], 100)}]),
            'DecrementBrightnessPercentageRequest': lambda state, attributes, payload: (['light'], ['turn_on'], [{'brightness_pct': max(state.attributes['brightness'] / 255 * 100 - payload['deltaPercentage']['value'], 0)}]),
            'SetColorRequest': lambda state, attributes, payload: (['light'], ['turn_on'], [{'hs_color': [float(payload['color']['hue']), float(payload['color']['saturation']) * 100], 'brightness_pct': float(payload['color']['brightness']) * 100}]),
            'SetColorTemperatureRequest': lambda state, attributes, payload: (['light'], ['turn_on'], [{'kelvin': payload['colorTemperatureInKelvin']}]),
            'IncrementColorTemperatureRequest': lambda state, attributes, payload: (['light'], ['turn_on'],[ {'kelvin': min(state.attributes['color_temp_kelvin'] + payload['deltaPercentage']['value'] * (int(state.attributes['max_color_temp_kelvin']) - int(state.attributes['min_color_temp_kelvin'])) / 100, state.attributes['max_color_temp_kelvin'])}]),
            'DecrementColorTemperatureRequest': lambda state, attributes, payload: (['light'], ['turn_on'], [{'kelvin': max(state.attributes['color_temp_kelvin'] - payload['deltaPercentage']['value'] * (int(state.attributes['max_color_temp_kelvin']) - int(state.attributes['min_color_temp_kelvin'])) / 100, state.attributes['min_color_temp_kelvin'])}]),
        },
        'havcs':{
            'TurnOnRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_on']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
            'TurnOffRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['turn_off']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_off'], [{}]),
            'IncrementBrightnessPercentageRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increase_brightness']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
            'DecrementBrightnessPercentageRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_brightness']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),                 
            'TimingTurnOnRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'custom:havcs_actions/timing_turn_on', 'duration': int(payload['timestamp']['value']) - int(time.time())}]),
            'TimingTurnOffRequest': lambda state, attributes, payload: (['common_timer'], ['set'], [{'operation': 'custom:havcs_actions/timing_turn_off', 'duration': int(payload['timestamp']['value']) - int(time.time())}]),
            'IncrementColorTemperatureRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increment_colortemperature']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increment_colortemperature']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['increment_colortemperature']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),
            'DecrementColorTemperatureRequest': lambda state, attributes, payload:([cmnd[0] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_colortemperature']], [cmnd[1] for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_colortemperature']], [json.loads(cmnd[2]) for cmnd in attributes[ATTR_DEVICE_ACTIONS]['decrease_colortemperature']]) if attributes.get(ATTR_DEVICE_ACTIONS) else (['input_boolean'], ['turn_on'], [{}]),                 
        }

    }
    # action:[{Platfrom Attr: HA Attr},{}]
    _query_map_p2h = {
        'GetTemperatureReadingRequest':{'temperatureReading':{'value':'%temperatureReading','scale': 'CELSIUS'}},
    }


class VoiceControlDueros(PlatformParameter, VoiceControlProcessor):
    def __init__(self, hass, mode, entry):
        self._hass = hass
        self._mode = mode
        self.vcdm = VoiceControlDeviceManager(entry, DOMAIN, self.device_action_map_h2p, self.device_attribute_map_h2p, self._service_map_p2h, self.device_type_map_h2p, self._device_type_alias)
    def _errorResult(self, errorCode, messsage=None):
        """Generate error result"""
        error_code_map = {
            'INVALIDATE_CONTROL_ORDER': 'invalidate control order',
            'SERVICE_ERROR': 'TargetConnectivityUnstableError',
            'DEVICE_NOT_SUPPORT_FUNCTION': 'NotSupportedInCurrentModeError',
            'INVALIDATE_PARAMS': 'ValueOutOfRangeError',
            'DEVICE_IS_NOT_EXIST': 'DriverInternalError',
            'IOT_DEVICE_OFFLINE': 'TargetOfflineError',
            'ACCESS_TOKEN_INVALIDATE': 'InvalidAccessTokenError'            
        }
        messages = {
            'INVALIDATE_CONTROL_ORDER': 'invalidate control order',
            'SERVICE_ERROR': 'service error',
            'DEVICE_NOT_SUPPORT_FUNCTION': 'device not support',
            'INVALIDATE_PARAMS': 'invalidate params',
            'DEVICE_IS_NOT_EXIST': 'device is not exist',
            'IOT_DEVICE_OFFLINE': 'device is offline',
            'ACCESS_TOKEN_INVALIDATE': 'access_token is invalidate'
        }
        return {'errorCode': error_code_map.get(errorCode, 'undefined'), 'message': messsage if messsage else messages.get(errorCode, 'undefined')}

    async def handleRequest(self, data, auth = False, request_from = "http"):
        """Handle request"""
        _LOGGER.info("[%s] Handle Request:\n%s", LOGGER_NAME, data)

        header = self._prase_command(data, 'header')
        action = self._prase_command(data, 'action')
        namespace = self._prase_command(data, 'namespace')
        p_user_id = self._prase_command(data, 'user_uid')
        result = {}
        # uid = p_user_id+'@'+DOMAIN

        if auth:
            namespace = header['namespace']
            if namespace == 'DuerOS.ConnectedHome.Discovery':
                action = 'DiscoverAppliancesResponse'
                err_result, discovery_devices, entity_ids = self.process_discovery_command(request_from)
                result = {'discoveredAppliances': discovery_devices}
                if DATA_HAVCS_BIND_MANAGER in self._hass.data[INTEGRATION]:
                    await self._hass.data[INTEGRATION][DATA_HAVCS_BIND_MANAGER].async_save_changed_devices(entity_ids, DOMAIN, p_user_id)
            elif namespace == 'DuerOS.ConnectedHome.Control':
                err_result, properties = await self.process_control_command(data)
                result = err_result if err_result else {'attributes': properties}
                action = action.replace('Request', 'Confirmation') # fix
            elif namespace == 'DuerOS.ConnectedHome.Query':
                err_result, properties = self.process_query_command(data)
                result = err_result if err_result else properties
                action = action.replace('Request', 'Response') # fix 主动上报会收到ReportStateRequest action，可以返回设备的其他属性信息不超过10个
            else:
                result = self._errorResult('SERVICE_ERROR')
        else:
            result = self._errorResult('ACCESS_TOKEN_INVALIDATE')
        
        # Check error
        header['name'] = action
        if 'errorCode' in result:
            header['name'] = result['errorCode']
            result={}

        response = {'header': header, 'payload': result}

        _LOGGER.info("[%s] Respnose: %s", LOGGER_NAME, response)
        return response

    def _prase_command(self, command, arg):
        header = command['header']
        payload = command['payload']

        if arg == 'device_id':
            return payload['appliance']['applianceId']
        elif arg == 'action':
            return header['name']
        elif arg == 'user_uid':
            return payload.get('openUid','')
        else:
            return command.get(arg)

    def _discovery_process_propertites(self, device_properties):
        properties = []
        for device_property in device_properties:
            name = self.device_attribute_map_h2p.get(device_property.get('attribute'))
            state = self._hass.states.get(device_property.get('entity_id'))
            if name:
                value = state.state if state else 'unavailable'
                if name == 'temperature':
                    scale = 'CELSIUS'
                    legalValue = 'DOUBLE'
                if name == 'targettemperature':
                    scale = 'CELSIUS'
                    legalValue = 'DOUBLE'
                elif name == 'brightness':
                    scale = '%'
                    legalValue = '[0.0, 100.0]'                
                elif name == 'humidity':
                    scale = '%'
                    legalValue = '[0.0, 100.0]'
                elif name == 'aqi':
                    scale = ''
                    legalValue = 'INTEGER'
                elif name == 'pm25':
                    scale = 'μg/m3'
                    legalValue = 'DOUBLE'
                elif name == 'pm10':
                    scale = 'μg/m3'
                    legalValue = 'DOUBLE'
                elif name == 'co2':
                    scale = 'ppm'
                    legalValue = 'DOUBLE'
                elif name == 'hcho':
                    scale = 'mg/m³'
                    legalValue = 'DOUBLE'
                elif name == 'turnOnState':
                    if value != 'on':
                        value = 'OFF'
                    else:
                        value = 'ON'
                    scale = ''
                    legalValue = '(ON, OFF)'                
                elif name == 'havc_mode':
                    scale = ''
                    legalValue = '("off", "heat_cool", "cool", "heat", "fan_only", "dry")'
                elif name == 'mode':
                    scale = ''
                    legalValue = '(POWERFUL, NORMAL, QUIET)'
                else:
                    _LOGGER.warning("[%s] %s has unsport attribute %s", LOGGER_NAME, device_property.get('entity_id'), name)
                    continue
                properties += [{'name': name, 'value': value, 'scale': scale, 'timestampOfSample': int(time.time()), 'uncertaintyInMilliseconds': 1000, 'legalValue': legalValue }]
        _LOGGER.debug(properties)
        _LOGGER.debug("properties list")
        return properties if properties else [{'name': 'turnOnState', 'value': 'OFF', 'scale': '', 'timestampOfSample': int(time.time()), 'uncertaintyInMilliseconds': 1000, 'legalValue': '(ON, OFF)' }]
        
    def _discovery_process_actions(self, device_properties, raw_actions):
        actions = []
        for device_property in device_properties:
            name = self.device_attribute_map_h2p.get(device_property.get('attribute'))
            if name:
                action = self.device_action_map_h2p.get('query_'+name)
                if action:
                    actions += [action,]
        for raw_action in raw_actions:
            action = self.device_action_map_h2p.get(raw_action)
            if action:
                actions += [action,]
        return list(set(actions))

    def _discovery_process_device_type(self, raw_device_type):
        # raw_device_type guess from device_id's domain transfer to platform style
        return raw_device_type if raw_device_type in self._device_type_alias else self.device_type_map_h2p.get(raw_device_type)

    def _discovery_process_device_info(self, device_id,  device_type, device_name, zone, properties, actions):
        return {
            'applianceId': encrypt_device_id(device_id),
            'friendlyName': device_name,
            'friendlyDescription': device_name,
            'additionalApplianceDetails': [],
            'applianceTypes': [device_type],
            'isReachable': True,
            'manufacturerName': 'HomeAssistant',
            'modelName': 'HomeAssistant',
            'version': '1.0',
            'actions': actions,
            'attributes': properties,
            }


    def _control_process_propertites(self, device_properties, action) -> None:
        
        return self._discovery_process_propertites(device_properties)

    def _query_process_propertites(self, device_properties, action) -> None:
        properties = {}
        queryresponseattributes = ["humidity", "turnonstate", "state", "location"]
        action = action.replace('Request', '').replace('Get', '')
        if action in self._query_map_p2h:
            for property_name, attr_template in self._query_map_p2h[action].items():
                formattd_property = self.vcdm.format_property(self._hass, device_properties, attr_template)
                properties.update({property_name:formattd_property})
                _LOGGER.debug("properties=  %s : %s", property_name, formattd_property)
        else:
            for device_property in device_properties:                
                _LOGGER.debug("device_property")
                _LOGGER.debug(device_property)
                state = self._hass.states.get(device_property.get('entity_id'))
                value = state.attributes.get(device_property.get('attribute'), state.state) if state else None
                _LOGGER.debug(state)
                _LOGGER.debug(value)
                # if isinstance(value, str):
                    # value = value.replace("on","ON").replace("off","OFF")
                if device_property.get('entity_id').startswith('climate.') and action == "TemperatureReading":
                    value = state.attributes.get("current_temperature", state.state) if state else None
                if device_property.get('entity_id').startswith('humidifier.') and action == "Humidity":
                    value = state.attributes.get("current_humidity", state.state) if state else None
                if device_property.get('entity_id').startswith('humidifier.') and action == "TargetHumidity":
                    value = state.attributes.get("humidity", state.state) if state else None                
                if value:
                    # if action == "Humidity" or action == "TargetHumidity":
                        # value = float(value)/100
                    if device_property.get('attribute').lower() in action.lower():
                        name = action[0].lower() + action[1:]
                        name = name.replace("targetHumidity", "humidity")       # fix除湿机目标湿度
                        name = name.replace("airPM25", "PM25")
                        name = name.replace("airPM10", "PM10")
                        name = name.replace("cO2Quantity", "ppm")
                        name = name.replace("airQualityIndex", "AQI")                        
                        _LOGGER.debug(name)
                        if name.lower() in queryresponseattributes:                                    
                            if name == 'humidity':
                                scale = '%'
                            elif name == 'state':
                                scale = ''
                            elif name == 'location':
                                scale = ''
                            elif name == 'turnOnState':
                                if value != 'on':
                                    value = 'OFF'
                                else:
                                    value = 'ON'
                                scale = ''                         
                            formattd_property = {"attributes": [{'name': name, 'value': value, 'scale': scale, 'timestampOfSample': int(time.time()), 'uncertaintyInMilliseconds': 1000}]}
                        else:
                            formattd_property = {name: {'value': value}}                        
                        properties.update(formattd_property)                
                    _LOGGER.debug("value：%s", value)
        return properties

    def _decrypt_device_id(self, device_id) -> None:
        return decrypt_device_id(device_id)

    def report_device(self, device_id):

        payload = []
        for p_user_id in self._hass.data[INTEGRATION][DATA_HAVCS_BIND_MANAGER].get_uids(DOMAIN, device_id):
            _LOGGER.info("[%s] report device for %s:\n", LOGGER_NAME, p_user_id)
            report = {
                "header": {
                    "namespace": "DuerOS.ConnectedHome.Control",
                    "name": "ChangeReportRequest",
                    "messageId": str(uuid.uuid4()),
                    "payloadVersion": "1"
                },
                "payload": {
                    "botId": "",
                    "openUid": p_user_id,
                    "appliance": {
                        "applianceId": encrypt_device_id(device_id),
                        "attributeName": "turnOnState"
                    }
                }
            }
            payload.append(report)
        return payload