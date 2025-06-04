import pyvisa_py
import pyvisa
import enum
import math

TRUE_STRINGS = {'TRUE', 'YES', 'ON', '1'}
FALSE_STRINGS = {'FALSE', 'NO', 'OFF', '0', 'NONE', ''}

class BtStandard(enum.Enum):
    """
    BT 测试的三种制式
    """
    BDR = 0
    EDR = 1
    BLE = 2


class MEASChannel(enum.Enum):
    """
    WIFI Channel的枚举类
    """
    CH0 = 0
    CH1 = 1
    CH2 = 2
    CH3 = 3
    CH4 = 4
    CH5 = 5
    CH6 = 6
    CH7 = 7
    CH8 = 8
    CH9 = 9
    CH10 = 10
    CH11 = 11
    CH12 = 12
    CH13 = 13
    CH14 = 14
    CH15 = 15
    CH16 = 16
    CH17 = 17
    CH18 = 18
    CH19 = 19
    CH20 = 20
    CH21 = 21
    CH22 = 22
    CH23 = 23
    CH24 = 24
    CH25 = 25
    CH26 = 26
    CH27 = 27
    CH28 = 28
    CH29 = 29
    CH30 = 30
    CH31 = 31
    CH32 = 32
    CH33 = 33
    CH34 = 34
    CH35 = 35
    CH36 = 36
    CH37 = 37
    CH38 = 38
    CH39 = 39
    CH40 = 40
    CH41 = 41
    CH42 = 42
    CH43 = 43
    CH44 = 44
    CH45 = 45
    CH46 = 46
    CH47 = 47
    CH48 = 48
    CH49 = 49
    CH50 = 50
    CH51 = 51
    CH52 = 52
    CH53 = 53
    CH54 = 54
    CH55 = 55
    CH56 = 56
    CH57 = 57
    CH58 = 58
    CH59 = 59
    CH60 = 60
    CH61 = 61
    CH62 = 62
    CH63 = 63
    CH64 = 64
    CH65 = 65
    CH66 = 66
    CH67 = 67
    CH68 = 68
    CH69 = 69
    CH70 = 70
    CH71 = 71
    CH72 = 72
    CH73 = 73
    CH74 = 74
    CH75 = 75
    CH76 = 76
    CH77 = 77
    CH78 = 78
    CH79 = 79
    CH80 = 80
    CH81 = 81
    CH82 = 82
    CH83 = 83
    CH84 = 84
    CH85 = 85
    CH86 = 86
    CH87 = 87
    CH88 = 88
    CH89 = 89
    CH90 = 90
    CH91 = 91
    CH92 = 92
    CH93 = 93
    CH94 = 94
    CH95 = 95
    CH96 = 96
    CH97 = 97
    CH98 = 98
    CH99 = 99
    CH100 = 100
    CH101 = 101
    CH102 = 102
    CH103 = 103
    CH104 = 104
    CH105 = 105
    CH106 = 106
    CH107 = 107
    CH108 = 108
    CH109 = 109
    CH110 = 110
    CH111 = 111
    CH112 = 112
    CH113 = 113
    CH114 = 114
    CH115 = 115
    CH116 = 116
    CH117 = 117
    CH118 = 118
    CH119 = 119
    CH120 = 120
    CH121 = 121
    CH122 = 122
    CH123 = 123
    CH124 = 124
    CH125 = 125
    CH126 = 126
    CH127 = 127
    CH128 = 128
    CH129 = 129
    CH130 = 130
    CH131 = 131
    CH132 = 132
    CH133 = 133
    CH134 = 134
    CH135 = 135
    CH136 = 136
    CH137 = 137
    CH138 = 138
    CH139 = 139
    CH140 = 140
    CH141 = 141
    CH142 = 142
    CH143 = 143
    CH144 = 144
    CH145 = 145
    CH146 = 146
    CH147 = 147
    CH148 = 148
    CH149 = 149
    CH150 = 150
    CH151 = 151
    CH152 = 152
    CH153 = 153
    CH154 = 154
    CH155 = 155
    CH156 = 156
    CH157 = 157
    CH158 = 158
    CH159 = 159
    CH160 = 160
    CH161 = 161
    CH162 = 162
    CH163 = 163
    CH164 = 164
    CH165 = 165


class MEASMeasurand(enum.Enum):
    AVG_POWER = 0
    PER = 1  # Packet error rate
    BER = 2  # Bit error rate

    # region WLAN
    EVM = 10
    FREQ_ERROR = 11
    SYMBOL_CLOCK_ERROR = 12
    FREQ_LEAKAGE = 13
    OCCUPIED_BANDWIDTH = 14
    SPECTRUM_MASK_MARGIN_LO_1 = 15
    SPECTRUM_MASK_MARGIN_LO_2 = 16
    SPECTRUM_MASK_MARGIN_LO_3 = 17
    SPECTRUM_MASK_MARGIN_LO_4 = 18
    SPECTRUM_MASK_MARGIN_UP_1 = 19
    SPECTRUM_MASK_MARGIN_UP_2 = 20
    SPECTRUM_MASK_MARGIN_UP_3 = 21
    SPECTRUM_MASK_MARGIN_UP_4 = 22
    SPECTRAL_FLATNESS_MIN_MARGIN = 23
    SENSITIVITY_MIN = 24
    SENSITIVITY_MAX = 25
    # endregion

    # region BDR
    SPECTRUM_20DB_BANDWIDTH = 100
    SPECTRUM_ACP_MIN_MARGIN = 101
    DELTA_F1_AVG = 102
    DELTA_F2_AVG = 103
    DELTA_F2_MAX = 104
    DELTA_F2_F1_AVG_RATIO = 105
    INITIAL_CARRIER_FREQ_ERR = 106
    CARRIER_FREQ_DRIFT = 107
    BIT_ERROR_RATE = 108

    SINGLE_SLOT_SENSITIVITY = 109
    MULTI_SLOT_SENSITIVITY = 110
    # endregion

    # region EDR
    EDR_RELATIVE_TRANSMIT_POWER = 200
    EDR_OMEGA_I = 201
    EDR_OMEGA_0 = 202
    EDR_OMEGA_I0 = 203
    EDR_DEVM_AVG = 204
    EDR_DEVM_PEAK = 205
    EDR_ACP_MIN_MARGIN = 206
    EDR_SENSITIVITY = 207
    # endregion

    # region BLE
    LE_OUTPUT_POWER = 300
    LE_DELTA_F1_AVG = 301
    LE_DELTA_F2_AVG = 302
    LE_DELTA_F2_MAX = 303
    LE_DELTA_F2_F1_AVG_RATIO = 304
    LE_INITIAL_FREQ_ERR = 305
    LE_FN_MAX = 306
    DELTA_F0_FN_MAX = 307
    DELTA_F1_F0 = 308  # For DataRate 1Mbps/2Mbps
    DELTA_FN_FN5_MAX = 309  # For DataRate 1Mbps/2Mbps
    DELTA_F3_F0 = 400  # For DataRate 125Kbps
    DELTA_FN_FN3_MAX = 401  # For DataRate 125Kbps
    LE_ACP_MIN_MARGIN = 402


