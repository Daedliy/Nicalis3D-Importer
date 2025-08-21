#WIP Nicalis 3D importer

from inc_noesis import *
noesis.logPopup()
noesis.openDataViewer()

def registerNoesisTypes():
  handle = noesis.register("Nicalis 3D Data",".n3ddta")
  noesis.setHandlerTypeCheck(handle, n3dCheckType)
  noesis.setHandlerLoadModel(handle, n3dLoadModel)
  handle = noesis.register("Nicalis 3D Data",".n3dhdr")
  noesis.setHandlerTypeCheck(handle, n3dCheckType)
  noesis.setHandlerLoadModel(handle, n3dLoadModel)
  # noesis.addOption(handle, "option name", "option description", noesisflags (Do Later)
  return 1

def n3dCheckType(data):
  if rapi.checkFileExists(rapi.getExtensionlessName(rapi.getInputName()) + ".n3dhdr" ) == 0:
    print("Invalid file or header is missing")
    return 0
  return 1

def uInitString(bs,bufferSize): #Moves data pointer and returns string
  readString = bs.readString()
  stringLength = (len(readString))
  if (stringLength):
    bs.seek(bufferSize - stringLength -1, 1)
    return readString
  
def fetchSegmentsOfType(n3dSegmentDict,TYPE):#create smaller dict of desired type
  requestedSegments = {}
  for id in n3dSegmentDict:
    for k,v in n3dSegmentDict[id].items():
      if v == str(TYPE):
        requestedSegments.update({id:n3dSegmentDict.get(id)})
  return requestedSegments  

def getLevelDescriptor(n3dSegment,bs):
  for segmentID in n3dSegment: #Assign type to descriptor
    if segmentID == '2186838753': #This ID is consistent
      n3dSegment['2186838753']['type'] = 'LEVELDESC'
      print("Found level-descriptor, assigning segment types...")
      break

  bs.seek(n3dSegment['2186838753']['offset']+256)
  move_x1,move_y1,move_z1,move_x2,move_y2,move_z2,shadingtemp,shadingweight,_,_, = [bs.readFloat() for _ in range(10)]
  #Second entry in segmentTypes may just be extra space for propnodes (???)
  segmentTypes = ['PROPNODE','PROPNODE','LIGHT','TYPE4','ANIMPROPNODE','TEXTURE','MATERIAL','MESH','TYPE9','SKIN','ACTORNODE']
  for i in range (0,11):
    bitstreamoffset = 4*i
    bs.seek(n3dSegment['2186838753']['offset']+296+bitstreamoffset)
    typeCount = bs.readUInt()
    bs.seek(n3dSegment['2186838753']['offset']+296+bitstreamoffset+44)
    typeOffset = bs.readUInt()
    bs.seek(n3dSegment['2186838753']['offset']+typeOffset)
    for x in range (typeCount):
      currentType = segmentTypes[i]
      id = bs.readUInt()
      if n3dSegment.get(str(id)) != None:
        n3dSegment[str(id)].update({'type':str(currentType)})
      else:
        n3dSegment[str(id)] = {'name':'missingsegment','offset':0,'size':0,'type':'MISSING'}
  n3dSegment.pop('2186838753') # No need for the level-descriptor anymore, discard it.
  return

