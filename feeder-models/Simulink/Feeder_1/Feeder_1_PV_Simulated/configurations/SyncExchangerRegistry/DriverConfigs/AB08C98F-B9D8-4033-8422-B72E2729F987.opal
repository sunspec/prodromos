OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=AB08C98F-B9D8-4033-8422-B72E2729F987_Config2B29BF5A-DE06-4833-8CCA-624F1EB77EF0
  m10_signalGroupConfigList=AB08C98F-B9D8-4033-8422-B72E2729F987_Config2B29BF5A-DE06-4833-8CCA-624F1EB77EF0/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=AB08C98F-B9D8-4033-8422-B72E2729F987_Config2B29BF5A-DE06-4833-8CCA-624F1EB77EF0/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=430D9EC0-3A02-4112-9270-A115CB608458-default/SyncExchangerRegistry/396B76C1-EC1A-42A6-AF78-56B7886250E0/AB08C98F-B9D8-4033-8422-B72E2729F987_Config2B29BF5A-DE06-4833-8CCA-624F1EB77EF0/SignalGroupConfigList
      instance {
        guid=86E8A8C3-CE55-4E02-8392-17C28006F00A
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
  parent=AB08C98F-B9D8-4033-8422-B72E2729F987_Config2B29BF5A-DE06-4833-8CCA-624F1EB77EF0
}