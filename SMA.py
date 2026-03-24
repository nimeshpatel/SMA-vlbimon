import time
import subprocess,gc
import numpy as np
from decimal import Decimal as D
import sys, signal, os
# Removed pydsm import - using Redis instead
import redis
from math import *

from datetime import datetime
#from HTMLParser import HTMLParser
from html.parser import HTMLParser
from time import sleep
from urllib.request import urlopen, URLError

maserURL = 'http://172.22.4.240/monit.htm'

class maserParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_lock = False
        self.in_ubatta = False
        self.in_ibatta = False
        self.in_ubattb = False
        self.in_ibattb = False
        self.in_seth = False
        self.in_meash = False
        self.in_ipur = False
        self.in_idis = False
        self.in_hlight = False
        self.in_itheat = False
        self.in_ibheat = False
        self.in_isheat = False
        self.in_utcheat = False
        self.in_esheat = False
        self.in_ebheat = False
        self.in_iheat = False
        self.in_theat = False
        self.in_boxt = False
        self.in_boxi = False
        self.in_ambt = False
        self.in_cfield = False
        self.in_uvar = False
        self.in_uhte = False
        self.in_ihte = False
        self.in_uhti = False
        self.in_ihti = False
        self.in_hstpres = False
        self.in_hstheat = False
        self.in_pirani = False
        self.in_u405 = False
        self.in_uocx = False
        self.in_p24 = False
        self.in_p15 = False
        self.in_m15 = False
        self.in_p5 = False
        self.in_m5 = False
        self.in_p8 = False
        self.in_p18 = False
        self.in_dds = False

    def handle_data(self, data):

        if self.in_ubatta:
            self.ubatta = float(data)
            self.in_ubatta = False
        elif data == 'U batt.A[V]':
            self.in_ubatta = True

        if self.in_ibatta:
            self.ibatta = float(data)
            self.in_ibatta = False
        elif data == 'I batt.A[A]':
            self.in_ibatta = True

        if self.in_ubattb:
            self.ubattb = float(data)
            self.in_ubattb = False
        elif data == 'U batt.B[V]':
            self.in_ubattb = True

        if self.in_ibattb:
            self.ibattb = float(data)
            self.in_ibattb = False
        elif data == 'I batt.B[A]':
            self.in_ibattb = True

        if self.in_seth:
            self.seth = float(data)
            self.in_seth = False
        elif data == 'Set H[V]':
            self.in_seth = True

        if self.in_meash:
            self.meash = float(data)
            self.in_meash = False
        elif data == 'Meas. H[V]':
            self.in_meash = True

        if self.in_ipur:
            self.ipur = float(data)
            self.in_ipur = False
        elif data == 'I pur.[A]':
            self.in_ipur = True

        if self.in_idis:
            self.idis = float(data)
            self.in_idis = False
        elif data == 'I diss.[A]':
            self.in_idis = True

        if self.in_hlight:
            self.hlight = float(data)
            self.in_hlight = False
        elif data == 'H light[V]':
            self.in_hlight = True

        if self.in_itheat:
            self.itheat = float(data)
            self.in_itheat = False
        elif data == 'IT heater[V]':
            self.in_itheat = True

        if self.in_ibheat:
            self.ibheat = float(data)
            self.in_ibheat = False
        elif data == 'IB heater[V]':
            self.in_ibheat = True

        if self.in_isheat:
            self.isheat = float(data)
            self.in_isheat = False
        elif data == 'IS heater[V]':
            self.in_isheat = True

        if self.in_utcheat:
            self.utcheat = float(data)
            self.in_utcheat = False
        elif data == 'UTC heater[V]':
            self.in_utcheat = True

        if self.in_esheat:
            self.esheat = float(data)
            self.in_esheat = False
        elif data == 'ES heater[V]':
            self.in_esheat = True

        if self.in_ebheat:
            self.ebheat = float(data)
            self.in_ebheat = False
        elif data == 'I heater[V]':
            self.in_ebheat = True

        if self.in_iheat:
            self.iheat = float(data)
            self.in_iheat = False
        elif data == 'I heater[V]':
            self.in_iheat = True

        if self.in_theat:
            self.theat = float(data)
            self.in_theat = False
        elif data == 'T heater[V]':
            self.in_theat = True

        if self.in_boxt:
            self.boxt = float(data)
            self.in_boxt = False
        elif data[:-4] == 'Boxes temp':
            self.in_boxt = True

        if self.in_boxi:
            self.boxi = float(data)
            self.in_boxi = False
        elif data == 'I boxes[A]':
            self.in_boxi = True

        if self.in_ambt:
            self.ambt = float(data)
            self.in_ambt = False
        elif data[:-4] == 'Amb.temp.':
            self.in_ambt = True

        if self.in_cfield:
            self.cfield = float(data)
            self.in_cfield = False
        elif data == 'C field[V]':
            self.in_cfield = True

        if self.in_uvar:
            self.uvar = float(data)
            self.in_uvar = False
        elif data == 'U varactor[V]':
            self.in_uvar = True

        if self.in_uhte:
            self.uhte = float(data)
            self.in_uhte = False
        elif data == 'U HT ext.[kV]':
            self.in_uhte = True

        if self.in_ihte:
            self.ihte = float(data)
            self.in_ihte = False
        elif data == 'I HT ext[uA]':
            self.in_ihte = True

        if self.in_uhti:
            self.uhti = float(data)
            self.in_uhti = False
        elif data == 'U HT int.[kV]':
            self.in_uhti = True

        if self.in_ihti:
            self.ihti = float(data)
            self.in_ihti = False
        elif data == 'I HT int.[uA]':
            self.in_ihti = True

        if self.in_hstpres:
            self.hstpres = float(data)
            self.in_hstpres = False
        elif data == 'H st.pres.[bar]':
            self.in_hstpres = True

        if self.in_hstheat:
            self.hstheat = float(data)
            self.in_hstheat = False
        elif data == 'H st. heat[V]':
            self.in_hstheat = True

        if self.in_pirani:
            self.pirani = float(data)
            self.in_pirani = False
        elif data == 'Pirani heat.[V]':
            self.in_pirani = True

        if self.in_u405:
            self.u405 = float(data)
            self.in_u405 = False
        elif data == 'U 405kHz[V]':
            self.in_u405 = True

        if self.in_uocx:
            self.uocx = float(data)
            self.in_uocx = False
        elif data == 'U OCXO[V]':
            self.in_uocx = True

        if self.in_p24:
            self.p24 = float(data)
            self.in_p24 = False
        elif data == '+24 VDC[V]':
            self.in_p24 = True

        if self.in_p15:
            self.p15 = float(data)
            self.in_p15 = False
        elif data == '+15 VDC[V]':
            self.in_p15 = True

        if self.in_m15:
            self.m15 = float(data)
            self.in_m15 = False
        elif data == '-15 VDC[V]':
            self.in_m15 = True

        if self.in_p5:
            self.p5 = float(data)
            self.in_p5 = False
        elif data == '+5 VDC[V]':
            self.in_p5 = True

        if self.in_m5:
            self.m5 = float(data)
            self.in_m5 = False
        elif data == '-5 VDC[V]':
            self.in_m5 = True

        if self.in_p8:
            self.p8 = float(data)
            self.in_p8 = False
        elif data == '+8 VDC[V]':
            self.in_p8 = True

        if self.in_p18:
            self.p18 = float(data)
            self.in_p18 = False
        elif data == '+18 VDC[V]':
            self.in_p18 = True

        if self.in_lock:
            if data == ' 1':
                self.lockStatus = True
            else:
                self.lockStatus = False
            self.in_lock = False
        elif data == 'Lock':
            self.in_lock = True

        if self.in_dds:
            self.dds = float(data)
            self.in_dds = False
        elif data == 'DDS':
            self.in_dds = True

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise IOError("Timeout")

