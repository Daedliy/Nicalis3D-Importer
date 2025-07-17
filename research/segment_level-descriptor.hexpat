#include <std/mem.pat>

struct lvldesc_info{
float unknown_float1,unknown_float2,unknown_float3,unknown_float4;
float unknown_float5,unknown_float6;
padding[16];
//really small values ranging from 0 to 4
u32 idIntCount1;
padding[16];
u32 idIntCount2,idIntCount3,idIntCount4;
padding[4];
u32 idIntCount5,idIntCount6,idblockoffset1;
padding[16];
//in-segment offsets likely, 
u32 idblockoffset2,idblockoffset3,idblockoffset4;
padding[4];
u32 idblockoffset5,idblockoffset6;
};

struct lvldesc_header{
char segmentName[256];
lvldesc_info data;
//often has IDs matching with those in the n3dhdr file, some are unknown
u32 ID1 [data.idIntCount1] @ data.idblockoffset1;
u32 ID2 [data.idIntCount2] @ data.idblockoffset2;
u32 ID3 [data.idIntCount3] @ data.idblockoffset3;
u32 ID4 [data.idIntCount4] @ data.idblockoffset4;
u32 ID5 [data.idIntCount5] @ data.idblockoffset5;
u32 ID6 [data.idIntCount6] @ data.idblockoffset6;
//no clue what these last ints are, may end in 40 02 40 02 or FF FF FF FF
}[[name(segmentName)]];

lvldesc_header LevelDescriptor @0x00;