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

def n3dCheckType(data):
  bs = NoeBitStream(data)
  return 1

def getLevelDescriptor(n3dSegment,bs):
  for segmentID in n3dSegment: #Assign type to descriptor
    if segmentID == '2186838753': #This ID is consistent
      noesis.logOutput("!!! LEVELDESC found "+"\n")
      n3dSegment['2186838753']['type'] = 'LEVELDESC'
      continue

  bs.seek(n3dSegment['2186838753']['offset']+256)
  move_x1,move_y1,move_z1 = bs.readFloat(),bs.readFloat(),bs.readFloat() # move transform
  move_x2,move_y2,move_z2 = bs.readFloat(),bs.readFloat(),bs.readFloat() # duplicate of move transform?
  shadingtemp,shadingweight,_,_, = bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat()
  
  segmentTypes = ['PROPNODE','PROPNODE2?','LIGHT','TYPE4','ANIMNODE','TEXTURE','MATERIAL','MESH','TYPE9','SKIN','SKELETON']
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
        noesis.logOutput(str(currentType)+" Found! \n")
      else:
        n3dSegment[str(id)] = {'name':'missingsegment','offset':0,'size':0,'type':'MISSING'}
        noesis.logOutput("!!! MISSING Found! \n")
  return
    
def listN3DSegments(bs,bs2):
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
  return n3dSegment

def fetchSegmentsOfType(n3dSegmentDict,TYPE):#create smaller dict of desired type
  requestedSegments = {}
  for id in n3dSegmentDict:
    for key, value in n3dSegmentDict[id].items():
      if value == str(TYPE):
        requestedSegments.update({id:n3dSegmentDict.get(id)})
  return requestedSegments

def getPropNode(bs,propNodeSegments,requestedID):
  PropNodeID = ''
  for id in propNodeSegments.keys(): # fetch corresponding node
    bs.seek (propNodeSegments[id]['offset']+364)
    propCount,propOffset = bs.readUInt(),bs.readUInt()#normally there is never more than one prop referenced in a propnode
    if propCount > 1:
      noesis.logOutput("!!! !!! !!! Prop Node Count higher than 1, investigate")
    bs.seek (propNodeSegments[id]['offset']+propOffset)
    targetID = bs.readUInt()
    if str(requestedID) == str(targetID):
      PropNodeID = str(id)
      continue
  bs.seek (propNodeSegments[PropNodeID]['offset'])
  propNodeName = bs.readString()
  bs.seek (propNodeSegments[PropNodeID]['offset']+256)
  selfID,_,_ = bs.readUInt(),bs.readUInt(),bs.readUInt()

  transformMatrix = NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43() # Transforms Mesh
  rapi.rpgSetTransform(transformMatrix)

def getMaterial(bs,materialID,materialSegments,textureSegments,texList,matList):
  #material
  for material,value in materialSegments.items():
    bs.seek (materialSegments[str(materialID)]['offset'])
    materialName = bs.readString()
    bs.seek (materialSegments[str(materialID)]['offset']+256)
    textureID = bs.readUInt()
    rapi.rpgSetMaterial(materialName)# if materials share a name they are merged
  #texture
  if textureID != 0:
    for texture, value in textureSegments.items():
      bs.seek (textureSegments[str(textureID)]['offset'])
      textureName = bs.readString()
      bs.seek (textureSegments[str(textureID)]['offset']+36)
      texWidth,texHeight,texFormat,_,texBufferOffs = bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt()
      if texFormat == 4:
        textureData = rapi.imageDecodeRaw(bs.readBytes(texWidth*texHeight*2),texWidth,texHeight,'b5g6r5')
      elif texFormat == 2:
        textureData = rapi.imageDecodeRaw(bs.readBytes(texWidth*texHeight*2),texWidth,texHeight,'a4b4g4r4')
      format = noesis.NOESISTEX_RGBA32
    
    texture = NoeTexture(str(textureName), texWidth, texHeight, textureData, format)
    texture.flags = noesis.NTEXFLAG_FILTER_NEAREST #Sets texture flag to nearest, put this somewhere else later
    texList.append(texture)
    material = NoeMaterial(str(materialName),str(textureName))
  else:
    material = NoeMaterial(str(materialName),None)
    noesis.logOutput("Material '"+str(materialName)+"' has no texture\n")
  #material.flags =
  matList.append(material)
  return 