def getActorNode(bs,n3dSegment,origin):
  actorNode = fetchSegmentsOfType(n3dSegment,'ACTORNODE')
  if actorNode != {}:
    print("Found actornode, assigning segment types...")
    for k in actorNode.keys():
      bs.seek(actorNode[str(k)]['offset'])
      segmentName = uInitString(bs,256)
      skeletonName = uInitString(bs,256)
      jointSegmentID,skinSegmentID,_,animSubsectionOffset = [bs.readUInt() for _ in range(4)]#check on that third value later
      bs.seek(actorNode[str(k)]['offset']+animSubsectionOffset)
      animSubsectionName = uInitString(bs,64)
      animSubsectionSize,animCount,animIDOffset,animNamePointerOffset = [bs.readUInt() for _ in range(4)]
      n3dSegment[str(jointSegmentID)].update({'type':'JOINTLIST','origin':str(origin)})
    for i in range (animCount):
      bitstreamoffset = 4*i
      bs.seek(actorNode[str(k)]['offset']+animSubsectionOffset+animIDOffset+bitstreamoffset)
      animID = bs.readUInt()
      bs.seek(actorNode[str(k)]['offset']+animSubsectionOffset+animNamePointerOffset+bitstreamoffset)
      animNamePointer = bs.readUInt()
      bs.seek(actorNode[str(k)]['offset']+animSubsectionOffset+animNamePointer)
      animName = bs.readString()
      n3dSegment[str(animID)].update({'type':'ACTORANIM','index':str(i),'origin':str(origin)})
  else:
    return

def listN3DSegments(bs,bs2,origin):
  bs2.seek(256)
  segmentCount = bs2.readUInt()
  n3dSegmentData = {}
  n3dSegment = {}
  for segmentIndex in range(segmentCount):
    segmentID, segmentOffset, segmentSize = [bs2.readUInt() for _ in range(3)]
    bs.seek(segmentOffset)
    try:
      segmentName = bs.readString() 
    except:
      segmentName = "NO NAME / NOT UTF8 ENCODED"
    n3dSegmentData = {'name':segmentName,'offset':segmentOffset,'size':segmentSize,'type':'UNKNOWN'}
    n3dSegment.update({str(segmentID):n3dSegmentData})
  getLevelDescriptor(n3dSegment,bs)
  getActorNode(bs,n3dSegment,origin)
  for k,v in n3dSegment.items():
    print(k,v)
  return n3dSegment

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
      break
  bs.seek (propNodeSegments[PropNodeID]['offset'])
  propNodeName = uInitString(bs,256)
  selfID,_,_ = [bs.readUInt() for _ in range(3)]

  transformMatrix = NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43() # Transforms Mesh
  rapi.rpgSetTransform(transformMatrix)

def getMaterial(bs,materialID,materialSegments,textureSegments,texList,matList):
  #material
  for k in materialSegments.keys():
    bs.seek (materialSegments[str(materialID)]['offset'])
    materialName = uInitString(bs,256)
    textureID,_,_,_ = [bs.readUInt() for _ in range(4)]
    _,_,_,_,_,_,_,_,_,_,_ = [bs.readFloat() for _ in range(11)]
    materialBlendMode = bs.readUInt()
    rapi.rpgSetMaterial(materialName)# if materials share a name they are merged
  #texture
  if textureID != 0:
    for k in textureSegments.keys():
      bs.seek (textureSegments[str(textureID)]['offset'])
      textureName = uInitString(bs,36)
      texWidth,texHeight,texFormat,_,texBufferOffs = [bs.readUInt() for _ in range(5)]
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
  if materialBlendMode == 43: #Additive Blend Mode
    material.setBlendMode("GL_ONE","GL_ONE")
  elif materialBlendMode == 11: #Alpha Blend Mode, luminance too high?
    material.setBlendMode("GL_SRC_ALPHA","GL_ONE")
  matList.append(material)
  return 
    
