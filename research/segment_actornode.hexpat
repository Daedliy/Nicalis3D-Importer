//Actor Node Segment

import std.ptr;
fn relative_to_parent(u128 offset) {
    return addressof(parent.parent.parent);
};
struct animnames{//pointer to name string relative to animsubsegment
    char *animname[] : u32 [[pointer_base("relative_to_parent")]];
}[[name(animname)]];

struct animsubsegment{
    char subsegmentname[64];
    u32 subsegmentsize;
    u32 animcount;
    u32 animidsoffs;
    u32 off2animnameoffs;
    u32 animids[animcount] @ addressof(this)+animidsoffs;
    animnames animnames [animcount]@addressof(this)+off2animnameoffs;
}[[name(subsegmentname)]];

struct actorinfo{
    char segmentname[256];
    char skeletonname[256];
    u32 jointlistsegmentid;
    u32 skinsegmentid;
    u32 unknown;
    u32 animationsubsegmentoffset;
    animsubsegment animlist @ animationsubsegmentoffset;
}[[name(segmentname)]];

actorinfo ActorNodeSegment @ 0x00;