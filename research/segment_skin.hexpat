//Skin Segment
import std.mem;
struct matrix44{
float a[16];
};

struct skininfo{
char segmentname[256*3];
matrix44 unknownmatrix;
u32 matrixcount;
u32 matrixoffset;
matrix44 jointmatrix[matrixcount]@ matrixoffset;
};

skininfo SkinSegment @ 0x00;