signal.signal(signal.SIGALRM, handler)
signal.alarm(1800)

def readShmValue(dsmVariable):
    result = subprocess.run(['/application/shmValue/test/shmValue','-mcolossus',dsmVariable],\
                 stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    value = float(result.stdout.decode('utf-8').split()[0])
    gc.collect()
    return value

# Helper functions for Redis
def redis_hget_float(redis_client, hash_key, field_key, default=0.0):
    """Safely retrieve a float value from Redis hash"""
    try:
        value = redis_client.hget(hash_key, field_key)
        if value is not None:
            return float(value.decode('utf-8'))
        return default
    except Exception as e:
        print(f"Error reading {hash_key}:{field_key} - {e}")
        return default

def redis_hget_str(redis_client, hash_key, field_key, default=''):
    """Safely retrieve a string value from Redis hash"""
    try:
        value = redis_client.hget(hash_key, field_key)
        if value is not None:
            return value.decode('utf-8')
        return default
    except Exception as e:
        print(f"Error reading {hash_key}:{field_key} - {e}")
        return default

def redis_hget_int(redis_client, hash_key, field_key, default=0):
    """Safely retrieve an integer value from Redis hash"""
    try:
        value = redis_client.hget(hash_key, field_key)
        if value is not None:
            return int(float(value.decode('utf-8')))
        return default
    except Exception as e:
        print(f"Error reading {hash_key}:{field_key} - {e}")
        return default

#def median(sample):
#    newSample = sorted(sample)
#    n = len(newSample)
#    if (n % 2) == 0:
#        return (newSample[round(n/2)-1] + newSample[round(n/2)])/2.0
#    else:
#        return newSample[n/2]

#-- exact floating point arithmetic
def sumf(a, b):
    return float(D(str(a)) + D(str(b)))
def prodf(a, b):
    return float(D(str(a)) * D(str(b)))

class Sitedata(object):
    def __init__(self, sitelist):
        self.sitelist = sitelist

    def close(self):
        """Clean up this class, e.g. close any threads used"""
        pass

    def collect(self):
        """Collect data points"""
        #-- start with empty dict
        params = {}

        #-- default timestamp: now
        #-- time: seconds since 1970 Jan 1 UTC, also known as "unix time".
        utime = time.mktime(time.localtime())
        weatherHost = 'hal9000'
        weatherRefAnt = 6
        tauHost = 'colossus'

        # Initialize Redis connection
        r = redis.StrictRedis('128.171.116.189')

        #-- insert any new values with times at which those values were measured
        #-- if no measurement time is available, use the current time
        # Use antenna 1 as reference
        params['OBS.TIMEZONE'] = [utime, -10]

        # Use antenna 1 as default reference antenna
        refAnt = 1
        refAntName = 'acc%d' % (refAnt)

        # Build antenna lists
        line ="1 2 3 4 5 6 7 8"
        tok = line.split()
        antennas = []
        phasedAntennas = []
        for i in range(len(tok)):
            ant = int(tok[i])
            if 0 < ant < 9:
                antennas.append(ant)
                phasedAntennas.append(ant)
        onlineAnts = [0,1,1,1,1,1,1,1,1]
        onSource = True
        mode = 'Tracking'
        tsys1Values = []
        tsys2Values = []
        waveplateOrientation = []
        tcalValues = []
        rxALocked = True;
        rxBLocked = True;
        wavePlatesIn = True
        for ant in antennas:
            antName = 'acc%d' %(ant)
            rm_key = 'RM:%s' % antName
            if onlineAnts[ant] == 1:
                if wavePlatesIn:
                    waveplate_status = redis_hget_int(r, rm_key, 'RM_WAVEPLATE_ROTATION_STATUS_S', default=0)
                    if waveplate_status != 4:
                        wavePlatesIn = False
                if rxALocked:
                    gunn1_locked = redis_hget_int(r, rm_key, 'RM_GUNN1_LOCKED_S', default=0)
                    if gunn1_locked != 1:
                        rxALocked = False
                if rxBLocked:
                    gunn2_locked = redis_hget_int(r, rm_key, 'RM_GUNN2_LOCKED_S', default=0)
                    if gunn2_locked != 1:
                        rxBLocked = False
                azTrackError = redis_hget_float(r, rm_key, 'RM_AZ_TRACKING_ERROR_F', default=0.0)
                elTrackError = redis_hget_float(r, rm_key, 'RM_EL_TRACKING_ERROR_F', default=0.0)
                trackError = sqrt(azTrackError**2 + elTrackError**2)
                if ant != 5:
                    if trackError > 10.0:
                        onSource = False
                    if trackError > 100.0:
                        mode = 'slewing'
                tsys1Values.append(redis_hget_float(r, rm_key, 'RM_TSYS_D', default=99999.9))
                tsys2Values.append(redis_hget_float(r, rm_key, 'RM_TSYS2_D', default=99999.9))
                waveplateOrientation.append(redis_hget_int(r, rm_key, 'RM_WAVEPLATE_ROTATION_STATUS_S', default=0))
                tcalValues.append(redis_hget_float(r, rm_key, 'RM_UNHEATEDLOAD_TEMPERATURE_F', default=99999.9))
        if len(antennas) > 0:
            if len(set(waveplateOrientation)) == 1:
                if waveplateOrientation[0] == 1:
                    iFPol1 = 'R'
                    iFPol2 = 'L'
                elif waveplateOrientation[0] == 2:
                    iFPol1 = 'L'
                    iFPol2 = 'R'
                else:
                    iFPol1 = '?'
                    iFPol2 = '?'
            else:
                iFPol1 = '?'
                iFPol2 = '?'
            if len(tsys1Values) > 0:
                tsys1 =np.median(tsys1Values)
            else:
                tsys1 = 99999.9
            if len(tsys2Values) > 0:
                tsys2 = np.median(tsys2Values)
            else:
                tsys2 = 99999.9
            if len(tcalValues) > 0:
                tcal = np.median(tcalValues)
            else:
                tcal = 99999.9
        else:
            tsys1 = 99999.9
            tsys2 = 99999.9
            tcal = 99999.9
        if not (40.0 < tsys1 < 10000.0):
            tsys1 = 99999.9
        if not (40.0 < tcal < 400.0):
            tcal = 99999.9
        if not (40.0 < tsys2 < 10000.0):
            tsys2 = 99999.9

        rm_ref_key = 'RM:%s' % refAntName
        drive_status = redis_hget_int(r, rm_ref_key, 'RM_ANTENNA_DRIVE_STATUS_B', default=1)
        if drive_status == 0:
            mode = 'stationary'
        params['TEL.OBS_MODE'] = [utime, mode]
        if len(antennas) < 2:
            params['TEL.STATUS'] = [utime, 'idle']
        else:
            params['TEL.STATUS'] = [utime, 'online']

        rAHours = redis_hget_float(r, rm_ref_key, 'RM_RA_APP_HR_D', default=0.0)
        decDegs = redis_hget_float(r, rm_ref_key, 'RM_DEC_APP_DEG_D', default=0.0)
        if decDegs < 0.0:
            coordString = '%7.6f%7.6f' % (rAHours, decDegs)
        else:
            coordString= '%7.6f+%7.6f' % (rAHours, decDegs)
        params['TEL.APP_RA_DEC'] = [utime, coordString]

        az = redis_hget_float(r, rm_ref_key, 'RM_ACTUAL_AZ_DEG_F', default=0.0)
        el = redis_hget_float(r, rm_ref_key, 'RM_ACTUAL_EL_DEG_F', default=0.0)
        azElString = '%1.5f+%1.5f' % (az, el)
        params['TEL.AZEL'] = [utime, azElString]        
#        params['IF1.CENTER_FREQ'] = [utime, 7.0]
#        params['IF1.CENTER_FREQ'] = [utime, 2.0]
        if len(antennas) > 0:
            params['IF1.POL'] = [utime, iFPol1]
            params['IF2.POL'] = [utime, iFPol2]
        params['IF1.TSYS'] = [utime, 2.0*tsys1]
        params['IF1.TSYS_AZEL'] = [utime, azElString]
#        params['IF2.CENTER_FREQ'] = [utime, 7.0]
#        params['IF2.CENTER_FREQ'] = [utime, 2.0]
        params['IF2.TSYS'] = [utime, 2.0*tsys2]
        params['IF2.TSYS_AZEL'] = [utime, azElString]

        SMASource = redis_hget_str(r, rm_ref_key, 'RM_SOURCE_C34', default='')
        if (4.0 < az < 16.0) and (SMASource.strip() == 'target'):
            params['TEL.SOURCE_NAME'] = [utime, 'Stowed']
        else:
            params['TEL.SOURCE_NAME'] = [utime, SMASource.strip()]

        rAHours = redis_hget_float(r, rm_ref_key, 'RM_RA_CAT_HOURS_F', default=0.0)
        decDegs = redis_hget_float(r, rm_ref_key, 'RM_DEC_CAT_DEG_F', default=0.0)
        if decDegs < 0.0:
            coordString = '%7.6f%7.6f' % (rAHours, decDegs)
        else:
            coordString= '%7.6f+%7.6f' % (rAHours, decDegs)
        params['TEL.EPOCH_RA_DEC'] = [utime, coordString]
        params['TEL.EPOCH'] = [utime, 'J2000']
        params['GAIN.STATUS'] = [utime, False]
        params['PHASING.STATUS'] = [utime, False]
        params['PHASING.REF_ANT'] = [utime, 6]
        params['PHASING.REF_PAD'] = [utime, 'pad 1']
        params['PHASING.REF_COORDS'] = [utime, '+19.82420-155.47752']
        params['PHASING.PHASE_CENTER'] = [utime, coordString]
        params['PHASING.N_ANTENNAS'] = [utime, len(phasedAntennas)]
        if len(line) > 1:
            phasedString = ''
            tok = line.split()
            for i in range(len(tok)):
                if tok[i] != '5':
                    phasedString += tok[i]+' '
            params['PHASING.IDS'] = [utime, phasedString]
        else:
            params['PHASING.IDS'] = [utime, 'None']
        params['TEL.ON_SOURCE'] = [utime, onSource]

        # Weather data from Redis
        weather_key = 'DSM:colossus:SMA_METEOROLOGY_X'
        tempC = redis_hget_float(r, weather_key, 'TEMP_F', default=0.0)
        params['ENVIRO.Air_Temp'] = [utime, sumf(tempC, 273.15)] #-- convert C to K

        mbar = redis_hget_float(r, weather_key, 'MBAR_F', default=625.0)
        params['ENVIRO.Pressure'] = [utime, prodf(.1, mbar)] #-- convert hPa to kPa

        humid = redis_hget_float(r, weather_key, 'HUMIDITY_F', default=50.0)
        params['ENVIRO.Humidity'] = [utime, humid]
        if humid > 97.0:
            params['ENVIRO.rain_event'] = [utime, 'fog']
        else:
            params['ENVIRO.rain_event'] = [utime, 'dry']

        windDir = redis_hget_float(r, weather_key, 'WINDDIR_F', default=0.0)
        if not (0.0 <= windDir < 360.0):
            windDir = 0.0
        params['ENVIRO.Wind_Dir'] = [utime, windDir]

        windSpeed = redis_hget_float(r, weather_key, 'WINDSPEED_F', default=0.0)
        params['ENVIRO.Wind_Speed'] = [utime, windSpeed]
        phasingValues = []
#        
#        for chunk in [1, 2]:
#            for pol in [0, 1]:
#                phasingValues.append(r.get('swarm.calibrate_vlbi.efficiency.chk{0}.pol{1}'.format(chunk, pol)))
#        if None in phasingValues:
#            params['PHASING.PHASING_NOW'] = [utime, False]
#            params['PHASING.EFF'] = [utime, 0.00]
#        else:
#            realPhase = []
#            for i in range(len(phasingValues)):
#                realPhase.append(float(phasingValues[i]))
#            phaseUp = median(realPhase)
#            print 'Median phasing efficiency', phaseUp
#            params['PHASING.PHASING_NOW'] = [utime, True]
#            params['PHASING.EFF'] = [utime, phaseUp]

        tau225 = redis_hget_float(r, 'weather:forecast:gfs', 'tau225', default=0.05)
        params['ENVIRO.SMA_TAU'] = [utime, tau225]
        params['ENVIRO.PWV'] = [utime, prodf(20.0,tau225)]
#        pm = pydsm.read('phasemon','PHASEMON_DATA_X')['PHASE_STRUCT_V10_V19_F'][0][0][5]*225.0/12.4
        pm = 0.0
        params['ENVIRO.PM'] = [utime, pm]
        params['ENVIRO.WVR_PRESENT'] = [utime, False]
        params['ENVIRO.ONLINE'] = [utime, True]

        # Receiver status from Redis
        rxAName = redis_hget_str(r, rm_ref_key, 'RM_ACTIVE_LOW_RECEIVER_C10', default='')
        rxBName = redis_hget_str(r, rm_ref_key, 'RM_ACTIVE_HIGH_RECEIVER_C10', default='')
        if (rxAName == 'A1') or (rxAName == 'B1'):
            rxAActive = True
        else:
            rxAActive = False
        if (rxBName == 'C') or (rxBName == 'E'):
            rxBActive = True
        else:
            rxBActive = False
#        print(rxAActive, rxBActive)
        params['RXA_ENG_TASK.ONLINE'] = [utime, rxAActive]
        params['IF1.ONLINE'] = [utime, rxAActive]
        params['RXB_ENG_TASK.ONLINE'] = [utime, rxBActive]
        params['IF2.ONLINE'] = [utime, rxBActive]        
            
#        params['RXA_ENG_TASK.LO_FREQ_DEMAND'] = [utime, prodf(1.0e-9, dDSInfo['FREQ_V3_D'][0][1])]
#        params['IF1.CENTER_FREQ'] = [utime, prodf(1.0e-9, dDSInfo['FREQ_V3_D'][0][1])]
#        params['IF2.CENTER_FREQ'] = [utime, prodf(1.0e-9, dDSInfo['FREQ_V3_D'][0][2])]
        params['RXA_ENG_TASK.WAVEPLATE_IN'] = [utime, wavePlatesIn]
        params['RXA_ENG_TASK.NRIFS'] = [utime, 2]
        params['RXA_ENG_TASK.CAL_TEMP'] = [utime, sumf(tcal, 273.15)]
        params['RXA_ENG_TASK.ALL_LOCKED'] = [utime, rxALocked]
        params['RXA_ENG_TASK.SYNTHOFF'] = [utime, 0.0]
#        params['RXB_ENG_TASK.LO_FREQ_DEMAND'] = [utime, prodf(1.0e-9, dDSInfo['FREQ_V3_D'][0][2])]
        params['RXB_ENG_TASK.WAVEPLATE_IN'] = [utime, wavePlatesIn]
        params['RXB_ENG_TASK.NRIFS'] = [utime, 2]
        params['RXB_ENG_TASK.CAL_TEMP'] = [utime, sumf(tcal, 273.15)]
        params['RXB_ENG_TASK.ALL_LOCKED'] = [utime, rxBLocked]
        params['RXB_ENG_TASK.SYNTHOFF'] = [utime, 0.0]

#        parser = maserParser()
#        hc = urlopen(maserURL, timeout=5)
#        parser.feed(hc.read())
##        print 'battA', parser.ubatta, parser.ibatta
#        params['MASER.battery_voltage_a'] = [utime, parser.ubatta]
#        params['MASER.battery_current_a'] = [utime, parser.ibatta]
##        print 'battB', parser.ubattb, parser.ibattb
#        params['MASER.battery_voltage_b'] = [utime, parser.ubattb]
#        params['MASER.battery_current_b'] = [utime, parser.ibattb]
##        print 'Set H[V]', parser.seth
#        params['MASER.hydrogen_pressure_setting'] = [utime, parser.seth]
##        print 'Meas. H[V]', parser.meash
#        params['MASER.hydrogen_pressure_measurement'] = [utime, parser.meash]
##        print 'I pur.[A]', parser.ipur
#        params['MASER.purifier_current'] = [utime, parser.ipur]
##        print 'I diss.[A]', parser.idis
#        params['MASER.dissociator_current'] = [utime, parser.idis]
##        print 'H light[V]', parser.hlight
#        params['MASER.dissociator_light'] = [utime, parser.hlight]
##        print 'IT heater[V]', parser.itheat
#        params['MASER.heater_internal_top'] = [utime, parser.itheat]
##        print 'IB heater[V]', parser.ibheat
#        params['MASER.heater_internal_bottom'] = [utime, parser.ibheat]
##        print 'IS heater[V]', parser.isheat
#        params['MASER.heater_internal_side'] = [utime, parser.isheat]
##        print 'UTC heater[V]', parser.utcheat
#        params['MASER.heater_thermal_control_unit'] = [utime, parser.utcheat]
##        print 'ES heater[V]', parser.esheat
#        params['MASER.heater_external_side'] = [utime, parser.esheat]
##        print 'EB heater[V]', parser.ebheat
#        params['MASER.heater_external_bottom'] = [utime, parser.ebheat]
##        print 'I heater[V]', parser.iheat
#        params['MASER.heater_isolator'] = [utime, parser.iheat]
##        print 'T heater[V]', parser.theat
#        params['MASER.heater_tube'] = [utime, parser.theat]
##        print 'Boxes temp.[C]', parser.boxt
#        params['MASER.boxes_temperature'] = [utime, parser.boxt]
##        print 'I boxes[A]', parser.boxi
#        params['MASER.boxes_current'] = [utime, parser.boxi]
##        print 'Amb.temp.[C]', parser.ambt
#        params['MASER.ambient_temperature'] = [utime, parser.ambt]
##        print 'C field[V]', parser.cfield
#        params['MASER.cfield_voltage'] = [utime, parser.cfield]
##        print 'U varactor[V]', parser.uvar
#        params['MASER.varactor_voltage'] = [utime, parser.uvar]
##        print 'U HT ext.[kV]', parser.uhte
#        params['MASER.external_high_voltage_value'] = [utime, parser.uhte]
##        print 'I HT ext[uA]', parser.ihte
#        params['MASER.external_high_voltage_current'] = [utime, parser.ihte]
##        print 'U HT int.[kV]', parser.uhti
#        params['MASER.internal_high_voltage_value'] = [utime, parser.uhti]
##        print 'I HT int.[uA]', parser.ihti
#        params['MASER.internal_high_voltage_current'] = [utime, parser.ihti]
##        print 'H st.pres.[bar]', parser.hstpres
#        params['MASER.hydrogen_storage_pressure'] = [utime, parser.hstpres]
##        print 'H st. heat[V]', parser.hstheat
#        params['MASER.hydrogen_storage_heater'] = [utime, parser.hstheat]
##        print 'Pirani heat.[V]', parser.pirani
#        params['MASER.pirani_heater'] = [utime, parser.pirani]
##        print 'U 405kHz[V]', parser.u405
#        params['MASER.405kHz_amplitude'] = [utime, parser.u405]
##        print 'U OCXO[V]', parser.uocx
#        params['MASER.ocxo_voltage'] = [utime, parser.uocx]
##        print '+24 VDC[V]', parser.p24
#        params['MASER.supply_p24V_voltage'] = [utime, parser.p24]
##        print '+15 VDC[V]', parser.p15
#        params['MASER.supply_p15V_voltage'] = [utime, parser.p15]
##        print '-15 VDC[V]', parser.m15
#        params['MASER.supply_m15V_voltage'] = [utime, parser.m15]
##        print '+5 VDC[V]', parser.p5
#        params['MASER.supply_p5V_voltage'] = [utime, parser.p5]
##        print '-5 VDC[V]', parser.m5
#        params['MASER.supply_m5V_voltage'] = [utime, parser.m5]
##        print '+8 VDC[V]', parser.p8
#        params['MASER.supply_p8V_voltage'] = [utime, parser.p8]
##        print '+18 VDC[V]', parser.p18
#        params['MASER.supply_p18V_voltage'] = [utime, parser.p18]
##        print 'Lock', parser.lockStatus
#        params['MASER.lock'] = [utime, parser.lockStatus]
##        print 'DDS', parser.dds        
#        params['MASER.dds'] = [utime, parser.dds]
#
#        try:
#            for line in open('/global/logs/2EHT'):
#                params['MESS.MESSAGE'] = [utime, line]
#        except IOError:
#            params['MESS.MESSAGE'] = [utime, ' ']
#        try:
#            for line in open('/global/logs/EHTStatus'):
#                params['MESS.STATUS'] = [utime, line]
#        except IOError:
#            params['MESS.STATUS'] = [utime, ' ']
#        try:
#            for line in open('/global/logs/EHTWeather'):
#                params['MESS.WEATHER'] = [utime, line]
#        except IOError:
#            params['MESS.WEATHER'] = [utime, ' ']

        params_wrapped = {k: [v] for k,v in list(params.items())}
        return params_wrapped
