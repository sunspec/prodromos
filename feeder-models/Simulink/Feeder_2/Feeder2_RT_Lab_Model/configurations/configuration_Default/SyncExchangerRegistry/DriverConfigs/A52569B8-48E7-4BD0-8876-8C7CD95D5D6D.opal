OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=A52569B8-48E7-4BD0-8876-8C7CD95D5D6D_Config597EFB58-719C-4391-9173-F47F5C6DDBA0
  m10_signalGroupConfigList=A52569B8-48E7-4BD0-8876-8C7CD95D5D6D_Config597EFB58-719C-4391-9173-F47F5C6DDBA0/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=A52569B8-48E7-4BD0-8876-8C7CD95D5D6D_Config597EFB58-719C-4391-9173-F47F5C6DDBA0/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=0F95A00E-06C4-41FE-9BCA-E82C9AF28C0D-default/SyncExchangerRegistry/27526F42-E14E-4BF7-AC5A-B17CC7D226B2/A52569B8-48E7-4BD0-8876-8C7CD95D5D6D_Config597EFB58-719C-4391-9173-F47F5C6DDBA0/SignalGroupConfigList
      instance {
        guid=F4178704-7DDD-415D-A78C-D24E72C7E9B6
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
  parent=A52569B8-48E7-4BD0-8876-8C7CD95D5D6D_Config597EFB58-719C-4391-9173-F47F5C6DDBA0
}