def getMesh(bs,n3dSegmentDict,mdlList):
  texList = []
  matList = []
  meshSegments = fetchSegmentsOfType(n3dSegmentDict,'MESH')
  for meshID,value in meshSegments.items():
    bs.seek (meshSegments[meshID]['offset'])
    meshSegmentName = bs.readString()
    rapi.rpgSetName(meshSegmentName)
    bs.seek (meshSegments[meshID]['offset']+256)
    _,_,_,_,_,_,_ = bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat()
    modelType,submeshCount,vertexCount,indexCount,submeshOffset = bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt()
    indexOffset,vertexOffset,_,_,_,_ = bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt()
    actorInfoOffset = bs.readUInt()
    if modelType == 33881:
      dataStride = 0x28
      noesis.logOutput("MESH Type: Actor "+"\n")
    elif modelType == 32857:
      dataStride = 0x24
      propNodeSegments = fetchSegmentsOfType(n3dSegmentDict,'PROPNODE')
      getPropNode(bs,propNodeSegments,meshID)
      noesis.logOutput("MESH Type: Prop "+"\n")
    else:
      noesis.doException("Unknown MESH Type!")
    
    #vertices
    bs.seek(meshSegments[meshID]['offset']+vertexOffset)
    vertexBuffer = bs.readBytes(vertexCount * dataStride)
    rapi.rpgClearBufferBinds()
    rapi.rpgBindPositionBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0)#bytes for positions, dataType, stride
    rapi.rpgBindColorBufferOfs(vertexBuffer,noesis.RPGEODATA_UBYTE, dataStride,0x0C,4)
    rapi.rpgBindNormalBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0x10)
    rapi.rpgBindUV1BufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0x1C)
    if modelType == 33881:
      rapi.rpgBindBoneIndexBufferOfs(vertexBuffer, noesis.RPGEODATA_UBYTE, dataStride,0x24, 0x1)
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset)
      unknownCount,boneWeightCount,offsetToUnknownOffset,offsetToBoneWeightOffset = bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt()
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset+offsetToBoneWeightOffset)
      boneWeightOffset = bs.readUInt()
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset+boneWeightOffset)
      boneWeightBuffer = bs.readBytes(boneWeightCount)
      rapi.rpgBindBoneWeightBuffer(boneWeightBuffer, noesis.RPGEODATA_UBYTE, 0x1, 0x1)#boneweights, datatype, stride, weights per-vert
      
    for submeshIndex in range(submeshCount):
      submeshStride = submeshIndex * 0x24
      bs.seek (meshSegments[meshID]['offset']+ submeshOffset + submeshStride)
      meshBBoxMinWidth,meshBBoxMinLength,MeshBBoxMinHeight = bs.readFloat(),bs.readFloat(),bs.readFloat()
      meshBBoxMaxWidth,meshBBoxMaxLength,MeshBBoxMaxHeight = bs.readFloat(),bs.readFloat(),bs.readFloat()
      submeshFaceCount,submeshFaceOffset,materialID = bs.readUInt(),bs.readUInt(),bs.readUInt()
      
      materialSegments = fetchSegmentsOfType(n3dSegmentDict,'MATERIAL')
      textureSegments = fetchSegmentsOfType(n3dSegmentDict,'TEXTURE')
      if materialSegments != {}: #check if there are materials
        getMaterial(bs,materialID,materialSegments,textureSegments,texList,matList)
      
      #indices
      bs.seek (meshSegments[meshID]['offset']+ indexOffset+submeshFaceOffset*2)
      indexBuffer = bs.readBytes(submeshFaceCount*2)
      rapi.rpgCommitTriangles(indexBuffer,noesis.RPGEODATA_USHORT, submeshFaceCount,noesis.RPGEO_TRIANGLE)
      
  try:
    mdl = rapi.rpgConstructModel()
  except:
    mdl = NoeModel()
  mdl.setModelMaterials(NoeModelMaterials(texList, matList))
  mdlList.append(mdl)
  #is erroring out on some models, investigate
  #noesis.logOutput(str(vertexOffset)+"\n")
  return mdlList

def n3dLoadModel(data, mdlList):
  ctx = rapi.rpgCreateContext()
  bs = NoeBitStream(data)
  #Load Header and give it a bitstream
  headerFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".n3dhdr" 
  if rapi.checkFileExists(headerFileName):
    data2 = rapi.loadIntoByteArray(headerFileName)
  bs2 = NoeBitStream(data2)
  
  modelName = bs2.readString()
  n3dSegmentDict = listN3DSegments(bs,bs2)#Fetch segment info and return a dict
  getMesh(bs,n3dSegmentDict,mdlList)
  noesis.logOutput("Model file: '"+str(modelName) +"' Loaded. "+"\n")
  
  return 1