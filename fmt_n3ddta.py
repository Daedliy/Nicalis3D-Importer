from inc_noesis import *
noesis.logPopup()
noesis.openDataViewer()
# Modified on 7/12/25 (6:45 PM)
# This is here so it's easier to recognize later versions
# without having to deal with version numbers

# Annie's not so unreadable code
def readUInt32(fp):
  return int.from_bytes(fp.read(4), byteorder='little', signed=False)

def readString(inputBytes): # reads null terminated string from bytes object
  output = ''
  for i in range(0, len(inputBytes)):
    if inputBytes[i] == 0:
      return output
    output += chr(inputBytes[i])
  return output

def getSegmentThatEndsWith(inputObject, endsWithString): # terrible bodge while I work out something better
  for attr, value in inputObject.items():
    if attr.endswith(endsWithString):
      return value  

# N3Dhdr Start
def getN3DSegments(basePath):
  outputData = {}
  with open(basePath+'.n3dhdr', 'rb') as hdrFilePointer:
    # Retrieve amount of segments in file, always starts at 0x100/256bytes
    hdrFilePointer.seek(256, 0)
    totalSegments = readUInt32(hdrFilePointer)

    dtaFilePointer = open(basePath+'.n3ddta', 'rb')
    objectHasSkeleton = False
    objectName = ''
    for segmentIndex in range(0, totalSegments):
      # Layout: ID (4 bytes), Offset (4 bytes), Length (4 bytes)
      segmentID = readUInt32(hdrFilePointer) # read ID from n3dhdr
      segmentOffset = readUInt32(hdrFilePointer) # read offset from n3dhdr
      segmentLength = readUInt32(hdrFilePointer) # read length from n3dhdr
      dtaFilePointer.seek(segmentOffset, 0)
      segmentData = dtaFilePointer.read(segmentLength) # read data from n3ddta

      segmentName = ''
      if segmentIndex == 0: # check if n3ddta has valid skeleton info
        objectName = readString(segmentData)
        skeletonName = readString(segmentData[256:])
        skinName = readString(segmentData[384:])
        if skeletonName.startswith(objectName) and skinName.startswith(objectName):
          objectHasSkeleton = True
        outputData['hasSkeleton'] = objectHasSkeleton

      if segmentIndex == 1 and objectHasSkeleton: # skeleton info offset starts with joint count
        segmentName = objectName + '-skeleton' # because of that, we need to name it manually
      else:
        segmentName = readString(segmentData) # if there's no skeleton data it starts with segment name

      outputData[segmentName] = {'offset': segmentOffset, 'length': segmentLength}
      #noesis.logOutput("Segment: '" + segmentName + "' ID: '" + str(segmentID)+"'\n") # prints segment names and their IDs

    hdrFilePointer.close()
    dtaFilePointer.close()
  return outputData
# End of Willow's unreadable garbage

def registerNoesisTypes():
  handle = noesis.register("Cave Story 3D Data",".n3ddta")
  noesis.setHandlerTypeCheck(handle, CheckType)
  noesis.setHandlerLoadModel(handle, LoadModel)  
  return 1
  
def CheckType(data):
  bs = NoeBitStream(data)
  return 1

def Align(bs, n):
  value = bs.tell() % n
  if (value):
    bs.seek(n - value, 1)

