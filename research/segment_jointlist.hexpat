//Jointlist Segment

struct jointdata{
    char jointname[40];
    u32 jointmagic;
    u32 unknown[5];
    float unknownfloat[16];
    u32 jointparent;
}[[name(jointname)]];

struct jointlistinfo{
    u32 jointcount;
    u32 jointoffset;
    jointdata jointdata[jointcount]@jointoffset;
};
jointinfo jointListSegment @ 0x00;