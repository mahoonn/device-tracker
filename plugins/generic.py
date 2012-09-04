# -*- coding: utf-8 -*-
import subprocess, re

class Generic:
  ifIndexOID = ".1.3.6.1.2.1.2.2.1.1"
  ifDescriptionOID = ".1.3.6.1.2.1.2.2.1.2"
  ifTypeOID = ".1.3.6.1.2.1.2.2.1.3"
  ifMacOID = ".1.3.6.1.2.1.2.2.1.6"
  ifNameOID = ".1.3.6.1.2.1.31.1.1.1.1"
  ifAliasOID = ".1.3.6.1.2.1.31.1.1.1.18"
  ifSpeedOID =  ".1.3.6.1.2.1.2.2.1.5"
  ifMtuOID = ".1.3.6.1.2.1.2.2.1.5"

  deviceNameOID = ".1.3.6.1.2.1.1.5"
  deviceSystemOID = ".1.3.6.1.2.1.1.1"
  deviceLocationOID = ".1.3.6.1.2.1.1.6"
  
  interfaceTable = {}
  
  speeds = {"10000000":"10M", "100000000":"100M", "1000000000":"1G", "4294967295":"other"}
  
  ip = ""
  community = ""
  name=""
  system=""
  location=""
  
  def __init__(self, device, community):
    self.ip = device
    self.community = community
    self.name = self.getStrippedOIDKeyValueData(self.deviceNameOID)["0"]
    self.system = self.getStrippedOIDKeyValueData(self.deviceSystemOID)["0"]
    self.location = self.getStrippedOIDKeyValueData(self.deviceLocationOID)["0"]

  def getStrippedOIDKeyValueData(self, oid):
    args = ['snmpbulkwalk', '-v2c', '-OnQ', '-c', self.community, self.ip, oid]
    output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    pattern = oid.replace(".","\.")+"\."+"(\d+)\s+=\s+(.*)"
    output = output.replace("\r","")
    result = re.findall(pattern, output)
    print result
    data = {}
    for r in result:
      data[r[0]] = r[1].strip("\"").strip("\n")
    return data

  def getStrippedOIDKeyData(self, oid):
    args = ['snmpbulkwalk', '-v2c', '-OnQ', '-c', self.community, self.ip, oid]
    output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
    pattern = oid.replace(".","\.")+"\."+"(\d+)\s+="
    data = re.findall(pattern, output)
    return data

  def getIfIndexData(self):
    data = self.getStrippedOIDKeyData(self.ifIndexOID)
    return data

  def getIfNameData(self):
    data = self.getStrippedOIDKeyValueData(self.ifNameOID)
    for d in data.keys():
      data[d] = data[d].strip("\"")
    return data

  def buildInterfaceTable(self):
    ifIndexArray = self.getStrippedOIDKeyData(self.ifIndexOID)
    ifNameTable = self.getStrippedOIDKeyValueData(self.ifNameOID)
    ifAliasTable = self.getStrippedOIDKeyValueData(self.ifAliasOID)
    ifSpeedTable = self.getStrippedOIDKeyValueData(self.ifSpeedOID)
    
    for i in ifIndexArray:
      self.interfaceTable[i] = {"name":ifNameTable[i], "alias":ifAliasTable[i], "speed":self.speeds[ifSpeedTable[i]]}
    return self.interfaceTable