def LoadModel(data, mdlList):
  ctx = rapi.rpgCreateContext()
  rapi.setPreviewOption("drawAllModels","1") # sets Draw all models to 1 by default, both values must be strings
  bs = NoeBitStream(data)
  bs.setEndian(NOE_LITTLEENDIAN)

  currentFilePath = noesis.getSelectedFile()
  baseFilePath = currentFilePath[:-7]
  n3dSegments = getN3DSegments(baseFilePath)

  for name, value in n3dSegments.items():# even worse bodge, repeats for every section with -mesh in name and then the offset is used
    if name.endswith("-mesh"):
      #noesis.logOutput(name + "\n" + str(value) + "\n\n") #best looking formatting for navigating this nightmare right now
      rapi.rpgSetName(name)
      
      #mesh section header
      meshSectionOffset = value['offset'];
      bs.seek(meshSectionOffset+284) #data starts past 256bytes/0xFF, just skipping these prop -node related 28bytes 
      mshType, matCount, vCount, idxCount, matOffs, idxOffs, vOffs = bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt(),bs.readUInt()

      if mshType == 33881:
          vStride = 0x28
      elif mshType == 32857:
          vStride = 0x24
      else:
          noesis.doException("Unknown Model Type!")
      
      #extra header exclusive to actors
      bs.seek(meshSectionOffset+328) # this value is zero in props as far as i know 
      actOffs = bs.readUInt()
      # noesis.logOutput(str(actOffs))
      
      #vertices
      bs.seek(meshSectionOffset + vOffs)
      vBuffer = bs.readBytes(vCount * vStride)
      rapi.rpgClearBufferBinds()
      rapi.rpgBindPositionBufferOfs(vBuffer, noesis.RPGEODATA_FLOAT, vStride,0)#bytes for positions, dataType, stride
      rapi.rpgBindColorBufferOfs(vBuffer,noesis.RPGEODATA_UBYTE, vStride,0x0C,4)
      rapi.rpgBindNormalBufferOfs(vBuffer, noesis.RPGEODATA_FLOAT, vStride,0x10)
      rapi.rpgBindUV1BufferOfs(vBuffer, noesis.RPGEODATA_FLOAT, vStride,0x1C)
      if mshType == 3881:
        rapi.rpgBindBoneIndexBufferOfs(vBuffer, noesis.RPGEODATA_UBYTE, vStride,0x24, 0x1)
      
        wBuffer = b'x\FF' * vCount #create dummy wBuffer of weight 1 
        rapi.rpgBindBoneWeightBuffer(wBuffer, noesis.RPGEODATA_UBYTE, 0x1, 0x1) # boneweights bytes, data type, stride, weights per vert
      
      
      #material headers?
      for matCounter in range(matCount):
        matStride = matCounter * 0x24
        bs.seek(meshSectionOffset + matOffs + matStride)
        _,_,_,_,_,_,matFaceCount,matFaceOffset,matID = bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readFloat(),bs.readUInt(),bs.readUInt(),bs.readUInt()
        rapi.rpgSetMaterial(str(matID))# if a read material is the same name, only one material is created 

        #indices
        bs.seek(meshSectionOffset + idxOffs+matFaceOffset*2)
        idxBuffer = bs.readBytes(matFaceCount*2)
        rapi.rpgCommitTriangles(idxBuffer,noesis.RPGEODATA_USHORT, matFaceCount,noesis.RPGEO_TRIANGLE)
        noesis.logOutput("Material #"+str(matCounter+1) +" "+ str(matID)+"\n")
      
      if n3dSegments['hasSkeleton']:
        #jump to skel section, grab names and parenting info
        jointNames = []
        jointParents = []
        jointMatrices = []
        skeletonSegmentOffset = getSegmentThatEndsWith(n3dSegments, 'skeleton')['offset'];
        bs.seek(skeletonSegmentOffset)
        jointCount = bs.readUInt()
        unk = bs.readUInt()
        for i in range(jointCount):
          jointNames.append(bs.readString())
          Align(bs,4)
          #very annoying alignment going on, cheat and jump to 4 directly, seems consistent
          a = 0
          while(a - 4): 
            a = bs.readUInt()
          if i:#skip 0x70 bytes for root and 0x58 for others to jump to parent info directly.
            bs.seek(0x50,1)
          else:
            bs.seek(0x68,1) 
          jointParents.append(bs.readByte())
          Align(bs,4)
          
        #jump to bone bind transform section
        boneBindSegmentOffset = getSegmentThatEndsWith(n3dSegments, 'skin')['offset'];
        bs.seek(boneBindSegmentOffset+(256*3)+80)
        #bs.seek(0x17F0)
        for _ in range(jointCount):
          jointMatrices.append(NoeMat44.fromBytes(bs.readBytes(0x40)).toMat43().inverse())
        
        #we have all the bone info, constructing the skeleton
        jointList = []
        for i, (parent,name, mat) in enumerate(zip(jointParents,jointNames,jointMatrices)):
          joint = NoeBone(i, name, mat, None, parent)
          jointList.append(joint)
  
  try:
    mdl = rapi.rpgConstructModel()
  except:
    mdl = NoeModel()
  rapi.setPreviewOption("setAngOfs", "0 -90 0")
  if n3dSegments['hasSkeleton']:
    mdl.setBones(jointList)
  mdlList.append(mdl)
  
  return 1

  
# thank you @s0me0neelse. for your help with writing the very first version of this script with my AXE template 