class MEASCenterFreq(enum.Enum):
    """
	BT frequency range: 2402MHz - 2480MHz
	WLAN frequency range: 2412MHz - 5825MHz
	"""
    F_2402 = 2402
    F_2403 = 2403
    F_2404 = 2404
    F_2405 = 2405
    F_2406 = 2406
    F_2407 = 2407
    F_2408 = 2408
    F_2409 = 2409
    F_2410 = 2410
    F_2411 = 2411
    F_2412 = 2412
    F_2413 = 2413
    F_2414 = 2414
    F_2415 = 2415
    F_2416 = 2416
    F_2417 = 2417
    F_2418 = 2418
    F_2419 = 2419
    F_2420 = 2420
    F_2421 = 2421
    F_2422 = 2422
    F_2423 = 2423
    F_2424 = 2424
    F_2425 = 2425
    F_2426 = 2426
    F_2427 = 2427
    F_2428 = 2428
    F_2429 = 2429
    F_2430 = 2430
    F_2431 = 2431
    F_2432 = 2432
    F_2433 = 2433
    F_2434 = 2434
    F_2435 = 2435
    F_2436 = 2436
    F_2437 = 2437
    F_2438 = 2438
    F_2439 = 2439
    F_2440 = 2440
    F_2441 = 2441
    F_2442 = 2442
    F_2443 = 2443
    F_2444 = 2444
    F_2445 = 2445
    F_2446 = 2446
    F_2447 = 2447
    F_2448 = 2448
    F_2449 = 2449
    F_2450 = 2450
    F_2451 = 2451
    F_2452 = 2452
    F_2453 = 2453
    F_2454 = 2454
    F_2455 = 2455
    F_2456 = 2456
    F_2457 = 2457
    F_2458 = 2458
    F_2459 = 2459
    F_2460 = 2460
    F_2461 = 2461
    F_2462 = 2462
    F_2463 = 2463
    F_2464 = 2464
    F_2465 = 2465
    F_2466 = 2466
    F_2467 = 2467
    F_2468 = 2468
    F_2469 = 2469
    F_2470 = 2470
    F_2471 = 2471
    F_2472 = 2472
    F_2473 = 2473
    F_2474 = 2474
    F_2475 = 2475
    F_2476 = 2476
    F_2477 = 2477
    F_2478 = 2478
    F_2479 = 2479
    F_2480 = 2480
    F_5180 = 5180
    F_5190 = 5190
    F_5200 = 5200
    F_5210 = 5210
    F_5220 = 5220
    F_5230 = 5230
    F_5240 = 5240
    F_5250 = 5250
    F_5260 = 5260
    F_5270 = 5270
    F_5280 = 5280
    F_5290 = 5290
    F_5300 = 5300
    F_5310 = 5310
    F_5320 = 5320
    F_5500 = 5500
    F_5510 = 5510
    F_5520 = 5520
    F_5530 = 5530
    F_5540 = 5540
    F_5550 = 5550
    F_5560 = 5560
    F_5570 = 5570
    F_5580 = 5580
    F_5590 = 5590
    F_5600 = 5600
    F_5610 = 5610
    F_5620 = 5620
    F_5630 = 5630
    F_5640 = 5640
    F_5660 = 5660
    F_5670 = 5670
    F_5680 = 5680
    F_5690 = 5690
    F_5700 = 5700
    F_5710 = 5710
    F_5720 = 5720
    F_5745 = 5745
    F_5755 = 5755
    F_5765 = 5765
    F_5775 = 5775
    F_5785 = 5785
    F_5795 = 5795
    F_5805 = 5805
    F_5825 = 5825


class CHBandWidth(enum.Enum):
    BW5 = 5
    BW10 = 10
    BW20 = 20
    BW40 = 40
    BW80 = 80
    BW160 = 160


class MeasuredState(enum.Enum):
    PASS = 0
    FAIL = 1
    NOT_APPLICABLE = 2


class Technology(enum.Enum):
    BT = 0
    WIFI = 1


class HardwareMode(enum.Enum):
    VSA = 0
    VSG = 1


class HardwarePort(enum.Enum):
    RF1A = 0
    RF1B = 1
    RF2A = 2
    RF2B = 3
    RF3A = 4
    RF3B = 5
    RF4A = 6
    RF4B = 7


class SamplingRate(enum.Enum):
    MHZ_10 = 10
    MHZ_20 = 20
    MHZ_30 = 30.72
    MHZ_40 = 40
    MHZ_61 = 61.44
    MHZ_80 = 80
    MHZ_160 = 160
    MHZ_240 = 240


class WifiBandType(enum.Enum):
    G2_4 = '2G4'
    G5 = '5G'
    G4_9 = '4G9'


class WifiModulation(enum.Enum):
    OFDM = 0
    DSSS = 1


class WifiOFDMStandard(enum.Enum):
    A_P_N_AC_AX = 0
    A_P_N_AC = 1
    AF = 2
    AH = 3
    BA = 4


class WifiFreqCorrect(enum.Enum):
    LTF = 0
    STF = 1
    SIG = 2
    DATA = 3
    AUTO = 4


class WifiOFDMPacketFormat(enum.Enum):
    AUTO = 0
    NONH = 1
    MIX = 2
    GRE = 2
    VHT = 3
    TVHT = 4
    S1G1 = 5
    S1GS = 6
    S1GL = 7
    HESU = 8
    HEMU = 9
    HETR = 10
    HEEXTR = 11
    EHTMU = 12
    EHTTR = 13


class WifiOFDMAnalyMode(enum.Enum):
    MXN = 0
    COMP = 1
    SING = 2
    EVMS = 3


class WifiOFDMPowerClass(enum.Enum):
    A = 0
    B = 1
    C = 2
    D = 3


class SpectrumLimitType(enum.Enum):
    AUTO = 'AUTO'
    UNII4 = 'UNII4'
    P80 = '80P80'
    ETSI1 = 'ETSI1'
    AX11 = '11AX'
    AX11_P80 = '11AX_80P80'


class SpectrumLimitBW(enum.Enum):
    AUTO = 0
    CBW = 1


class EvmMethod(enum.Enum):
    RMS = 0
    STANDARD = 1
    STANDARD_1999 = 2
    STANDARD_2007 = 3
    STANDARD_2016 = 4


class EqualizerTaps(enum.Enum):
    OFF = 0
    TAP5 = 1
    TAP7 = 2
    TAP9 = 3


class MeasuredStatusCode(enum.Enum):
    RESULTS_CALCULATED_FROM_PARTIAL_DATA = 14
    RESULT_SIGNAL_ACQUISITION_OFF = 13
    RESULT_UNRELIABLE = 12
    RESULT_SIGNAL_INVALID = 11
    RESULT_CALC_LENGTH_EXCEED_ANA_LIMIT = 3
    RESULT_LIMIT_NA = 2
    RESULT_LIMIT_FAIL = 1
    RESULT_OK = 0
    RESULT_CALC_NOT_DEFINED = -1
    RESULT_CALC_OUT_OF_RANGE = -2
    RESULT_CALC_PENDING = -3
    RESULT_CAPTURE_NONE = -11
    RESULT_CAPTURE_TIMEOUT = -12
    RESULT_CAPTURE_INVALID = -13
    RESULT_ANALYSIS_FAILED = -21
    RESULT_SIGNAL_DIM_UNAVAILABLE = -31
    RESULT_STAT_RESULT_LEN_INCONSISTENT = -32
    RESULT_UNAVAILABLE = -33
    RESULT_STAT_SIGNAL_INCONSISTENT = -34
    RESULT_ANALYSIS_CFG_INVALID = -41
    RESULT_ANALYSIS_ERR = -111
    RESULT_OUT_OF_MEMORY = -225


class TestDeviceError(Exception):
    pass


