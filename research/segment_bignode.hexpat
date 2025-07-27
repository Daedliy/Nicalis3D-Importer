//Animation Node
struct animdata{
float start_x;
float start_y;
float start_z;

float end_x;
float end_y;
float end_z;
};

struct subsgmntheader{ 
    char subsegmentName[256];//i hate whoever kept doing this man
    float animationspeed;
    float animationdelay;
    u32 unknownvalue;
    u32 unknown2;
    u32 animoffset;
}[[name(subsegmentName)]];

struct subsgmnt_info{
    u32 subsegmentOffset;
};
struct bigNodeSegmentHeader{
    char segmentName [256];
    float animationspeed;//smaller values are slower
    float animationdelay;//time until anim replays, larger is slower
    float unknown[16];//reinvestigate after getting a better grasp
    
    u32 SmallNodeID;
    u32 subsegmentCount;
    u32 unknown2;
    u32 subsegmentInfoOffset;
    subsgmnt_info subsegmentInfo [subsegmentCount] @ subsegmentInfoOffset;
    subsgmntheader Segments @ subsegmentInfo[0].subsegmentOffset;//set as for loop
    animdata AnimationData @ Segments.animoffset+subsegmentInfo[0].subsegmentOffset;
    
    
    
    subsgmntheader Segments2 @ subsegmentInfo[1].subsegmentOffset;
}[[name(segmentName)]];

bigNodeSegmentHeader BigNode@0x0;