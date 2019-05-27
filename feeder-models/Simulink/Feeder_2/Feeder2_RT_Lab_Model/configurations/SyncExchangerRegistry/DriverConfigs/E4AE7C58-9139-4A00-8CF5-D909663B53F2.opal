OPAL-1.0 Object
DataLogger::Configuration {
  m00_usageMode=Basic
  m01_recordMode=Automatic
  m05_useRTCore=0
  m06_verbose=0
  m07_showDLTConsole=0
  m09_noDataLoss=0
  name=E4AE7C58-9139-4A00-8CF5-D909663B53F2_ConfigE299476A-6BAD-4777-8871-B92662B08071
  m10_signalGroupConfigList=E4AE7C58-9139-4A00-8CF5-D909663B53F2_ConfigE299476A-6BAD-4777-8871-B92662B08071/SignalGroupConfigList
  parent=/
}
IOConfigListMap<DataLogger::SignalGroupConfig> {
  resizable=1
  uiName=SIGNAL_GROUP_
  name=E4AE7C58-9139-4A00-8CF5-D909663B53F2_ConfigE299476A-6BAD-4777-8871-B92662B08071/SignalGroupConfigList
  items {
    item {
      IOConfigItem_id=SIGNAL_GROUP_1
      listParent=0F95A00E-06C4-41FE-9BCA-E82C9AF28C0D-default/SyncExchangerRegistry/028146A2-0237-428B-BC81-23385A85C3B1/E4AE7C58-9139-4A00-8CF5-D909663B53F2_ConfigE299476A-6BAD-4777-8871-B92662B08071/SignalGroupConfigList
      instance {
        guid=32D11256-BE82-4EB0-B5BD-5B2DF113FC5A
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
  parent=E4AE7C58-9139-4A00-8CF5-D909663B53F2_ConfigE299476A-6BAD-4777-8871-B92662B08071
}