class Utils(object):
    """
    常用工具类
    """
    @staticmethod
    def floatEquals(a, b, uncertainty=0.0, epsilon=None):
        a = float(a)
        b = float(b)
        uncertainty = float(uncertainty)
        epsilon = (sys.float_info.epsilon * 1e3) if epsilon is None else epsilon
        delta_AB = abs(a - b)

        if a == b:
            return True
        elif uncertainty == 0:
            return delta_AB < sys.float_info.epsilon
        else:
            if delta_AB < uncertainty:
                return True
            else:
                delta_deltaAB_uncertainty = abs(delta_AB - uncertainty)

                if delta_AB == uncertainty:
                    return True
                elif delta_AB == 0 or uncertainty == 0 or delta_deltaAB_uncertainty < sys.float_info.min:
                    return delta_deltaAB_uncertainty < (epsilon * sys.float_info.min)
                else:
                    return (delta_deltaAB_uncertainty / min(delta_AB + uncertainty, sys.float_info.max)) < epsilon

    @staticmethod
    def to_enum(name, enumClass):

        if not issubclass(enumClass, enum.Enum):
            raise ValueError('Class {:s} is not a subclass of {:s}'.format(enumClass.__name__, enum.Enum.__name__))

        if issubclass(name.__class__, enum.Enum) and name.__class__ == enumClass:
            return name
        else:
            try:
                enumClass = enumClass[name]
            except KeyError:
                pass
            else:
                return enumClass

            try:
                enumClass = enumClass(name)
            except ValueError:
                raise ValueError(
                    'Enum class {:s} does not have an item with name or value {}'.format(enumClass.__name__, name))
            else:
                return enumClass

    @staticmethod
    def scientific_to_float(strNum):
        if 'e' in strNum:
            e = float(strNum.split('e')[0])
            sign = strNum.split('e')[1][:1]
            result_e = int(strNum.split('e')[1][1:])

            if sign == '+':
                floatNum = e * math.pow(10, result_e)
            elif sign == '-':
                floatNum = e * math.pow(10, -result_e)
            else:
                floatNum = None
                raise ValueError('error: unknown sign :{:s}'.format(sign))
        else:
            floatNum = float(strNum)

        return floatNum

    @staticmethod
    def is_truthy(item):
        """Returns `True` or `False` depending is the item considered true or not.

        Validation rules:

        - If the value is a string, it is considered false if it is `'FALSE'`,
          `'NO'`, `'OFF'`, `'0'`, `'NONE'` or `''`, case-insensitively.
          Considering `'NONE'` false is new in RF 3.0.3 and considering `'OFF'`
          and `'0'` false is new in RF 3.1.
        - Other strings are considered true.
        - Other values are handled by using the standard `bool()` function.

        Designed to be used also by external test libraries that want to handle
        Boolean values similarly as Robot Framework itself. See also
        :func:`is_falsy`.
        """
        #if isinstance(item, (str, unicode)):
        #    return item.upper() not in FALSE_STRINGS
        return bool(item)


