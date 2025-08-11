#WIP Nicalis 3D importer

from inc_noesis import *
noesis.logPopup()
noesis.openDataViewer()

def registerNoesisTypes():
  handle = noesis.register("Nicalis 3D Data",".n3ddta")
  noesis.setHandlerTypeCheck(handle, n3dCheckType)
  noesis.setHandlerLoadModel(handle, n3dLoadModel)
  # noesis.addOption(handle, "option name", "option description", noesisflags (Do Later)
  return 1

def getLevelDescriptor(n3dSegment,bs):
  for id in n3dSegment: #Assign type to descriptor
    if id == '2186838753': #This ID is consistent
      noesis.logOutput("level-descriptor found "+"\n")
      n3dSegment['2186838753']['type'] = 'LEVEL_DESC'
      continue

  bs.seek(n3dSegment['2186838753']['offset']+256)
  move_x1,move_y1,move_z1 = bs.readFloat(),bs.readFloat(),bs.readFloat() # move transform
  move_x2,move_y2,move_z2 = bs.readFloat(),bs.readFloat(),bs.readFloat() # duplicate of move transform?
  shadingtemp,shadingweight,_,_, = bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat()
  
  segmentTypes = ['PROPNODE','TYPE2','LIGHT','TYPE4','ANIMNODE','TEXTURE','MATERIAL','MESH','TYPE9','SKIN','SKELETON']
  for i in range (0,11):
    bitstreamoffset = 4*i
    bs.seek(n3dSegment['2186838753']['offset']+296+bitstreamoffset)
    typeCount = bs.readUInt()
    bs.seek(n3dSegment['2186838753']['offset']+296+bitstreamoffset+44)
    typeOffset = bs.readUInt()
    bs.seek(n3dSegment['2186838753']['offset']+typeOffset)
    for x in range (0,typeCount):
      currentType = segmentTypes[i]
      id = bs.readUInt()
      if n3dSegment.get(str(id)) != None:
        n3dSegment[str(id)].update({'type':str(currentType)})
  return
    
 
def getN3DSegments(bs,bs2):
  bs2.seek(256)
  segmentCount = bs2.readUInt()
  n3dSegmentData = {}
  n3dSegment = {}
  for segmentIndex in range(segmentCount):
    segmentID, segmentOffset, segmentSize = bs2.readUInt(),bs2.readUInt(),bs2.readUInt()
    bs.seek(segmentOffset)
    segmentName = bs.readString()
    n3dSegmentData = {'name':segmentName,'offset':segmentOffset,'size':segmentSize,'type':'UNKNOWN'}
    n3dSegment.update({str(segmentID):n3dSegmentData})
  getLevelDescriptor(n3dSegment,bs)
  noesis.logOutput(str(n3dSegment.values()))
  return 

def n3dCheckType(data):
  bs = NoeBitStream(data)
  return 1

def n3dLoadModel(data, mdlList):
  ctx = rapi.rpgCreateContext()
  
  bs = NoeBitStream(data)
  #Load Header and give it a bitstream
  headerFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".n3dhdr" 
  if rapi.checkFileExists(headerFileName):
    data2 = rapi.loadIntoByteArray(headerFileName)
  bs2 = NoeBitStream(data2)
  
  modelName = bs2.readString()
  n3dSegments = getN3DSegments(bs,bs2)#Fetch segment info and return a dict
  noesis.logOutput("Model file: '"+str(modelName) +"' Loaded. "+"\n")
  return 1