def getSkeleton(bs,actorNodeSegments,skinSegments,jointListSegments,jointList):
  jointNames = []
  jointParents = []
  jointMatrices = []
  animList = {}
  for k in jointListSegments.keys():#TODO change logic to find via type
    if jointListSegments[str(k)]['origin'] == 'INTERNAL':
      bs.seek(jointListSegments[str(k)]['offset']) #no name string here, if only the other segments were as nice...
      jointCount,jointOffset = [bs.readUInt() for _ in range(2)]
      bs.seek(jointListSegments[str(k)]['offset']+jointOffset)
      for joint in range (jointCount):
        jointNames.append(uInitString(bs,40))
        jointMagic,_,_,_,_,_ = [bs.readUInt() for _ in range(6)]
        jointMatrix = (NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43().inverse()) #unsure what to do with this when skin matrix works fine
        jointParents.append(bs.readUInt())
        
  for k in skinSegments.keys():
    if skinSegments[str(k)]['type'] == 'SKIN':
      bs.seek(skinSegments[str(k)]['offset'])
      skinSegmentName = uInitString(bs,(256*3))
      skinSegmentMatrix = NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43() #transforms mesh before applying skel
      rapi.rpgSetTransform(skinSegmentMatrix)

      matrixCount,matrixOffset = [bs.readUInt() for _ in range(2)]
      bs.seek(skinSegments[str(k)]['offset']+matrixOffset)
      for _ in range(matrixCount):
        jointMatrices.append(NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43().inverse())
        
  for i, (parent,name,mat) in enumerate(zip(jointParents,jointNames,jointMatrices)): #construct skeleton
    joint = NoeBone(i,name,mat,None,parent)
    jointList.append(joint)
  
  return jointList

def getMesh(bs,n3dSegmentDict,mdlList):
  texList = []
  matList = []
  jointList = []
  meshSegments = fetchSegmentsOfType(n3dSegmentDict,'MESH')
  for meshID in meshSegments.keys():
    bs.seek (meshSegments[meshID]['offset'])
    meshSegmentName = uInitString(bs,256)
    rapi.rpgSetName(meshSegmentName)
    _,_,_,_,_,_,_ = [bs.readFloat() for _ in range(7)]
    meshType,submeshCount,vertexCount,indexCount,submeshOffset,indexOffset = [bs.readUInt() for _ in range(6)]
    vertexOffset,_,_,_,_,actorInfoOffset = [bs.readUInt() for _ in range(6)]
    if meshType == 33881:
      dataStride = 0x28
      actorNodeSegments = fetchSegmentsOfType(n3dSegmentDict,'ACTORNODE')
      if actorNodeSegments != {}:
        skinSegments = fetchSegmentsOfType(n3dSegmentDict,'SKIN')
        jointListSegments = fetchSegmentsOfType(n3dSegmentDict,'JOINTLIST')
        getSkeleton(bs,actorNodeSegments,skinSegments,jointListSegments,jointList)
      print("Loaded actor mesh: " + meshSegmentName)
    elif meshType == 32857:
      dataStride = 0x24
      propNodeSegments = fetchSegmentsOfType(n3dSegmentDict,'PROPNODE')
      getPropNode(bs,propNodeSegments,meshID)
      print("Loaded prop mesh: " + meshSegmentName)
    else:
      noesis.doException("Unknown mesh type!")
    
    #vertices
    bs.seek(meshSegments[meshID]['offset']+vertexOffset)
    vertexBuffer = bs.readBytes(vertexCount * dataStride)
    rapi.rpgClearBufferBinds()
    rapi.rpgBindPositionBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0)#bytes for positions, dataType, stride
    rapi.rpgBindColorBufferOfs(vertexBuffer,noesis.RPGEODATA_UBYTE, dataStride,0x0C,4)
    rapi.rpgBindNormalBufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0x10)
    rapi.rpgBindUV1BufferOfs(vertexBuffer, noesis.RPGEODATA_FLOAT, dataStride,0x1C)
    if meshType == 33881:
      rapi.rpgBindBoneIndexBufferOfs(vertexBuffer, noesis.RPGEODATA_UBYTE, dataStride,0x24, 0x1)
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset)
      unknownCount,boneWeightCount,offsetToUnknownOffset,offsetToBoneWeightOffset = [bs.readUInt() for _ in range(4)]
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset+offsetToBoneWeightOffset)
      boneWeightOffset = bs.readUInt()
      bs.seek (meshSegments[meshID]['offset']+actorInfoOffset+boneWeightOffset)
      boneWeightBuffer = bs.readBytes(boneWeightCount)
      rapi.rpgBindBoneWeightBuffer(boneWeightBuffer, noesis.RPGEODATA_UBYTE, 0x1, 0x1)#boneweights, datatype, stride, weights per-vert
      
    for submeshIndex in range(submeshCount):
      submeshStride = submeshIndex * 0x24
      bs.seek (meshSegments[meshID]['offset']+ submeshOffset + submeshStride)
      meshBBoxMinWidth,meshBBoxMinLength,meshBBoxMinHeight = [bs.readFloat() for _ in range(3)]
      meshBBoxMaxWidth,meshBBoxMaxLength,meshBBoxMaxHeight = [bs.readFloat() for _ in range(3)]
      submeshFaceCount,submeshFaceOffset,materialID = [bs.readUInt() for _ in range(3)]
      
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
  mdl.setBones(jointList)
  mdl.setModelMaterials(NoeModelMaterials(texList, matList))
  mdlList.append(mdl)
  return mdlList