class _LitePointKeywords(object):
    """
    控制IQ的主体函数
    """
    _socket = None
    _locked = False
    _ip = '192.168.100.254'
    _port = 24000

    def __init__(self, *args):
        super().__init__(*args)

        self._WLANChFreqMapping = {
            MEASChannel.CH1: MEASCenterFreq.F_2412,
            MEASChannel.CH2: MEASCenterFreq.F_2417,
            MEASChannel.CH3: MEASCenterFreq.F_2422,
            MEASChannel.CH4: MEASCenterFreq.F_2427,
            MEASChannel.CH5: MEASCenterFreq.F_2432,
            MEASChannel.CH6: MEASCenterFreq.F_2437,
            MEASChannel.CH7: MEASCenterFreq.F_2442,
            MEASChannel.CH8: MEASCenterFreq.F_2447,
            MEASChannel.CH9: MEASCenterFreq.F_2452,
            MEASChannel.CH10: MEASCenterFreq.F_2457,
            MEASChannel.CH11: MEASCenterFreq.F_2462,
            MEASChannel.CH12: MEASCenterFreq.F_2467,
            MEASChannel.CH13: MEASCenterFreq.F_2472,
            MEASChannel.CH36: MEASCenterFreq.F_5180,
            MEASChannel.CH38: MEASCenterFreq.F_5190,
            MEASChannel.CH40: MEASCenterFreq.F_5200,
            MEASChannel.CH42: MEASCenterFreq.F_5210,
            MEASChannel.CH44: MEASCenterFreq.F_5220,
            MEASChannel.CH46: MEASCenterFreq.F_5230,
            MEASChannel.CH48: MEASCenterFreq.F_5240,
            MEASChannel.CH50: MEASCenterFreq.F_5250,
            MEASChannel.CH52: MEASCenterFreq.F_5260,
            MEASChannel.CH54: MEASCenterFreq.F_5270,
            MEASChannel.CH56: MEASCenterFreq.F_5280,
            MEASChannel.CH58: MEASCenterFreq.F_5290,
            MEASChannel.CH60: MEASCenterFreq.F_5300,
            MEASChannel.CH62: MEASCenterFreq.F_5310,
            MEASChannel.CH64: MEASCenterFreq.F_5320,
            MEASChannel.CH100: MEASCenterFreq.F_5500,
            MEASChannel.CH102: MEASCenterFreq.F_5510,
            MEASChannel.CH104: MEASCenterFreq.F_5520,
            MEASChannel.CH106: MEASCenterFreq.F_5530,
            MEASChannel.CH108: MEASCenterFreq.F_5540,
            MEASChannel.CH110: MEASCenterFreq.F_5550,
            MEASChannel.CH112: MEASCenterFreq.F_5560,
            MEASChannel.CH114: MEASCenterFreq.F_5570,
            MEASChannel.CH116: MEASCenterFreq.F_5580,
            MEASChannel.CH118: MEASCenterFreq.F_5590,
            MEASChannel.CH120: MEASCenterFreq.F_5600,
            MEASChannel.CH122: MEASCenterFreq.F_5610,
            MEASChannel.CH124: MEASCenterFreq.F_5620,
            MEASChannel.CH126: MEASCenterFreq.F_5630,
            MEASChannel.CH128: MEASCenterFreq.F_5640,
            MEASChannel.CH132: MEASCenterFreq.F_5660,
            MEASChannel.CH134: MEASCenterFreq.F_5670,
            MEASChannel.CH136: MEASCenterFreq.F_5680,
            MEASChannel.CH138: MEASCenterFreq.F_5690,
            MEASChannel.CH140: MEASCenterFreq.F_5700,
            MEASChannel.CH142: MEASCenterFreq.F_5710,
            MEASChannel.CH144: MEASCenterFreq.F_5720,
            MEASChannel.CH149: MEASCenterFreq.F_5745,
            MEASChannel.CH151: MEASCenterFreq.F_5755,
            MEASChannel.CH153: MEASCenterFreq.F_5765,
            MEASChannel.CH155: MEASCenterFreq.F_5775,
            MEASChannel.CH157: MEASCenterFreq.F_5785,
            MEASChannel.CH159: MEASCenterFreq.F_5795,
            MEASChannel.CH161: MEASCenterFreq.F_5805,
            MEASChannel.CH165: MEASCenterFreq.F_5825,
        }

        self._BRChFreqMapping = {
            MEASChannel.CH0: MEASCenterFreq.F_2402,
            MEASChannel.CH1: MEASCenterFreq.F_2403,
            MEASChannel.CH2: MEASCenterFreq.F_2404,
            MEASChannel.CH3: MEASCenterFreq.F_2405,
            MEASChannel.CH4: MEASCenterFreq.F_2406,
            MEASChannel.CH5: MEASCenterFreq.F_2407,
            MEASChannel.CH6: MEASCenterFreq.F_2408,
            MEASChannel.CH7: MEASCenterFreq.F_2409,
            MEASChannel.CH8: MEASCenterFreq.F_2410,
            MEASChannel.CH9: MEASCenterFreq.F_2411,
            MEASChannel.CH10: MEASCenterFreq.F_2412,
            MEASChannel.CH11: MEASCenterFreq.F_2413,
            MEASChannel.CH12: MEASCenterFreq.F_2414,
            MEASChannel.CH13: MEASCenterFreq.F_2415,
            MEASChannel.CH14: MEASCenterFreq.F_2416,
            MEASChannel.CH15: MEASCenterFreq.F_2417,
            MEASChannel.CH16: MEASCenterFreq.F_2418,
            MEASChannel.CH17: MEASCenterFreq.F_2419,
            MEASChannel.CH18: MEASCenterFreq.F_2420,
            MEASChannel.CH19: MEASCenterFreq.F_2421,
            MEASChannel.CH20: MEASCenterFreq.F_2422,
            MEASChannel.CH21: MEASCenterFreq.F_2423,
            MEASChannel.CH22: MEASCenterFreq.F_2424,
            MEASChannel.CH23: MEASCenterFreq.F_2425,
            MEASChannel.CH24: MEASCenterFreq.F_2426,
            MEASChannel.CH25: MEASCenterFreq.F_2427,
            MEASChannel.CH26: MEASCenterFreq.F_2428,
            MEASChannel.CH27: MEASCenterFreq.F_2429,
            MEASChannel.CH28: MEASCenterFreq.F_2430,
            MEASChannel.CH29: MEASCenterFreq.F_2431,
            MEASChannel.CH30: MEASCenterFreq.F_2432,
            MEASChannel.CH31: MEASCenterFreq.F_2433,
            MEASChannel.CH32: MEASCenterFreq.F_2434,
            MEASChannel.CH33: MEASCenterFreq.F_2435,
            MEASChannel.CH34: MEASCenterFreq.F_2436,
            MEASChannel.CH35: MEASCenterFreq.F_2437,
            MEASChannel.CH36: MEASCenterFreq.F_2438,
            MEASChannel.CH37: MEASCenterFreq.F_2439,
            MEASChannel.CH38: MEASCenterFreq.F_2440,
            MEASChannel.CH39: MEASCenterFreq.F_2441,
            MEASChannel.CH40: MEASCenterFreq.F_2442,
            MEASChannel.CH41: MEASCenterFreq.F_2443,
            MEASChannel.CH42: MEASCenterFreq.F_2444,
            MEASChannel.CH43: MEASCenterFreq.F_2445,
            MEASChannel.CH44: MEASCenterFreq.F_2446,
            MEASChannel.CH45: MEASCenterFreq.F_2447,
            MEASChannel.CH46: MEASCenterFreq.F_2448,
            MEASChannel.CH47: MEASCenterFreq.F_2449,
            MEASChannel.CH48: MEASCenterFreq.F_2450,
            MEASChannel.CH49: MEASCenterFreq.F_2451,
            MEASChannel.CH50: MEASCenterFreq.F_2452,
            MEASChannel.CH51: MEASCenterFreq.F_2453,
            MEASChannel.CH52: MEASCenterFreq.F_2454,
            MEASChannel.CH53: MEASCenterFreq.F_2455,
            MEASChannel.CH54: MEASCenterFreq.F_2456,
            MEASChannel.CH55: MEASCenterFreq.F_2457,
            MEASChannel.CH56: MEASCenterFreq.F_2458,
            MEASChannel.CH57: MEASCenterFreq.F_2459,
            MEASChannel.CH58: MEASCenterFreq.F_2460,
            MEASChannel.CH59: MEASCenterFreq.F_2461,
            MEASChannel.CH60: MEASCenterFreq.F_2462,
            MEASChannel.CH61: MEASCenterFreq.F_2463,
            MEASChannel.CH62: MEASCenterFreq.F_2464,
            MEASChannel.CH63: MEASCenterFreq.F_2465,
            MEASChannel.CH64: MEASCenterFreq.F_2466,
            MEASChannel.CH65: MEASCenterFreq.F_2467,
            MEASChannel.CH66: MEASCenterFreq.F_2468,
            MEASChannel.CH67: MEASCenterFreq.F_2469,
            MEASChannel.CH68: MEASCenterFreq.F_2470,
            MEASChannel.CH69: MEASCenterFreq.F_2471,
            MEASChannel.CH70: MEASCenterFreq.F_2472,
            MEASChannel.CH71: MEASCenterFreq.F_2473,
            MEASChannel.CH72: MEASCenterFreq.F_2474,
            MEASChannel.CH73: MEASCenterFreq.F_2475,
            MEASChannel.CH74: MEASCenterFreq.F_2476,
            MEASChannel.CH75: MEASCenterFreq.F_2477,
            MEASChannel.CH76: MEASCenterFreq.F_2478,
            MEASChannel.CH77: MEASCenterFreq.F_2479,
            MEASChannel.CH78: MEASCenterFreq.F_2480,
        }

        self._LEChFreqMapping = {
            MEASChannel.CH0: MEASCenterFreq.F_2402,
            MEASChannel.CH1: MEASCenterFreq.F_2404,
            MEASChannel.CH2: MEASCenterFreq.F_2406,
            MEASChannel.CH3: MEASCenterFreq.F_2408,
            MEASChannel.CH4: MEASCenterFreq.F_2410,
            MEASChannel.CH5: MEASCenterFreq.F_2412,
            MEASChannel.CH6: MEASCenterFreq.F_2414,
            MEASChannel.CH7: MEASCenterFreq.F_2416,
            MEASChannel.CH8: MEASCenterFreq.F_2418,
            MEASChannel.CH9: MEASCenterFreq.F_2420,
            MEASChannel.CH10: MEASCenterFreq.F_2422,
            MEASChannel.CH11: MEASCenterFreq.F_2424,
            MEASChannel.CH12: MEASCenterFreq.F_2426,
            MEASChannel.CH13: MEASCenterFreq.F_2428,
            MEASChannel.CH14: MEASCenterFreq.F_2430,
            MEASChannel.CH15: MEASCenterFreq.F_2432,
            MEASChannel.CH16: MEASCenterFreq.F_2434,
            MEASChannel.CH17: MEASCenterFreq.F_2436,
            MEASChannel.CH18: MEASCenterFreq.F_2438,
            MEASChannel.CH19: MEASCenterFreq.F_2440,
            MEASChannel.CH20: MEASCenterFreq.F_2442,
            MEASChannel.CH21: MEASCenterFreq.F_2444,
            MEASChannel.CH22: MEASCenterFreq.F_2446,
            MEASChannel.CH23: MEASCenterFreq.F_2448,
            MEASChannel.CH24: MEASCenterFreq.F_2450,
            MEASChannel.CH25: MEASCenterFreq.F_2452,
            MEASChannel.CH26: MEASCenterFreq.F_2454,
            MEASChannel.CH27: MEASCenterFreq.F_2456,
            MEASChannel.CH28: MEASCenterFreq.F_2458,
            MEASChannel.CH29: MEASCenterFreq.F_2460,
            MEASChannel.CH30: MEASCenterFreq.F_2462,
            MEASChannel.CH31: MEASCenterFreq.F_2464,
            MEASChannel.CH32: MEASCenterFreq.F_2466,
            MEASChannel.CH33: MEASCenterFreq.F_2468,
            MEASChannel.CH34: MEASCenterFreq.F_2470,
            MEASChannel.CH35: MEASCenterFreq.F_2472,
            MEASChannel.CH36: MEASCenterFreq.F_2474,
            MEASChannel.CH37: MEASCenterFreq.F_2476,
            MEASChannel.CH38: MEASCenterFreq.F_2478,
            MEASChannel.CH39: MEASCenterFreq.F_2480,
        }

    # region LitePoint Connection

    def open_lite_point_connection(self, ipAddress, port=None, timeout=0.2):
        """与IQ仪表建立连接"""
        print(pyvisa_py.common.int_to_byte(12))
        self.pyvisa_rm = pyvisa.ResourceManager('@py')
        self.pyvisa_inst = self.pyvisa_rm.open_resource('TCPIP::192.168.100.254::hislip0::INSTR')
        self.pyvisa_inst.timeout = timeout*1000


    def close_lite_point_connection(self):
        """与IQ仪表断开连接"""
        self.pyvisa_inst.close()

    def send_raw_command(self, cmd):
        """向IQ仪表发送SCPI指令"""
        if '?' in cmd:
            return self.pyvisa_inst.query(cmd)
        else:
            return self.pyvisa_inst.write(cmd)

    # endregion

    # region Port Configuration
    def config_port_routing(self, routIndex=None, portName=None, sigMode=None):
        routIndex = int(routIndex) if routIndex is not None else routIndex
        portName = Utils.to_enum(portName, HardwarePort) if portName is not None else portName
        sigMode = Utils.to_enum(sigMode, HardwareMode) if sigMode is not None else sigMode

        params = []

        if routIndex:
            params.append('ROUT{}'.format(routIndex))

        if all([portName, sigMode]):
            params.append('PORT:RES {},{}'.format(portName.name, sigMode.name))

        if len(params) >= 1:
            self.send_raw_command('{:s}'.format(';'.join(params)))
        else:
            print('No command sent, no parameter was set')

    # endregion

    # region VSA Configuration
    def config_vsa_hardware_settings(self, freq=None, referLevel=None, enableAGC=None, interval=None, samRate=None,
                                     capLength=None):
        """
        This function can be used for WiFi SISO and Bluetooth hardware VSA Settings.
        """

        freq = int(freq) if freq is not None else freq
        referLevel = int(referLevel) if referLevel is not None else referLevel
        enableAGC = Utils.is_truthy(enableAGC) if enableAGC is not None else enableAGC
        interval = int(interval) if interval is not None else 5
        samRate = Utils.to_enum(samRate, SamplingRate) if samRate is not None else samRate
        capLength = int(capLength) if capLength is not None else capLength

        vsaParams = []

        if freq is not None:
            vsaParams.append('FREQ {}'.format(freq * 1000000))

        if enableAGC is not None:
            vsaParams.append('RLEV:AUTO')
        else:
            if referLevel:
                vsaParams.append('RLEV {}'.format(referLevel))

        if samRate is not None:
            vsaParams.append('SRAT {}'.format(samRate.value * 1000000))

        if capLength is not None:
            vsaParams.append('CAPT:TIME {}'.format(capLength / 1000))

        if len(vsaParams) >= 1:
            self.send_raw_command('VSA1;{:s}'.format(';'.join(vsaParams)))
        else:
            print('No command sent, no parameter was set')

    def config_vsa_technology_settings(self, bandType=None, channel=None, userMargin=None, expectedPNom=None,
                                       bandwidth=None, technology=Technology.WIFI):
        """
        This function can be used for WiFi SISO and Bluetooth technology VSA Settings.
        """

        bandType = Utils.to_enum(bandType, WifiBandType) if bandType is not None else bandType
        channel = Utils.to_enum(channel, MEASChannel) if channel is not None else channel
        userMargin = int(userMargin) if userMargin is not None else userMargin
        expectedPNom = int(expectedPNom) if expectedPNom is not None else expectedPNom
        bandwidth = Utils.to_enum(bandwidth, CHBandWidth) if bandwidth is not None else bandwidth
        technology = Utils.to_enum(technology, Technology) if technology is not None else technology

        params = []

        if bandType is not None:
            params.append('CONF:BAND {:s}'.format(bandType.value))
        if channel is not None:
            if technology == Technology.WIFI:
                params.append('CONF:CHAN:IND {:d}'.format(channel.value))
            else:
                params.append('CONF:CHAN {:d}'.format(channel.value))
        if userMargin is not None:
            if technology == Technology.WIFI:
                modulationType = self.get_vsa_configured_modulation_type()
                params.append('CONF:UMAR:{:s} {:d}'.format(modulationType.name, userMargin))
            else:
                params.append('CONF:UMAR {:d}'.format(userMargin))
        if expectedPNom is not None:
            params.append('CONF:ENP {:d}'.format(expectedPNom))
        if bandwidth is not None:
            params.append('CONF:CHAN:CBW {}'.format(bandwidth.value * 1000000))

        if len(params) >= 1:
            self.send_raw_command('{:s};{:s}'.format(technology.name, ';'.join(params)))
        else:
            print('No command sent, no parameter was set')

        self.send_raw_command('{:s};HSET:ALL VSA1'.format(technology.name))

    def config_vsa_common_settings(self, standardFamily=None, analySignal=None, powerDetection=None,
                                   txQualityRate=None):
        standardFamily = Utils.to_enum(standardFamily, WifiModulation) if standardFamily is not None else standardFamily
        analySignal = int(analySignal) if analySignal is not None else analySignal
        powerDetection = str(powerDetection) if powerDetection is not None else powerDetection
        txQualityRate = int(txQualityRate) if txQualityRate is not None else txQualityRate

        commParams = []

        if standardFamily:
            commParams.append('CONF:STAN {}'.format(standardFamily.name))
        if analySignal:
            commParams.append('CONF:TXQ:ASIG {}'.format(analySignal))
        if powerDetection:
            commParams.append('CONF:PDET:SIGN {}'.format(powerDetection))
        if txQualityRate:
            commParams.append('CONF:TXQ:CLOC {}'.format(txQualityRate))

        if len(commParams) >= 1:
            self.send_raw_command('WIFI;{:s}'.format(';'.join(commParams)))
        else:
            print('No command sent, no parameter was set')

    def config_vsa_ofdm_settings(self, standard=None, freqCorrect=None, phaseCorrect=None, ampCorrect=None,
                                 symCorrect=None, channelEst=None, packetFormat=None, freqSeg=None, useAllSig=None,
                                 analyMode=None, powerClass=None, symbolTimeAdj=None, specLimitType=None,
                                 specLimitBW=None, enablePreAVG=None):
        standard = Utils.to_enum(standard, WifiOFDMStandard) if standard is not None else standard
        freqCorrect = Utils.to_enum(freqCorrect, WifiFreqCorrect) if freqCorrect is not None else freqCorrect
        phaseCorrect = Utils.is_truthy(phaseCorrect) if phaseCorrect is not None else phaseCorrect
        ampCorrect = Utils.is_truthy(ampCorrect) if ampCorrect is not None else ampCorrect
        symCorrect = Utils.is_truthy(symCorrect) if symCorrect is not None else symCorrect
        channelEst = Utils.to_enum(channelEst, WifiFreqCorrect) if channelEst is not None else channelEst
        packetFormat = Utils.to_enum(packetFormat, WifiOFDMPacketFormat) if packetFormat is not None else packetFormat
        freqSeg = int(freqSeg) if freqSeg is not None else freqSeg
        useAllSig = Utils.is_truthy(useAllSig) if useAllSig is not None else useAllSig
        analyMode = Utils.to_enum(analyMode, WifiOFDMAnalyMode) if analyMode is not None else analyMode
        powerClass = Utils.to_enum(powerClass, WifiOFDMPowerClass) if powerClass is not None else powerClass
        symbolTimeAdj = float(symbolTimeAdj) if symbolTimeAdj is not None else symbolTimeAdj
        specLimitType = Utils.to_enum(specLimitType, SpectrumLimitType) if specLimitType is not None else specLimitType
        specLimitBW = Utils.to_enum(specLimitBW, SpectrumLimitBW) if specLimitBW is not None else specLimitBW
        enablePreAVG = Utils.is_truthy(enablePreAVG) if enablePreAVG is not None else enablePreAVG

        params = []

        if standard:
            params.append('CONF:STAN:OFDM {}'.format(standard.name))
        if freqCorrect:
            params.append('CONF:OFDM:TRAC:FREQ {}'.format(freqCorrect.name))
        if phaseCorrect:
            params.append('CONF:OFDM:TRAC:PHAS {}'.format(int(phaseCorrect)))
        if ampCorrect:
            params.append('CONF:OFDM:TRAC:AMP {}'.format(int(ampCorrect)))
        if symCorrect:
            params.append('CONF:OFDM:TRAC:SCL {}'.format(int(symCorrect)))
        if channelEst:
            params.append('CONF:OFDM:CEST {}'.format(channelEst.name))
        if packetFormat:
            params.append('CONF:OFDM:PFOR {}'.format(packetFormat.name))
        if freqSeg:
            params.append('CONF:AFS {}'.format(freqSeg))
        if useAllSig:
            params.append('CONF:OFDM:UAS {}'.format(int(useAllSig)))
        if analyMode:
            params.append('COND:OFDM:MIMO {}'.format(analyMode.name))
        if powerClass:
            params.append('CONF:POW:CLAS {}'.format(powerClass.name))
        if symbolTimeAdj:
            params.append('CONF:OFDM:STAD {:f}'.format(symbolTimeAdj))
        if specLimitType:
            params.append('CONF:SPEC:HLIM:TYPE {}'.format(specLimitType.value))
        if specLimitBW:
            params.append('CONF:SPEC:HLIM {}'.format(specLimitBW.name))
        if enablePreAVG:
            params.append('CONF:OFDM:CEST:SMO {}'.format(int(enablePreAVG)))

        if len(params) >= 1:
            self.send_raw_command('WIFI;{:s}'.format(';'.join(params)))
        else:
            print('No command sent, no parameter was set')

    def config_vsa_dsss_settings(self, evmMethod=None, equalTaps=None, dcRemoval=None):
        evmMethod = Utils.to_enum(evmMethod, EvmMethod) if evmMethod is not None else evmMethod
        equalTaps = Utils.to_enum(equalTaps, EqualizerTaps) if equalTaps is not None else equalTaps
        dcRemoval = Utils.is_truthy(dcRemoval) if dcRemoval is not None else dcRemoval

        modulationType = self.get_vsa_configured_modulation_type()

        if modulationType is not WifiModulation.DSSS:
            raise TestDeviceError('Pls ensure standard family is DSSS')

        dsssParams = []

        if evmMethod:
            dsssParams.append('CONF:DSSS:EVM:METH {}'.format(evmMethod.name))
        if equalTaps:
            dsssParams.append('CONF:DSSS:ETAP {}'.format(equalTaps.name))
        if dcRemoval:
            dsssParams.append('CONF:DSSS:EVM:DCR {}'.format(int(dcRemoval)))

        if len(dsssParams) >= 1:
            self.send_raw_command('WIFI;{:s}'.format(';'.join(dsssParams)))
        else:
            print('No command sent, no parameter was set')

    def get_vsa_configured_channel(self):
        """
        This function is used for query wifi channel.
        """
        index = self.send_raw_command('WIFI;CONF:CHAN:IND?')

        return Utils.to_enum(int(index), MEASChannel)

    def get_vsa_configured_modulation_type(self):
        """
        This function is used for query wifi modulation type.
        """
        modulation = self.send_raw_command('WIFI;CONF:STAN?').strip()

        return Utils.to_enum(modulation, WifiModulation)

    def tx_test_pre_configuration(self, **kwargs):
        """
        For WIFI & BT VSA test
        给仪表中插入Cable Loss数据
        """
        try:
            loss2G_start = kwargs[MEASCenterFreq.F_2412.name]
            loss2G_end = kwargs[MEASCenterFreq.F_2472.name]
            loss5G_start = kwargs[MEASCenterFreq.F_5180.name]
            loss5G_end = kwargs[MEASCenterFreq.F_5825.name]
        except KeyError:
            print('Make sure &{PathLoss} contains: F_2412, F_2472, F_5180, F_5825')
            raise AssertionError('Make sure &{PathLoss} contains: F_2412, F_2472, F_5180, F_5825')

        self.send_raw_command('ROUT1;PORT:RES RF1A,VSA')
        self.send_raw_command(
            'MEM:TABL:LOSS:DEL:ALL;TABLE "MyLoss";TABLE:DEFINE "FREQ,LOSS";TABLE:INS:POIN {:d}MHz,{:.2f},{:d}MHz,{:.2f},{:d}MHz,{:.2f},{:d}MHz,{:.2f};TABL:STOR;VSA1;RFC:USE "MyLoss",RF1A;RFC:STAT ON,RF1A'.format(
                MEASCenterFreq.F_2412.value, float(loss2G_start), MEASCenterFreq.F_2472.value, float(loss2G_end),
                MEASCenterFreq.F_5180.value, float(loss5G_start), MEASCenterFreq.F_5825.value, float(loss5G_end)))

    def wifi_tx_measurement_configuration(self, modulationType, channel, bandwidth):
        """
        设置仪表的调制方式OFDM/DSSS， 信道， 带宽
        """
        modulationType = Utils.to_enum(modulationType, WifiModulation)
        channel = Utils.to_enum(channel, MEASChannel)
        bandwidth = Utils.to_enum(bandwidth, CHBandWidth)

        bandType = WifiBandType.G2_4 if 1 <= channel.value <= 13 else WifiBandType.G5

        self.send_raw_command('WIFI;CONF:OFDM:CEST DATA;CONF:STAN {:s}'.format(modulationType.name))

        if bandwidth == CHBandWidth.BW80:
            self.send_raw_command(
                'WIFI;CONF:BAND {:s};CONF:CHAN:IND {:d};HSET:ALL VSA1;VSA1;RLEV:AUTO;SRAT {};CAPT:TIME 0.009;INIT:SPEC:WIDE'.format(
                    bandType.value, channel.value, SamplingRate.MHZ_160.value * 1000000))
        else:
            self.send_raw_command(
                'WIFI;CONF:BAND {:s};CONF:CHAN:IND {:d};HSET:ALL VSA1;VSA1;RLEV:AUTO;SRAT {};CAPT:TIME 0.009;INIT'.format(
                    bandType.value, channel.value, SamplingRate.MHZ_240.value * 1000000))

    def bt_tx_measurement_configuration(self, channel, samRate, capLength, standard=None):
        """
        测量BT功能使用， 设置信道， 采样率， 采样长度
        """
        channel = Utils.to_enum(channel, MEASChannel)
        samRate = Utils.to_enum(samRate, SamplingRate)
        capLength = int(capLength)
        standard = Utils.to_enum(standard, BtStandard) if standard is not None else standard

        if standard == BtStandard.BLE:
            freq = self._LEChFreqMapping[channel]
        else:
            freq = self._BRChFreqMapping[channel]

        self.send_raw_command('BT;VSA1;FREQ {:d};RLEV:AUTO;SRAT {:d};CAPT:TIME {};INIT'.format(freq.value * 1000000,
                                                                                               samRate.value * 1000000,
                                                                                               capLength / 1000))

    # endregion

    # region VSG Configuration
    def config_vsg_hardware_settings(self, freq=None, powerLevel=None, samRate=None):
        """
        This function can be used for WiFi SISO and Bluetooth hardware VSG Settings.
        """
        freq = int(freq) if freq is not None else freq
        powerLevel = float(powerLevel) if powerLevel is not None else powerLevel
        samRate = Utils.to_enum(samRate, SamplingRate) if samRate is not None else samRate

        vsgParams = []

        if freq is not None:
            vsgParams.append('FREQ {}'.format(freq * 1000000))
        if powerLevel is not None:
            vsgParams.append('POW {:.2f}'.format(powerLevel))
        if samRate is not None:
            vsgParams.append('SRAT {}'.format(samRate.value * 1000000))

        if len(vsgParams) >= 1:
            self.send_raw_command('VSG;{:s}'.format(';'.join(vsgParams)))
        else:
            print('No command sent, no parameter was set')

        print('Power level is: {:.2f}'.format(powerLevel))

    def config_vsg_waveforms_settings(self, fileName=None, count=None, enableModulation=None, enableOutput=None):
        """
        This function can be used for WiFi SISO and Bluetooth hardware waveforms Settings.
        """

        fileName = str(fileName) if fileName is not None else fileName
        count = int(count) if count is not None else count
        enableModulation = Utils.is_truthy(enableModulation) if enableModulation is not None else enableModulation
        enableOutput = Utils.is_truthy(enableOutput) if enableOutput is not None else enableOutput

        waveParams = []

        if fileName is not None:
            waveParams.append('WAVE:LOAD "{:s}"'.format(fileName))

        if count is not None:
            waveParams.append('WLIS:COUNT {:d}'.format(count))

        if enableModulation is not None:
            waveParams.append('MOD:STAT {:d}'.format(int(enableModulation)))

        if enableOutput is not None:
            waveParams.append('POW:STAT {:d}'.format(int(enableOutput)))

        if len(waveParams) >= 1:
            self.send_raw_command('VSG1;{:s}'.format(';'.join(waveParams)))
        else:
            print('No command sent, no parameter was set')

    def config_vsg_technology_settings(self, bandType=None, channel=None, bandwidth=None, expectedPNom=None,
                                       userMargin=None, technology=Technology.WIFI):
        """
        This function can be used for WiFi SISO and Bluetooth technology VSG Settings.
        """

        bandType = Utils.to_enum(bandType, WifiBandType) if bandType is not None else bandType
        channel = Utils.to_enum(channel, MEASChannel) if channel is not None else channel
        bandwidth = Utils.to_enum(bandwidth, CHBandWidth) if bandwidth is not None else bandwidth
        expectedPNom = int(expectedPNom) if expectedPNom is not None else expectedPNom
        userMargin = int(userMargin) if userMargin is not None else userMargin
        technology = Utils.to_enum(technology, Technology) if technology is not None else technology

        vsgParams = []

        if bandType is not None:
            vsgParams.append('CONF:BAND {}'.format(bandType.value))
        if channel is not None:
            vsgParams.append('CONF:CHAN:IND {}'.format(channel.value))
        if bandwidth is not None:
            vsgParams.append('CONF:CHAN:CBW {}'.format(bandwidth.value * 1000000))
        if expectedPNom is not None:
            vsgParams.append('CONF:ENP {:d}'.format(expectedPNom))
        if userMargin is not None:
            vsgParams.append('CONF:UMAR {:d}'.format(userMargin))

        if len(vsgParams) >= 1:
            self.send_raw_command('{:s};{:s}'.format(technology.name, ';'.join(vsgParams)))
            self.send_raw_command('{:s};HSET:ALL VSG1'.format(technology.name))
        else:
            print('No command sent, no parameter was set')

    def activate_vsg_waveform_output(self):
        loaded = self.send_raw_command('VSG;WAVE:LOAD?')

        if loaded:
            self.send_raw_command('VSG1;WAVE:EXEC ON')
        else:
            raise AssertionError('Pls load waveform file first.')

    def deactivate_vsg_waveform_output(self):
        self.send_raw_command('VSG1;WAVE:EXEC OFF')

    def rx_test_pre_configuration(self, **kwargs):
        """
        For WIFI & BT VSG test
        """
        try:
            loss2G_start = kwargs[MEASCenterFreq.F_2412.name]
            loss2G_end = kwargs[MEASCenterFreq.F_2472.name]
            loss5G_start = kwargs[MEASCenterFreq.F_5180.name]
            loss5G_end = kwargs[MEASCenterFreq.F_5825.name]
        except KeyError:
            print('Make sure &{PathLoss} contains: F_2412, F_2472, F_5180, F_5825')
            raise AssertionError('Make sure &{PathLoss} contains: F_2412, F_2472, F_5180, F_5825')

        self.send_raw_command('ROUT1;PORT:RES RF1A,VSG')
        self.send_raw_command(
            'MEM:TABL:LOSS:DEL:ALL;TABLE "MyLoss";TABLE:DEFINE "FREQ,LOSS";TABLE:INS:POIN {:d}MHz,{:.2f},{:d}MHz,{:.2f},{:d}MHz,{:.2f},{:d}MHz,{:.2f};TABL:STOR;VSG1;RFC:USE "MyLoss",RF1A;RFC:STAT ON,RF1A'.format(
                MEASCenterFreq.F_2412.value, float(loss2G_start), MEASCenterFreq.F_2472.value, float(loss2G_end),
                MEASCenterFreq.F_5180.value, float(loss5G_start), MEASCenterFreq.F_5825.value, float(loss5G_end)))

    def wifi_rx_measurement_configuration(self, channel, fileName):
        """
        WIFI的接收测试， 设置信道，波形文件
        """
        channel = Utils.to_enum(channel, MEASChannel)
        fileName = str(fileName)

        freq = self._WLANChFreqMapping[channel]

        self.send_raw_command(
            'VSG1;WAVE:EXEC OFF;FREQ {:d};WAVE:LOAD "{:s}";WLIST:WSEG1:DATA "{:s}";WLIST:WSEG1:SAVE;WLIST:COUNT:ENABLE WSEG1;WLIS:COUN 1500;SRAT 80000000'.format(
                freq.value * 1000000, fileName, fileName))

    def bt_rx_measurement_configuration(self, channel, fileName):
        """
        This function is applicable to BR/EDR
        蓝牙接收测试，设置信道，波形文件
        """
        channel = Utils.to_enum(channel, MEASChannel)
        fileName = str(fileName)

        freq = self._BRChFreqMapping[channel]

        self.send_raw_command(
            'VSG1;WAVE:EXEC OFF;FREQ {:d};WAVE:LOAD "{:s}";WLIST:WSEG1:DATA "{:s}";WLIST:WSEG1:SAVE;WLIST:COUNT:ENABLE WSEG1;SRAT 80000000'.format(
                freq.value * 1000000, fileName, fileName))

    def le_rx_measurement_configuration(self, channel, fileName):
        """
        This function is applicable to BLE
        """
        channel = Utils.to_enum(channel, MEASChannel)
        fileName = str(fileName)
        freq = self._LEChFreqMapping[channel]

        self.send_raw_command(
            'VSG1;WAVE:EXEC OFF;FREQ {:d};WAVE:LOAD "{:s}";WLIST:WSEG1:DATA "{:s}";WLIST:WSEG1:SAVE;WLIST:COUNT:ENABLE WSEG1;WLIS:COUN 1500;SRAT 80000000'.format(
                freq.value * 1000000, fileName, fileName))

    # endregion

    # region WIFI Measurement
    def _check_status_code(self, status):
        status = Utils.to_enum(int(status), MeasuredStatusCode)

        if status.value != 0:
            raise AssertionError('Measured results were error :{:s}'.format(status.name))

    def initialize_measurement(self, packetNum=2):
        packetNum = int(packetNum)
        try:
            self.send_raw_command(
                'VSA1;INIT;WIFI;CALC:POW 0,{:d};CALC:TXQ 0,{:d};CALC:SPEC 0,{:d}'.format(packetNum, packetNum,
                                                                                         packetNum))
        except Exception as err:
            raise AssertionError('Measurement initial faied :{}'.format(err))

    def _convert_wifi_tx_quality_values(self, resp):
        """
        转换WIFI测量结果，科学计数法转换成小数
        """
        values = resp.split(',')

        self._check_status_code(values[0])
        qualities = [*map(Utils.scientific_to_float, values[1:])]

        return qualities

    def _convert_wifi_tx_avg_power(self, resp):
        """
        转换WIFI测量结果，科学计数法转换成小数
        """
        values = resp.split(',')

        self._check_status_code(values[0])
        p_avg = Utils.scientific_to_float(values[-1])

        return round(p_avg, 4)

    def _convert_wifi_tx_occupied_bandwidth(self, resp):
        """
        转换WIFI测量结果，科学计数法转换成小数
        """
        values = resp.split(',')
        self._check_status_code(values[0])

        ob = Utils.scientific_to_float(values[1])

        return ob

    def _convert_wifi_tx_margin(self, resp):
        """
        转换WIFI测量结果，科学计数法转换成小数
        """
        values = resp.split(',')

        margins = [*map(Utils.scientific_to_float, values[1:])]

        return margins

    def _convert_wifi_tx_flatness_state(self, stateCode):
        """
        转换WIFI测量结果，科学计数法转换成小数
        """
        codes = stateCode.split(',')

        flag = None

        flatStates = [Utils.to_enum(int(code), MeasuredState) for code in codes[1:]]

        if not all(flatStates):
            flag = MeasuredState.FAIL
        else:
            flag = MeasuredState.PASS

        return flag

    def get_all_wifi_ofdm_measurements(self):
        """
        获取OFDM调制方式下的所有WIFI测量结果
        """
        samRate = Utils.to_enum(int(self.send_raw_command('VSA1;SRAT?')) / 1000000, SamplingRate)

        if samRate == SamplingRate.MHZ_160:
            resp = self.send_raw_command(
                'VSA1;Init;WIFI;CALC:POW 3,10;CALC:TXQ 3,10;CALC:SEGM3:SPEC:WIDE 3,10;FETC:POW:AVER?;FETC:TXQ:OFDM?;FETC:SPEC:AVER:OBW?;FETC:SPEC:MARG?;FETC:OFDM:SFL:MARG?').split(';')
        else:
            resp = self.send_raw_command(
                'VSA1;Init;WIFI;calc:pow 3,10;calc:txq 3,10;calc:ccdf 3,10;calc:spec 3,10;FETC:POW:AVER?;FETC:TXQ:OFDM?;FETC:SPEC:AVER:OBW?;FETC:SPEC:MARG?;FETC:OFDM:SFL:MARG?').split(';')
        print(resp)
        avgPower = self._convert_wifi_tx_avg_power(resp[0])
        qualityValues = self._convert_wifi_tx_quality_values(resp[1])
        obw = self._convert_wifi_tx_occupied_bandwidth(resp[2])
        #maskMargins = self._convert_wifi_tx_margin(resp[3])
        #flatMargin = min(self._convert_wifi_tx_margin(resp[4]))

        measured = {
            MEASMeasurand.AVG_POWER: avgPower,
            MEASMeasurand.EVM: qualityValues[0],
            MEASMeasurand.FREQ_ERROR: qualityValues[2],  # In OFDM type, the unit of Freq error is Hz
            MEASMeasurand.FREQ_LEAKAGE: qualityValues[4],
            MEASMeasurand.SYMBOL_CLOCK_ERROR: qualityValues[3],
            MEASMeasurand.OCCUPIED_BANDWIDTH: obw / 1000000,
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_1: maskMargins[0],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_2: maskMargins[1],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_3: maskMargins[2],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_4: maskMargins[3],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_1: maskMargins[4],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_2: maskMargins[5],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_3: maskMargins[6],
            #MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_4: maskMargins[7],
            #MEASMeasurand.SPECTRAL_FLATNESS_MIN_MARGIN: flatMargin
        }

        # for measurand in [MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_1, MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_2, MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_3, MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_4, MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_1, MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_2, MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_3, MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_4]:
        # 	if measured[measurand] > 999:
        # 		measured.pop(measurand)

        return measured

    def get_all_wifi_dsss_measurements(self):
        """
        获取DSSS调制方式下的所有WIFI测量结果
        """

        resp = self.send_raw_command(
            'WIFI;CALC:POW 0,1;CALC:TXQ 0,1;CALC:SPEC 0,1;FETC:POW:AVER?;FETC:TXQ:DSSS?;FETC:SPEC:AVER:OBW?;FETC:SPEC:MARG?').split(
            ';')

        avgPower = self._convert_wifi_tx_avg_power(resp[0])
        qualityValues = self._convert_wifi_tx_quality_values(resp[1])
        obw = self._convert_wifi_tx_occupied_bandwidth(resp[2])
        maskMargins = self._convert_wifi_tx_margin(resp[3])

        measured = {
            MEASMeasurand.AVG_POWER: avgPower,
            MEASMeasurand.EVM: qualityValues[1],  # In DSSS type, get the EVM peak value, not the EVM avg value.
            MEASMeasurand.FREQ_ERROR: qualityValues[3],  # In DSSS type, the unit of Freq error is Hz
            MEASMeasurand.FREQ_LEAKAGE: qualityValues[6],
            MEASMeasurand.SYMBOL_CLOCK_ERROR: qualityValues[5],
            MEASMeasurand.OCCUPIED_BANDWIDTH: obw / 1000000,
            MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_1: maskMargins[0],
            MEASMeasurand.SPECTRUM_MASK_MARGIN_LO_2: maskMargins[1],
            MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_1: maskMargins[2],
            MEASMeasurand.SPECTRUM_MASK_MARGIN_UP_2: maskMargins[3]
        }

        return measured

    # endregion

    # region BT Measurement
    def _convert_bt_avg_power(self, resp):
        values = resp.split(',')

        self._check_status_code(values[0])
        p_avg = Utils.scientific_to_float(values[1])

        return p_avg

    def _convert_bt_20db_bandwidth(self, resp):
        values = resp.split(',')

        self._check_status_code(values[0])
        bandwidth = Utils.scientific_to_float(values[1])

        return bandwidth

    def _convert_bt_quality_values(self, resp):
        values = resp.split(',')

        self._check_status_code(values[0])
        qualities = [*map(Utils.scientific_to_float, values[1:])]

        return qualities

    def _convert_bt_acp_min_margin(self, resp):
        values = resp.split(',')

        self._check_status_code(values[0])
        margin = [*map(Utils.scientific_to_float, values[1:])]
        minMargin = min(margin)

        return minMargin

    def get_all_br_measurements(self):
        resp = self.send_raw_command(
            'BT;CLE:ALL;CALC:ALL 0,1;FETC:POW:AVER?;FETC:20BW:AVER?;FETC:TXQ:CLAS:AVER?;FETC:ACP:MARG?').split(';')
        power = self._convert_bt_avg_power(resp[0])
        bandwidth = self._convert_bt_20db_bandwidth(resp[1])
        qualityValues = self._convert_bt_quality_values(resp[2])
        minMargin = self._convert_bt_acp_min_margin(resp[3])

        measured = {
            MEASMeasurand.AVG_POWER: power,
            MEASMeasurand.SPECTRUM_20DB_BANDWIDTH: bandwidth / 1000000,  # convert Hz to MHz
            MEASMeasurand.SPECTRUM_ACP_MIN_MARGIN: minMargin,
            MEASMeasurand.INITIAL_CARRIER_FREQ_ERR: qualityValues[0] / 1000,  # convert Hz to KHz
            MEASMeasurand.CARRIER_FREQ_DRIFT: qualityValues[2] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F2_MAX: qualityValues[-3] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F1_AVG: qualityValues[-5] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F2_AVG: qualityValues[-4] / 1000,  # convert Hz to KHz
        }

        return measured

    def get_all_edr_measurements(self):
        resp = self.send_raw_command('BT;CLE:ALL;CALC:ALL 0,1;FETC:TXQ:EDR:AVER?;FETC:ACP:MARG?').split(';')

        qualityValues = self._convert_bt_quality_values(resp[0])
        minMargin = self._convert_bt_acp_min_margin(resp[1])

        measured = {
            MEASMeasurand.EDR_RELATIVE_TRANSMIT_POWER: qualityValues[6],
            MEASMeasurand.EDR_ACP_MIN_MARGIN: minMargin,
            MEASMeasurand.EDR_OMEGA_I: qualityValues[3] / 1000,  # convert Hz to KHz
            MEASMeasurand.EDR_OMEGA_0: qualityValues[4] / 1000,  # convert Hz to KHz
            MEASMeasurand.EDR_OMEGA_I0: qualityValues[5] / 1000,  # convert Hz to KHz
            MEASMeasurand.EDR_DEVM_AVG: qualityValues[0],
            MEASMeasurand.EDR_DEVM_PEAK: qualityValues[1],
        }

        return measured

    def get_all_le_measurements(self):
        resp = self.send_raw_command('BT;CLE:ALL;CALC:ALL 0,1;FETC:POW:AVER?;FETC:TXQ:LEN:AVER?;FETC:ACP:MARG?').split(
            ';')

        power = self._convert_bt_avg_power(resp[0])
        qualityValues = self._convert_bt_quality_values(resp[1])
        minMargin = self._convert_bt_acp_min_margin(resp[2])

        measured = {
            MEASMeasurand.LE_OUTPUT_POWER: power,
            MEASMeasurand.LE_ACP_MIN_MARGIN: minMargin,
            MEASMeasurand.LE_INITIAL_FREQ_ERR: qualityValues[0] / 1000,  # convert Hz to KHz
            MEASMeasurand.LE_DELTA_F1_AVG: qualityValues[1] / 1000,  # convert Hz to KHz
            MEASMeasurand.LE_DELTA_F2_AVG: qualityValues[2] / 1000,  # convert Hz to KHz
            MEASMeasurand.LE_DELTA_F2_MAX: qualityValues[3] / 1000,  # convert Hz to KHz
            MEASMeasurand.LE_FN_MAX: qualityValues[5] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F0_FN_MAX: qualityValues[-5] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F1_F0: qualityValues[-4] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_FN_FN5_MAX: qualityValues[-3] / 1000,  # convert Hz to KHz
            MEASMeasurand.DELTA_F3_F0: qualityValues[-4] / 1000,  # Special for BLE 125Kbps
            MEASMeasurand.DELTA_FN_FN3_MAX: qualityValues[-3] / 1000  # Special for BLE 125Kbps
        }

        return measured

    # endregion


