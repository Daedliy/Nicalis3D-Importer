//level-descriptor

struct lvldesc_info{
float unknown_float1,unknown_float2,unknown_float3,unknown_float4;
float unknown_float5,unknown_float6;
padding[16];
//this block counts how many of a type of segment is present with u32 ints
u32 idCount1,idCount2,idCount3,idCount4,idCount5,idCount6;
u32 idCount7,idCount8,idCount9,idCount10,idCount11;
//in-segment offsets likely, 
u32 idblockoffset1,idblockoffset2,idblockoffset3,idblockoffset4,idblockoffset5,idblockoffset6;
u32 idblockoffset7,idblockoffset8,idblockoffset9,idblockoffset10,idblockoffset11;

};

struct lvldesc_header{
char segmentName[256];
lvldesc_info data;
//often has IDs matching with those in the n3dhdr file, some are unknown
//make this into a function before pushing to git
u32 ID1 [data.idCount1] @ data.idblockoffset1;//smallnodes + unknowns
u32 ID2 [data.idCount2] @ data.idblockoffset2;
u32 ID3 [data.idCount3] @ data.idblockoffset3;
u32 ID4 [data.idCount4] @ data.idblockoffset4;
u32 ID5 [data.idCount5] @ data.idblockoffset5;//bignode segment IDs
u32 textureSegmentIDs [data.idCount6] @ data.idblockoffset6;
u32 materialSegmentIDs [data.idCount7] @ data.idblockoffset7;
u32 ID8 [data.idCount8] @ data.idblockoffset8;//mesh segment IDs + unknowns
u32 ID9 [data.idCount9] @ data.idblockoffset9;
u32 skinSegmentIDs [data.idCount10] @ data.idblockoffset10;
u32 skeletonSegmentIDs [data.idCount11] @ data.idblockoffset11;
//any extra data is likely to just be garbage information given that this may
//be another uninitiated array?
}[[name(segmentName)]];

lvldesc_header LevelDescriptor @0x00;