def n3dLoadModel(data, mdlList):
  ctx = rapi.rpgCreateContext()
  
  #Load model regardless of paired file selected
  print("Found selected file "+ rapi.getInputName())
  if rapi.checkFileExt(rapi.getInputName(),".n3ddta") == 1:
    bs = NoeBitStream(data)
    headerFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".n3dhdr"
    if rapi.checkFileExists(headerFileName) !=0:
      data2 = rapi.loadIntoByteArray(headerFileName)
      print("Found model header file: "+ headerFileName)
      bs2 = NoeBitStream(data2)
    else:noesis.Noesis_DoException("Missing .n3dhdr file!")
  else:
    dataFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".n3ddta"
    bs2 = NoeBitStream(data)
    if rapi.checkFileExists(dataFileName) !=0:
      data2 = rapi.loadIntoByteArray(dataFileName)
      print("Found model data file: "+ dataFileName)
      bs = NoeBitStream(data2)
    else:noesis.Noesis_DoException("Missing .n3ddta file!")
  modelName = bs2.readString()
  print("Loading model: " + modelName)
  n3dSegmentDict = listN3DSegments(bs,bs2,'INTERNAL')#Fetch segment info and return a dict

  #Load External Animations
  animDataFileName = rapi.getDirForFilePath(rapi.getInputName()) + "anim\\anim" + modelName[3:] + ".n3ddta"
  animHeaderFileName = rapi.getDirForFilePath(rapi.getInputName()) + "anim\\anim" + modelName[3:] + ".n3dhdr"
  if rapi.checkFileExists(animDataFileName) !=0 and rapi.checkFileExists(animHeaderFileName) !=0:
    data3,data4 = rapi.loadIntoByteArray(animDataFileName),rapi.loadIntoByteArray(animHeaderFileName)
    bs3,bs4 = NoeBitStream(data3),NoeBitStream(data4)
    animFileName = bs4.readString()
    print("Found animation data file: "+ animDataFileName)
    print("Found animation header file: "+ animHeaderFileName)
    print("Animation file name: " + animFileName)
    animN3DSegmentDict = listN3DSegments(bs3,bs4,'EXTERNAL')
    n3dSegmentDict.update(animN3DSegmentDict)

  #Load External Material Animation 
  matAnimFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".mat" 
  if rapi.checkFileExists(matAnimFileName) !=0:
    data5 = rapi.loadIntoByteArray(matAnimFileName)
    bs5 = NoeBitStream(data5)
    print("Found material animation file: "+ matAnimFileName)

  #Load External Camera Info (???)
  camFileName = rapi.getExtensionlessName(rapi.getInputName()) + ".cam" 
  if rapi.checkFileExists(camFileName) !=0:
    data6 = rapi.loadIntoByteArray(camFileName)
    bs6 = NoeBitStream(data6)
    print("Found camera file: "+ camFileName)
  
  getMesh(bs,n3dSegmentDict,mdlList)
  noesis.logOutput("Model file: '"+str(modelName) +"' Loaded. "+"\n")
  
  return 1