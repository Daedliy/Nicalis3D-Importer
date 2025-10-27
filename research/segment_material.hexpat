//Material Segment

enum materialmode : u32{
alphablend = 13,
normal = 14,
additive = 43,
alpha = 11,
};

bitfield matflags {
  alpha : 1;            //Enable texture opacity (takes priority over alphatest)
  cullbackfaces : 1;    //Disable two sided mesh faces
  solid : 1;            //Disables translucency
  unignorez : 1;        //Disable Ignore Z
  alphatest : 1;        //Enable binary texture opacity (alpha must be 0)
  additive : 1;         //Enable additive blending (alpha must be 1)
  subtractive : 1;      //Enable subtractive blending (alpha must be 1)
  unknownflag : 1;      //Probably some blend mode?
};
/*
Material documentation

Additive/Subtractive
    If set to 1 when alpha flag is 0, it will create an effect which blacks out any overlaid materials that arent
    transparent.
    If both are set to 1 they cancel eachother out
 */
struct materialinfo{
    char segmentname [256];
    u32 textureid;
    u32 unknown1[3];
    float unknown2[11];
    matflags flags;
}[[name(segmentname)]];

materialinfo MaterialSegment @ 0x00;