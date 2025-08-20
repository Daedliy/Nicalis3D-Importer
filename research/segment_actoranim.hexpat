//Actor Animation Segment

import std.ptr;
fn relative_to_parent(u128 offset) {
    return addressof(parent.parent);
};

struct matrix44{
    float m11,m12,m13,m14,
          m21,m22,m23,m24,
          m31,m32,m33,m34,
          m41,m42,m43,m44;
}[[single_color]];

struct vec3{
    float x;
    float y;
    float z;
};
struct keyframe{
    char name[256];
    float unknown1;
    float unknown2;
    u32 unknown3;
    u32 unknown4;
    vec3* vec3 :u32[[pointer_base("relative_to_parent")]];;
};

struct keyframepointer{
    keyframe* keyframe : u32;
}[[name(keyframe.name)]];
struct animation{
    char segmentname[256];
    float unknown1;
    float unknown2;
    matrix44 unknownmatrix;
    float unknown3;//maybe ID?
    u32 keyframecount;//???
    u32 bonecount; //maybe
    u32 pointerarrayoffset;
    keyframepointer keyframe [keyframecount]@ pointerarrayoffset;

}[[name(segmentname)]];

animation ActorAnimSegment @ 0x00;