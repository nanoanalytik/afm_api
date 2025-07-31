# API version 1.1

## Change log 

- Added command object “DataSubscription” to manage all data subscriptions
- Added subscription to AFM system log
- Added data format for raw measurement data “float”, and scientific notation for the format “txt”
- Adde APIEcho command for communication testing

# Commands list
<a name="commands-list"></a>

This section lists all available AFM Control objects and commands supported by API version 1.0 in alphabetical order. Each chapter describes a given object name, a short function description, and provides exemplary API commands and responses. API users are free to compose sequences of commands. It is also recommended to experiment with API server operation using tools like Postman or Python scripts to fine-tune the AFM system to the particular AFM applications. 

Please note that only authenticated API clients are allowed to exchange data with the AFM Control application server. 

# List of commands 

- [ActionActuationFrequencySweepStart](#actionactuationfrequencysweepstart)
- [ActionActuationFrequencySweepStop](#actionactuationfrequencysweepstop)
- [ActionAddMeasurementChannel](#actionaddmeasurementchannel)
- [ActionMeasurementBufferClear](#actionmeasurementbufferclear)
- [ActionMeasurementStart](#actionmeasurementstart)
- [ActionMeasurementStop](#actionmeasurementstop)
- [ActionMotorApproachContinuous](#actionmotorapproachcontinuous)
- [ActionMotorApproachOnce](#actionmotorapproachonce)
- [ActionMotorRetractContinuous](#actionmotorretractcontinuous)
- [ActionMotorRetractOnce](#actionmotorretractonce)
- [ActionMotorSafeDistance](#actionmotorsafedistance)
- [ActionRemoveMeasurementChannel](#actionremovemeasurementchannel)
- [ActionScannerReset](#actionscannerreset)
- [ActiveMeasurementChannels](#activemeasurementchannels)
- [ActuationAmplitude](#actuationamplitude)
- [ActuationFrequency](#actuationfrequency)
- [ActuationFrequencySweepStart](#actuationfrequencysweepstart)
- [ActuationFrequencySweepStop](#actuationfrequencysweepstop)
- [ActuationHalfResonanceFrequency](#actuationhalfresonancefrequency)
- [ActuationOutput](#actuationoutput)
- [AFMAmplitudeSetPoint](#afmamplitudesetpoint)
- [AFMPIDConstantI](#afmpidconstanti)
- [AFMPIDConstantP](#afmpidconstantp)
- [APIEcho](#apiecho)
- [APIVersion](#apiversion)
- [authenticate](#authenticate)
- [DataSubscription](#datasubscription)
- [FoundResonanceProperties](#foundresonanceproperties)
- [FrequencySweepStatus](#frequencysweepstatus)
- [MeasurementData](#measurementdata)
- [MeasurementDataActiveChannel](#measurementdataactivechannel)
- [MeasurementDataCorrectionMode](#measurementdatacorrectionmode)
- [MeasurementDataDirectionMode](#measurementdatadirectionmode)
- [MeasurementDataSubscription](#measurementdatasubscription)
- [MeasurementStatus](#measurementstatus)
- [MotorApproachMode](#motorapproachmode)
- [MotorPosition](#motorposition)
- [MotorSpeed](#motorspeed)
- [MotorStatus](#motorstatus)
- [ScannerCenterX](#scannercenterx)
- [ScannerCenterY](#scannercentery)
- [ScannerDeflectionZ](#scannerdeflectionz)
- [ScannerLimitZ](#scannerlimitz)
- [ScannerLinesPerSecond](#scannerlinespersecond)
- [ScannerMode](#scannermode)
- [ScannerPosition](#scannerposition)
- [ScannerProfileLine](#scannerprofileline)
- [ScannerProfileLineRepetition](#scannerprofilelinerepetitions)
- [ScannerProfileLineLock](#scannerprofilelinelock)
- [ScannerRange](#scannerrange)
- [ScannerResolution](#scannerresolution)
- [ScannerRotation](#scannerrotation)


# ActionActuationFrequencySweepStart
<a name="actionactuationfrequencysweepstart"></a>

## Description

Begin frequency sweep

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionActuationFrequencySweepStart",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false




# ActionActuationFrequencySweepStop
<a name="actionactuationfrequencysweepstop"></a>

## Description

End sweep frequency

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionActuationFrequencySweepStop",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false




# ActionAddMeasurementChannel
<a name="actionaddmeasurementchannel"></a>

## Description

Add a measurement channel

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionAddMeasurementChannel",
	"payload": {
	    "property": "channel",
	    "value": true
	}
}
```

### Expected SET Values

true only




# ActionMeasurementBufferClear
<a name="actionmeasurementbufferclear"></a>

## Description

Clear scanned picture buffer

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionMeasurementBufferClear",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false


# ActionMeasurementStart
<a name="actionmeasurementstart"></a>

## Description

Begin surface scanning

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActionMeasurementStart",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true

## Get Example

```
{
	"command": "get",
	"object": "ActionMeasurementStart",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

true, false

## Notes

Value "true" in SET command triggers the measurement start. Value in the GET response returns true when system is measuring and false when is in idle mode.


# ActionMeasurementStop
<a name="actionmeasurementstop"></a>

## Description

Stop surface scanning

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActionMeasurementStop",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true

## Get Example

```
{
	"command": "get",
	"object": " ActionMeasurementStop",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

true, false

## Notes

Value "true" in SET command triggers the measurement stop. Value in the GET response returns true when system is in idle mode and false when is measuring.


# ActionMotorApproachContinuous
<a name="actionmotorapproachcontinuous"></a>

## Description

Approach Cantilever towards the surface

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionMotorRetractContinuous",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

# ActionMotorApproachOnce
<a name="actionmotorapproachonce"></a>

## Description

Single approach step towards the surface

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionMotorRetractOnce",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

## Notes

One single step likely will be executed faster than getting the motor status. Therefore "false" response is to be expected in a typical case.


# ActionMotorRetractContinuous
<a name="actionmotorretractcontinuous"></a>

## Description

Rectract Cantilever from the surface

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActionMotorRetractContinuous",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false

## Get Example

```
{
	"command": "get",
	"object": "ActionMotorRetractContinuous",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

true, false


# ActionMotorRetractOnce
<a name="actionmotorretractonce"></a>

## Description

Single retract step from the surface

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionMotorRetractOnce",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false


# ActionMotorSafeDistance
<a name="actionmotorsafedistance"></a>

## Description

Go to safe distance

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionMotorSafeDistance",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

### Expected SET Values

true, false


# ActionRemoveMeasurementChannel
<a name="actionremovemeasurementchannel"></a>

## Description

Remove measurement channel

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionRemoveMeasurementChannel",
	"payload": {
	    "property": "index",
	    "channel": "1"
	}
}
```

### Expected SET Values

unsigned int

## Notes

Removing the main channel (0) is not permitted. 


# ActionScannerReset
<a name="actionscannerreset"></a>

## Description

Reset the scaning settings

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActionScannerReset",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```

## Notes

Strictly technically, it is possible to get the ActionScannerReset value, but the respons gets the status whether the action is in the middle of operation, and not whether the scanner has been reset after the the set command was sent. 


# ActiveMeasurementChannels
<a name="activemeasurementchannels"></a>

## Description

Returns number of active measurement channels

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "ActiveMeasurementChannels",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int

## Notes

unsigned int between 1 and 4, which is the maximum number of channels supported for this software version. 


# ActuationAmplitude
<a name="actuationamplitude"></a>

## Description

Cantilever actuation amplitude

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActuationAmplitude",
	"payload": {
	    "property": "value",
	    "value": 0.150
	}
}
```

### Expected SET Values

floating-point value  

## Get Example

```
{
	"command": "get",
	"object": "ActuationAmplitude",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

floating-point value  


# ActuationFrequency
<a name="actuationfrequency"></a>

## Description

Cantilever actuation frequency

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActuationFrequency",
	"payload": {
	    "property": "value",
	    "value": 32733
	}
}
```

### Expected SET Values

floating-point value 

## Get Example

```
{
	"command": "get",
	"object": "ActuationFrequency",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

floating-point value  


# ActuationFrequencySweepStart
<a name="actuationfrequencysweepstart"></a>

## Description

Start sweep frequency value

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActuationFrequencySweepStart",
	"payload": {
	    "property": "value",
	    "value": 10000
	}
}
```

### Expected SET Values

floating-point value 


# ActuationFrequencySweepStop
<a name="actuationfrequencysweepstop"></a>

## Description

End sweep frequency value

## Set/Get Information

set

## Set Example

```
{
	"command": "set",
	"object": "ActuationFrequencySweepStop",
	"payload": {
	    "property": "value",
	    "value": 40000
	}
}
```

### Expected SET Values

floating-point value 


# ActuationHalfResonanceFrequency
<a name="actuationhalfresonancefrequency"></a>

## Description

Half omega actuation of the cantilever resonance frequency

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActuationHalfResonanceFrequency",
	"payload": {
	    "property": "state",
	    "value": true
	}
}
```

### Expected SET Values

true, false

## Get Example

```
{
	"command": "get",
	"object": "ActuationHalfResonanceFrequency",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

true, false


# ActuationOutput
<a name="actuationoutput"></a>

## Description

Switch on/off the actuation signal ouput

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ActuationOutput",
	"payload": {
	    "property": "triggered",
	    "value": true
	}
}
```


### Expected SET Values

true, false

## Get Example

```
{
	"command": "get",
	"object": "ActuationOutput",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

true, false




# AFMAmplitudeSetPoint
<a name="afmamplitudesetpoint"></a>

## Description

Cantilever amplitude contact amplitude

## Set/Get Information

set / get

## Set Example

{
	"command": "set",
	"object": "AFMAmplitudeSetPoint",
	"payload": {
	    "property": "value",
	    "value": 0.521
	}
}

### Expected SET Values

floating-point value  

## Get Example

```
{
	"command": "get",
	"object": "AFMAmplitudeSetPoint",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

floating-point value  




# AFMPIDConstantI
<a name="afmpidconstanti"></a>

## Description

I constant in the Z PID controller

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "AFMPIDConstantI",
	"payload": {
	    "property": "value",
	    "value": 20
	}
}
```

### Expected SET Values

unsigned int

## Get Example

```
{
	"command": "get",
	"object": "AFMPIDConstantI",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int




# AFMPIDConstantP
<a name="afmpidconstantp"></a>

## Description

P constant in the Z PID controller

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "AFMPIDConstantP",
	"payload": {
	    "property": "value",
	    "value": 1000
	}
}
```

### Expected SET Values

unsigned int

## Get Example

```
{
	"command": "get",
	"object": "AFMPIDConstantP",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int


# APIEcho
<a name="apiecho"></a>

## Description

Send server echo response to the client

## Get Example

```
{
	"command": "get",
	"object": "APIEcho",
	"payload": {
	    "property": "hello world"
	}
}
```

### Expected Response

```
{
	"command": "response",
	"object": "APIEcho",
	"payload": {
	    "property": "hello world"
	}
}
```

The server replys with the same "property" value as received from the client.

## Notes

APIEcho command is available from AFM Control App v2.1.5

# APIVersion
<a name="apiversion"></a>

## Description

Manage API version

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "APIVersion",
	"payload": {
	    "property": "value",
	    "value": "1.0"
	}
}
```

### Expected SET Values

String values from the list of available server API versions

## Get Example

```
{
	"command": "get",
	"object": "APIVersion",
	"payload": {
	    "property": "value",
	    "value": "current"
	}
}
```

### Expected GET Values

String with a API version

## Notes

Use "current", "available" for the "value" field to get the corresponding data

Examplary response:

```
{
	"command": "get",
	"object": "APIVersion",
	"payload": {
	    "property": "value",
	    "value": "current"
	}
}
```



# authenticate
<a name="authenticate"></a>

## Description

Authenticate client for APIcommunication

## Set/Get Information

set

## Set Example

```
{
	"command": "authenticate",
	"apikey": "d1f89a72-3f0b-4d57-b3a9-0f7c63a2e914"
}
```

## Notes

Do not reveal the API-Key to unauthorized people!



# DataSubscription
<a name="datasubscription"></a>

## Description

Subscription to data steaming

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",	
	"object": "DataSubscription",
	"payload": {
	    "property": "type",
	    "type": "log",
	    "subscription": true
	}
}
```

### Expected SET Values

String values supported for property "type" are “line” (cross-section for each measured line) ,“map” (whole scanned area maps) or “log” (system log messages). 

## Get Example

```
{
	"command": "get",	
	"object": "DataSubscription",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

String “value” for "property". 

## Notes

An exemplary response for a client, who subscribed to “line” measurement for channels 0 and 1, and to the system log messages:

```
{
	"command": "response",	
	"object": "DataSubscription",
	"payload": {
	    "subscriptions": [
	        {
			"channel": 0,
			"format": "txt",
			"type": "line"
	        },
	        {
	            	"channel": 1,
			"format": "txt",
	            	"type": "line"
	        },
		{
			"format": "txt",
			"type": "log"
		}
	    ]
	}
}
```


"subscription": true subscribes to the data subscription system,   "subscription": false unsubscribes from the data subscription system.

When a clients requests a subscription to the system log, “channel” and “format” fields are ignored. 

For more information about the subscription to the measurement data, see .


# FoundResonanceProperties
<a name="foundresonanceproperties"></a>

## Description

Resonance parameters provided by the automatic sweep procedure.

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": " FoundResonanceProperties ",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

JSON structure with cantilever resonance parameters

## Notes

When after automatic frequency sweeping, a proper resonance is found, API returns the JSON structure as in this example:

```
{
	"command": "response",	
	"object": "FoundResonanceProperties",
	"payload": {
	    "Ivalue": 290,
	    "LITimeConstant_ms": 5.99708,
	    "Pvalue": 10,
	    "QFactor": 3926.04,
	    "peakBandwidth_Hz": 8.33739,
	    "resonanceAmplitude_V": 0.393794,
	    "resonanceFrequencyActuation_Hz": 32733.0,
	    "resonanceFrequencyVibration_Hz": 16366.5
	}
} 
```


When the probe actuation is set to half-Omega (see AFM user manual and   for reference) the actuation resonance frequency is a half of actual mechanical probe resonance frequency. Based on found probe’s resonance properties, AFM Control application proposes initial P ("Pvalue") and I ("Ivalue") constants for the control tip-sample feedback loop. "LITimeConstant\_ms" indicates proposed Lock-In amplifier time constant for balanced performance in terms of response speed and noise damping.  


# FrequencySweepStatus
<a name="frequencysweepstatus"></a>

## Description

Actuation frequency sweep status

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "FrequencySweepStatus",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

"Sweep", "Idle"

## Notes

"Sweep" = actuation frequency sweep in progress, "Idle"= AFM is not sweeping actuation frequency 




# MeasurementData
<a name="measurementdata"></a>

## Description

Get the scanned data from the buffer

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "MeasurementData",
	"payload": {
	    "property": "value",
	    "format": "txt",
	    "type": "image",
	    "channel": "0"
	}
}
```

### Expected GET Values

“format”: “txt ” – measurement map stored as ASCII text

“type”:  “image” – full measurement data including metadata and measurement map; “metadata” – metadata only; “map” – measurement map only  

“channel”: measurement data channel from 0 to MaxAvailableChannel -1

## Notes

The measurement data from the most recent completed measurement is transmitted via the API. The data structure consists of metadata, which describes the measurement conditions and settings, and the measurement data itself in an NxN matrix, where NxN represents the measurement resolution in pixels. The data format is very similar to Gwyddion files, with the key difference being that data points are transferred as ASCII values.

Please note that transferring full high-resolution images (above 256x256) may overload the WebSocket connection and cause instabilities in the Client-Server communication. In this case, it is recommended to use the subscription model to transmit measurement data in line by line (see  chapter for more information). 




# MeasurementDataActiveChannel
<a name="measurementdataactivechannel"></a>

## Description

Signal to display or transmit

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "MeasurementDataActiveChannel",
	"payload": {
	    "property": "index",
	    "value": 1,
	    "channel": "0"
	}
}
```

### Expected SET Values

unsigned int type as "value" in the SET command corresponding with the measurement channel set to extract data from

## Get Example

```
{
	"command": "get",
	"object": "MeasurementDataActiveChannel",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

Examplary response:

```
{
	"command": "response",
	"object": "MeasurementDataActiveChannel",
	"payload": {
	    "value": {
	        "index": 0,
	        "text": "topography"
	    }
	}
}
```

index 0 = "topography", index 1 = "phase"



# MeasurementDataCorrectionMode
<a name="measurementdatacorrectionmode"></a>

## Description

Line correction method

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "MeasurementDataCorrectionMode",
	"payload": {
	    "property": "index",
	    "value": 1,
	    "channel": "1"
	}
}
```

### Expected SET Values

unsigned int type as "value" in the SET command to set the corresponsdix index in the modes collection

## Get Example

```
{
	"command": "get",
	"object": "MeasurementDataCorrectionMode",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

index 0 = "none", index 1 = "line" correction, index 2 = "Plane", index 3 = "Paraboloid", index 4 = "Cubic surface"




# MeasurementDataDirectionMode
<a name="measurementdatadirectionmode"></a>

## Description

Forward or backward signal directon to display or transmit

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "MeasurementDataDirectionMode",
	"payload": {
	    "property": "index",
	    "value": "0",
	    "channel": "1"
	}
}
```

### Expected SET Values

unsigned int type as "value" in the SET command corresponding with the measurement channel set to extract data from

## Get Example

```
{
	"command": "get",
	"object": "MeasurementDataDirectionMode",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

Examplary response: 

```
{
	"command": "response",
	"object": "MeasurementDataDirectionMode",
	"payload": {
	    "value": {
	        "index": 0,
	        "text": "forward"
	    }
	}
}
```

index 0 = "forward", index 1 = "backward" direction

# MeasurementDataSubscription
<a name="measurementdatasubscription"></a>

## Description

Subscription to data steaming

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",	
	"object": "MeasurementDataSubscription",
	"payload": {
	    "property": "type",
	    "type": "line",
	    "format": "txt",
	    "channel": 0,
	    "subscription": true
	}
}
```

### Expected SET Values

String values supported for property "type" are “line” (cross-section for each measured line) and “map” (whole scanned area maps). "format" can be “float”, “txt” or “base64” coded in binary base64 format. “channel” contains int value between 0 and 3, where “channel” corresponds to the GUI data channel.  Channel 0 represents the main AFM measurement channel. 
“subscription” is a bool value. true means to subscribe, and false means to unsubscribe to the data channel.  

## Get Example

```
{
	"command": "get",	
	"object": "MeasurementDataSubscription",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

String “value” for "property". 

## Notes

An exemplary response for a client, who subscribed to “line” measurement for channels 0 and 1:

```
{
	"command": "response",	
	"object": "MeasurementDataSubscription",
	"payload": {
	    "subscriptions": [
	        {
	            	"channel": 0,
			"format": "txt",
	            	"type": "line"
	        },
	        {
	            	"channel": 1,
			"format": "txt",
	            	"type": "line"
	        }
	    ]
	}
}
```


Each line data response consists of the JSON structure as follows:

```
{
	"command": "response",	
	"object": "MeasurementDataSubscription",
	"payload": {
	    "channel": 0,
  		"format": "float",
	    "signal": "phase",
  		"type": "line",
	    "value": {
	        "x": [
	            0,
	            0.04093853011727333,
	            0.08187706023454666,
				...
			]
		}
	}
}
```


In the “value” structure, there are 3 sets of floating-point data for x ("x") position in µm, measured signals in forward ("y\_forward") and backward ("y\_backward") direction.  The length of each vector corresponds to the ScannerResolution setting; when set to 128x128, the data vector is 128 data-point long.  Property “y\_position” show the integer value of pixel position in Y direction. Y position pixel value is between 0 and scan resolution – 1. Due to the limited refresh rate of the scan lines, some measurement lines may be omitted for display, when scanning in high speed \> 2 lines/second, but they are recorded in the measurement data.  

When "format" is set to "txt", values are rounded to 5 digits after coma and sent as strings in scientific notation (e.g. 0.08283889… will be changed to "8.2839e-02").  When "format" is set to "base64", values are rounded to 5 digits after coma and sent base64 binary coded. 


# MeasurementStatus
<a name="measurementstatus"></a>

## Description

Get AFM scan state

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "MeasurementStatus",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

Measurement, Idle

## Notes

"Measurement" = measurement in progress, "Idle"= AFM is not measuring




# MotorApproachMode
<a name="motorapproachmode"></a>

## Description

Manual or auto approach method

## Set/Get Information

set / get

## Set Example

{
	"command": "set",
	"object": "MotorApproachMode",
	"payload": {
	    "property": "index",
	    "value": 0
	}
}

### Expected SET Values

unsigned int

## Get Example

```
{
	"command": "get",
	"object": "MotorApproachMode",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

index 0 = "manual" approach, index 1 = "auto, fast" approach




## MotorPosition

## Description

Return motor position with reliability status

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": " MotorPosition",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type in micrometers for "value", string value for “reliability” property (“reliable” or “unreliable”).

## Notes

Exemplary response for the position just after starting the application. In this case, similarly to the ScannerPosition, AFM system has not reached the tip-sample contact to determine the motor position as reliable. 

```
{
	"command": "response",
	"object": "MotorPosition",
	"payload": {
		"reference": "",
		"reliability": "unreliable",
		"value": 0
	}
}
```

# MotorPosition
<a name="motorposition"></a>

## Description

Coarse motor Z position

## Set/Get Information

get

## Get Example

```
{
    "command": "get",
    "object": "MotorPosition",
    "payload": {
        "property": "value"
    }
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

Exemplary response for the position just after starting the application. In this case, AFM system has not reached the tip-sample contact to determine the motor position as reliable. Therefore the "reliability" property is set to "unreliable"

```
{
    "command": "response",
    "object": "MotorPosition",
    "payload": {
        "reference": "",
        "reliability": "unreliable",
        "value": 0
    }
}
```


# MotorSpeed
<a name="motorspeed"></a>

## Description

Motor speed of the Z positioner

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "MotorSpeed",
	"payload": {
	    "property": "value",
	    "value": 500
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "MotorSpeed",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

Min value around 3.73 um/s (depends on the motor type), max value 1000 um/s




# MotorStatus
<a name="motorstatus"></a>

## Description

Return the motor status

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "MotorStatus",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

"None", "Stopped", "Retracting", "Approaching", "Approached", "Unknown"

## Notes

"None" when motor not available, "Stopped" when motor is not moving, "Retracting" when motor is retracting from the surface, "Approaching" when motor is approaching to the surface, "Approached" when the probe is in the contact with the surface, "Unknown" when state cannot be determined




# ScannerCenterX
<a name="scannercenterx"></a>

## Description

Scan centre in the x scanning direction

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerCenterX",
	"payload": {
	    "property": "value",
	    "value": 12.3456
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerCenterX",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response




# ScannerCenterY
<a name="scannercentery"></a>

## Description

Scan centre in the y scanning direction

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerCenterY",
	"payload": {
	    "property": "value",
	    "value": 7.6543
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerCenterY",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response




# ScannerDeflectionZ
<a name="scannerdeflectionz"></a>

## Description

Z piezo deflection

## Set/Get Information

get

## Get Example

```
{
	"command": "get",
	"object": "ScannerDeflectionZ",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

Floating point values between 0 and 100 percent




# ScannerLimitZ
<a name="scannerlimitz"></a>

## Description

Z piezo limit

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerLimitZ",
	"payload": {
	    "property": "value",
	    "value": 50.21
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerLimitZ",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

Floating point values between 0 and 100 percent




# ScannerLinesPerSecond
<a name="scannerlinespersecond"></a>

## Description

Lines per second

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerLinesPerSecond",
	"payload": {
	    "property": "value",
	    "value": 2.5
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerLinesPerSecond",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

The higher value, the faster measurement is carried out, but the quality of measurement data may be reduced. See the manual for more information. 




# ScannerMode
<a name="scannermode"></a>

## Description

Scan mode: 2D mapping or profile measurements.

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerMode",
	"payload": {
	    "property": "index",
	    "value": 1
	}
}
```

### Expected SET Values

unsigned int type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerMode",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

index = 0 = "Single scan" single 2D mapping scan; index = 1 = "Continuous scanning"; index = 2 = "Profile from navigation"; index = 3 = "Profile from scan". 

"Profile from navigation" takes the position of the profile from the current navigation position. "Profile from scan" takes the position of the profile from the given line number of the current scanner position in the "scan" mode.

# ScannerPosition
<a name="scannerposition"></a>

## Description

Return tip-sample distance with reliability status

## Set/Get Information

get

## Get Example


{
	"command": "get",
	"object": "ScannerPosition",
	"payload": {
	    "property": "value"
	}
}

### Expected GET Values

float type in micrometers for "value", string value for “reliability” property (“reliable” or “unreliable”).

## Notes

Exemplary response for the position just after starting the application. In this case, AFM system has not reached the tip-sample contact to determine the scanner position as reliable. 

```
{
	"command": "response",	
	"object": "ScannerPosition",
	"payload": {
	    "reliability": "unreliable",
	    "value": 8162.79
	}
}
```

# ScannerProfileLine
<a name="scannerprofileline"></a>

## Description

Selected line for profile measurement. The selected line is in range of 1 to the selected pixel resolution. 

## Set/Get Information

set / get

## Set Example

```
{
    "command": "set",
    "object": "ScannerProfileLine",
    "payload": {
        "property": "value",
        "value": 24
    }
}
```

### Expected SET Values

integet type as "value" in the SET command

## Get Example

```
{
    "command": "get",
    "object": "ScannerProfileLine",
    "payload": {
        "property": "value"
    }
}
```

### Expected GET Values

integer type as "value" in the GET response

## Notes

The maximum selected line is the resolution of the scanner. For example, if the selected scanner resolution is 256x256, the maximum selected line is 256. 


# ScannerProfileLineRepetition
<a name="scannerprofilelinerepetitions"></a>

## Description

Number of profile line repetitions. The maximum number of repetitions is in range of 1 to the selected pixel resolution. 

## Set/Get Information

set / get

## Set Example

```
{
    "command": "set",
    "object": "ScannerProfileLineRepetitions",
    "payload": {
        "property": "value",
        "value": 8
    }
}
```

### Expected SET Values

integet type as "value" in the SET command

## Get Example

```
{
    "command": "get",
    "object": "ScannerProfileLineLock",
    "payload": {
        "property": "value"
    }
}
```

### Expected GET Values

integer type as "value" in the GET response

## Notes

The maximum profile line repetition number is the resolution of the scanner. For example, if the selected scanner resolution is 256x256, the maximum repetitions are 256. 


# ScannerProfileLineLock
<a name="scannerprofilelinelock"></a>

## Description

Lock for the selected profile line. If this option is true, the selected profile line will be kept until new selected line is explicitly set. 

## Set/Get Information

set / get

## Set Example

```
{
    "command": "set",
    "object": "ScannerProfileLineLock",
    "payload": {
        "property": "state",
        "value": true
    }
}
```

### Expected SET Values

bool type (true, false) as "value" in the SET command

## Get Example

```
{
    "command": "get",
    "object": "ScannerProfileLineLock",
    "payload": {
        "property": "value"
    }
}
```

### Expected GET Values

bool type (true, false) as "value" in the GET response

## Notes

Selected profile line lock prevent from accidental selecting a line for profile measurement, and allows keeping the same selected line between several 2D mapping scans. 


# ScannerRange
<a name="scannerrange"></a>

## Description

Scan range

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerRange",
	"payload": {
	    "property": "value",
	    "value": 10.9977
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerRange",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response

## Notes

Range is limmited to the calibrated values stored in the ini file




# ScannerResolution
<a name="scannerresolution"></a>

## Description

Scanning resolution in pixels

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerResolution",
	"payload": {
	    "property": "index",
	    "value": 1
	}
}
```

### Expected SET Values

unsigned int type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerResolution",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

unsigned int for "index", string for "text"

## Notes

Exemplary response:

```
{
	"command": "response",
	"object": "ScannerResolution",
	"payload": {
	    "value": {
	        "index": 1,
	        "text": "128x128"
	    }
	}
}
```

The returned index is the position in the available resolution colletion and the corresponding resolution in pixels


# ScannerRotation
<a name="scannerrotation"></a>

## Description

Scan rotation value

## Set/Get Information

set / get

## Set Example

```
{
	"command": "set",
	"object": "ScannerRotation",
	"payload": {
	    "property": "value",
	    "value": 12.34
	}
}
```

### Expected SET Values

float type as "value" in the SET command

## Get Example

```
{
	"command": "get",
	"object": "ScannerRotation",
	"payload": {
	    "property": "value"
	}
}
```

### Expected GET Values

float type as "value" in the GET response
 
