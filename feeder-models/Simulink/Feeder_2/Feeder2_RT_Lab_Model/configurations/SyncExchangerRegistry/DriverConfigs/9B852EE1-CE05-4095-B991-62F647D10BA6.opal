OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=9B852EE1-CE05-4095-B991-62F647D10BA6_Config68B62BB7-59AC-4982-A6EE-01829FFEEB93
  m10_signalGroupConfigList=9B852EE1-CE05-4095-B991-62F647D10BA6_Config68B62BB7-59AC-4982-A6EE-01829FFEEB93/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=9B852EE1-CE05-4095-B991-62F647D10BA6_Config68B62BB7-59AC-4982-A6EE-01829FFEEB93/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=0F95A00E-06C4-41FE-9BCA-E82C9AF28C0D-default/SyncExchangerRegistry/E9319702-0DC4-4072-9969-9B5FBA559471/9B852EE1-CE05-4095-B991-62F647D10BA6_Config68B62BB7-59AC-4982-A6EE-01829FFEEB93/SignalGroupConfigList
      instance {
        guid=BFFBC1A0-BEFA-48D8-BC6F-8EBEE2C1A1A9
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
  parent=9B852EE1-CE05-4095-B991-62F647D10BA6_Config68B62BB7-59AC-4982-A6EE-01829FFEEB93
}