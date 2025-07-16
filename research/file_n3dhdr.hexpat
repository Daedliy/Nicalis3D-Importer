// Nicalis 3D File
import std.io;
import std.file;
import std.string;
#include <std/mem.pat>
#pragma loop_limit 99999999
#pragma pattern_limit 99999999

struct chunkinfo {
u32 ID;
u32 offset;
u32 size;
}[[name(ID)]];

struct n3dheader{
char model_name[while($[$]!=0)];
padding[1]; //0 terminated string
u32 segment_count @ 0x100;
chunkinfo read_chunks [segment_count] @ 0x104;
};

n3dheader N3D @ 0x0;

// file name
str datafile =
N3D.model_name + ".n3ddta";
// stage 3d folder path
str stage3d_path =
"C:/Users/daeem/AppData/Roaming/Azahar/dump/romfs/000400000004A100/data/stage3d/";
//merge the two strings and print to verify
str full_datafile_path =
stage3d_path + datafile;

std::file::Handle n3ddta = std::file::open(full_datafile_path,std::file::Mode::Read); //Read n3ddta
u32 datafileSize = std::file::size(n3ddta); //data file size
std::print(datafile + " Loaded.");

fn copy_str2char (u8 chunk, auto contents, auto section){//copy chunk contents into section
    for (u32 b=0,b<N3D.read_chunks[chunk].size,b+=1){
        section[b] = std::string::at(contents,b);
    }
    return section;//returns str as char
};

for (u8 a=0,a<N3D.segment_count,a+=1){//repeats per chunk according to header

    std::file::seek(n3ddta,N3D.read_chunks[a].offset);//set offset from header
    str chunkContent = std::file::read(n3ddta,N3D.read_chunks[a].size);//read size from header
    
    std::mem::Section chunkSection = std::mem::create_section(chunkContent);//sections instead
    char sectionData[N3D.read_chunks[a].size] @ 0x00 in chunkSection; //sets size of section
    sectionData = copy_str2char(a,chunkContent, sectionData);//places data into section
};