//Animation Node Segment

enum transform_magic : u32{
    Move = 12,
    Rotate = 780,
    //scale = ???, 
    //values in between will cause unpredictable results
};

struct animdata{//interpolates from point a to point b, then restarts at a
    float ax, ay, az, bx, by, bz;
};

struct subsegmentdata{
    char subsegmentname[256];//i hate whoever kept doing this man
    float animspeed;
    float animdelay;
    transform_magic;
    u32 unknown2;
    u32 animdataoff;
}[[name(subsegmentname)]];

struct animsubsegment{ 
    u32 subsegmentoff;
    subsegmentdata subsegmentData @ subsegmentoff;
    animdata animData @ subsegmentoff+subsegmentData.animdataoff;
};

struct animNodeSegment{
    char segmentName [256];
    float animspeed;//smaller values are slower
    float animadelay;//time until anim replays, larger is slower
    float unknownfloats[16];//reinvestigate further with cheatengine
    u32 propnodeid;
    u32 subsegmentcount;
    u32 unknown;
    u32 off2subsegmentoffs;
    animsubsegment animSubsegment[subsegmentcount]@ off2subsegmentoffs;
}[[name(segmentName)]];

animNodeSegment AnimationNode@0x0;