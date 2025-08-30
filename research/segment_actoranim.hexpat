//Actor Animation Segment

import std.io;
struct matrix44{
    float m11,m12,m13,m14,
          m21,m22,m23,m24,
          m31,m32,m33,m34,
          m41,m42,m43,m44;
}[[single_color]];

fn format_vec(ref auto vec) {
    return std::format("Vec({}, {}, {})", vec.x, vec.z, vec.y);
};
struct vec3{
float x,z,y;//facing model, right is X+, backwards is Z+, up is Y+
}[[static, sealed, format("format_vec")]];

struct keyframes{ //i dont know
    float keyframe_timestamps[parent.transformsize];
    vec3 keyframe_values[parent.transformsize];
};

struct animtransform{
    char currentbone[256];
    float tranformlengthstart;
    float tranformlengthend;
    u32 transformunknown3;//increments as animation goes on
    u32 transformmagic;
    u32 transformsize = transformmagic - 18087936; //accounts for any size
    u32 vec3pointer;
    keyframes keyframes;
}[[inline]];

struct animtranspointer{//scale? //pos //rotation?
    animtransform* animtransform : u32[[inline]];
}[[name(animtransform.bonename)]];

struct animation{
    char segmentname[256];
    float animlengthstart;//unsure
    float animlengthend;//unsure
    matrix44 unknownmatrix;
    u32 selfid;
    u32 animtransformcount;
    u32 boneindex;
    u32 pointerarrayoffset;
    animtranspointer animtransforms [animtransformcount]@ pointerarrayoffset;

}[[name(segmentname)]];

animation ActorAnimSegment @ 0x00;