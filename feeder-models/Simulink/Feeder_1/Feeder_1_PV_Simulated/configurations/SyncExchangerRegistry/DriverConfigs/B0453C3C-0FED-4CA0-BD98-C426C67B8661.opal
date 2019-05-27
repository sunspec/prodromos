OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=B0453C3C-0FED-4CA0-BD98-C426C67B8661_ConfigFDCEEF9F-BACC-42AE-BBDC-CEFE1C75CECE
  m10_signalGroupConfigList=B0453C3C-0FED-4CA0-BD98-C426C67B8661_ConfigFDCEEF9F-BACC-42AE-BBDC-CEFE1C75CECE/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=B0453C3C-0FED-4CA0-BD98-C426C67B8661_ConfigFDCEEF9F-BACC-42AE-BBDC-CEFE1C75CECE/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=430D9EC0-3A02-4112-9270-A115CB608458-default/SyncExchangerRegistry/B25F0988-29C3-4155-9E17-C273B2DB89C0/B0453C3C-0FED-4CA0-BD98-C426C67B8661_ConfigFDCEEF9F-BACC-42AE-BBDC-CEFE1C75CECE/SignalGroupConfigList
      instance {
        guid=32885A47-E890-4B53-B5E0-E58480327742
        m003_recordMode=Inherit
        m006_exportFormat=OPREC
        m007_fileAutoNaming=1
        m010_fileName=data
        m011_decimationRatio=1
        m021_fileLength=10
        m022_fileLengthUnits=Seconds
        m031_recordLength=1000
        m032_recordLengthUnits=Steps
        m11_showTriggerConfiguration=0
        m12_triggerReferenceValue=0
        m13_triggerMode=Normal
        m14_triggerFunction=Edge
        m15_triggerPolarity=Positive
        m18_preTriggerPercent=0
        m19_triggerHoldoff=0
        m35_enableSubFraming=1
        m36_subFrameSizeMillis=10
      }
    }
  }
  parent=B0453C3C-0FED-4CA0-BD98-C426C67B8661_ConfigFDCEEF9F-BACC-42AE-BBDC-CEFE1C75CECE
}