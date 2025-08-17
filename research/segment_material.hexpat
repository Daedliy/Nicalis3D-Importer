//Material Segment

enum materialmode : u32{
alphablend = 13,
normal = 14,
additive = 43,
};

struct materialinfo{
    char segmentname [256];
    u32 textureid;
    u32 unknown1[3];
    float unknown2[11];
    materialmode;
}[[name(segmentname)]];

materialinfo MaterialSegment @ 0x00;