/* Test N3D loader for ImHex
Previous version was absurdly slow because ImHex doesnt handle copying data to sections
well, the original was convinient for a while but if people are looking at this then
i would rather consolidate the patterns together so they can make sense of it.

The header file will always be significantly smaller in comparison,so lets copy that 
into memory instead 
*/
import std.io;
import hex.provider;
import std.string;
import std.file;
import std.mem;

import * from n3d.segment_leveldescriptor as LevelDescriptor;
import * from n3d.segment_actornode as ActorNode;

fn getSegmentData(u32 size,auto section){
u8 sectionData[size]@0x00 in section;//size of the section
    for (u32 b=0,b<size,b+=1){//repeat by size, b must be u32 or will loop forever
        sectionData[b] = std::file::read(hdrHandle,1);//read byte by byte
    }
};

fn getSegmentOffset(u32 id){
    for (u8 a=0, a<segmentCount,a+=1){
        if (Segments[a].id == id){
            return Segments[a].offset;
        }
    }
};

struct segmentData{u32 id; u32 offset; u32 size;};//segment info struct from header 

//Get header file path
str dtaFilePath = hex::prv::get_information("file_path","");//includes name and ext
str getExt = hex::prv::get_information("file_extension","");//grab the ext
str hdrFilePath = std::string::replace(dtaFilePath,getExt,".n3dhdr");//replace ext

std::print("Data file: {}", dtaFilePath); //Print both file paths
std::print("Header file: {}", hdrFilePath);

//Opens header file, prompts the warning
std::file::Handle hdrHandle = std::file::open(hdrFilePath,std::file::Mode::Read);
str modelName = std::file::read(hdrHandle,256);//name from hdr file
std::print("Model name: {}", modelName);

//Create sections to pull header data from
std::mem::Section hdrSegmentCount = std::mem::create_section("Segment Count");//Create count section
getSegmentData(4, hdrSegmentCount);//copy from file to section
u32 segmentCount @ 0x00 in hdrSegmentCount;//place pattern in section
std::print("{} segments found.",segmentCount);//print count

std::mem::Section hdrSegmentData = std::mem::create_section("Segment Data");//Create count section
u32 hdrSegmentDataSize = 4 * 3 * segmentCount;//amount of bytes in header to copy
getSegmentData(hdrSegmentDataSize,hdrSegmentData);
segmentData Segments[hdrSegmentDataSize] @ 0 in hdrSegmentData;//place pattern in section

//We are done with the header, read from n3ddta file and find level descriptor.
u32 levelDescOffset = getSegmentOffset(2186838753);//level descriptor is always this ID
std::print("Found level descriptor");
LevelDescriptor leveldescriptor @ levelDescOffset;//Place level descriptor pattern

//Get ActorNode if present
u32 actorNodeOffset;
if (leveldescriptor.segmentTypeCount[10] != 0){
    std::print("Found actor node of ID:{}",leveldescriptor.ACTORNODE[0]);
    actorNodeOffset = getSegmentOffset(leveldescriptor.ACTORNODE[0]);
};
ActorNode actornode @ actorNodeOffset;