//Skeleton Info

import std.mem;
struct skinposedata{
    char propertyname[80];
    u32 skinsegmentid;
    u32 unknown;
    char skinsegmentname[];
}[[name(propertyname)]];

struct skeletoninfo{
    char segmentname[256];
    char skeletonname[256];
    u32 jointsegmentid;
    u32 skinsegmentid;
    u32 skinposecount;//unsure
    u32 skinposeoffset;
    skinposedata @ skinposeoffset;
}[[name(skeletonname)]];

skeletoninfo skeletonSegment @ 0x00;