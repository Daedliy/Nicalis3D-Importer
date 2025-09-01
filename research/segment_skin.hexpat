//Skin Segment

struct matrix44{
    float m11,m12,m13,m14,
          m21,m22,m23,m24,
          m31,m32,m33,m34,
          m41,m42,m43,m44;
}[[single_color]];

struct skininfo{
    char segmentname[256*3];
    matrix44 meshtransformmatrix;
    u32 matrixcount;
    u32 matrixoffset;
    matrix44 jointmatrix[matrixcount]@ matrixoffset;
    u32 unknown1;//likely some ID?
    u32 unknown2;//likely some ID?
};

skininfo SkinSegment @ 0x00;