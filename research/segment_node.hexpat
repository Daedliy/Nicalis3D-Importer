//Smallnode?

struct meshref{
    u32 meshID;
};

struct smlNodeSegment{
    char segmentName [256];
    u32 selfID;
    padding[8];
    float scaleX;
    padding[20];
    float scaleY;
    padding[8];
    float scaleZ;
    padding[8];
   
    float x;
    float y;
    float z;
    float unknown2;
    float bboxWidth;
    float bboxLength;
    float bboxHeight;
    float bboxWidth2;
    float bboxLength2;
    float bboxHeight2;
    float unknown_floats2[2];
    u32 meshCount;
    u32 meshID_Offset;
    meshref somethingtodowithmesh [meshCount] @ meshID_Offset;
}[[name(segmentName)]];

smlNodeSegment SmallNode@0x0;