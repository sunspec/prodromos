OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=1E12885A-3211-44EE-8BEB-B8BFD061E4EF_ConfigD3407018-0FBE-4E1A-B55E-340C957BD1DF
  m10_signalGroupConfigList=1E12885A-3211-44EE-8BEB-B8BFD061E4EF_ConfigD3407018-0FBE-4E1A-B55E-340C957BD1DF/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=1E12885A-3211-44EE-8BEB-B8BFD061E4EF_ConfigD3407018-0FBE-4E1A-B55E-340C957BD1DF/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=430D9EC0-3A02-4112-9270-A115CB608458-default/SyncExchangerRegistry/3C7231C1-0987-4660-8352-F749F40DFDD0/1E12885A-3211-44EE-8BEB-B8BFD061E4EF_ConfigD3407018-0FBE-4E1A-B55E-340C957BD1DF/SignalGroupConfigList
      instance {
        guid=AD3D7C89-B290-446A-AFE7-ECD94C93B6A0
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
  parent=1E12885A-3211-44EE-8BEB-B8BFD061E4EF_ConfigD3407018-0FBE-4E1A-B55E-340C957BD1DF
}