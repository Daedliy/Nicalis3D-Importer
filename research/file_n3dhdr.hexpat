// Nicalis 3D Header
import std.io;
import std.file;
import std.string;
#include <std/mem.pat>
#pragma loop_limit 99999999
#pragma pattern_limit 99999999

struct segmentinfo {
u32 id;
u32 off;
u32 size;
}[[name(id)]];

struct headerinfo{
char modelname[while($[$]!=0)];
padding[1]; //0 terminated string
u32 segmentcount @ 0x100;
segmentinfo read_chunks [segmentcount] @ 0x104;
};

headerinfo Header @ 0x0;
//Start ImHex Segment loading
//file name
str datafile =
Header.modelname + ".n3ddta";
//stage 3d folder path
str stage3dpath =
"C:/Users/daeem/AppData/Roaming/Azahar/dump/romfs/000400000004A100/data/stage3d/";
//merge the two strings and print to verify
str fulldatafilepath = stage3dpath + datafile;

std::file::Handle n3ddta = std::file::open(fulldatafilepath,std::file::Mode::Read); //Read n3ddta
u32 datafileSize = std::file::size(n3ddta); //data file size
std::print(datafile + " Loaded.");

fn copystr2char (u8 chunk, auto contents, auto section){//copy chunk contents into section
    for (u32 b=0,b<Header.read_chunks[chunk].size,b+=1){
        section[b] = std::string::at(contents,b);
    }
    return section;//returns str as char
};

for (u8 a=0,a<Header.segmentcount,a+=1){//repeats per chunk according to header

    std::file::seek(n3ddta,Header.read_chunks[a].off);//set offset from header
    str chunkContent = std::file::read(n3ddta,Header.read_chunks[a].size);//read size from header
    
    std::mem::Section chunkSection = std::mem::create_section(chunkContent);//sections instead
    char sectiondata[Header.read_chunks[a].size] @ 0x00 in chunkSection; //sets size of section
    sectiondata = copystr2char(a,chunkContent, sectiondata);//places data into section
};