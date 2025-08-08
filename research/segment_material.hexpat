//Material Segment

struct materialinfo{
    char segmentname [256];
    u32 textureid;
    u32 unknown1[3];
    float unknown2[11];
    u32 unknown3;
}[[name(segmentname)]];
materialinfo MaterialSegment @ 0x00;