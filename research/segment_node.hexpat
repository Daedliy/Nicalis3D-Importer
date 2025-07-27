//Smallnode?

struct meshref{
    u32 meshID;
};

struct smlNodeSegment{
    char segmentName [256];
    u32 selfID;
    padding[8];
    float scaleX;//scales change position if xyz are 0 or not
    padding[20];
    float scaleY;
    padding[8];
    float scaleZ;
    padding[8];
   
    float x,y,z;
    float unknown2;
    float bboxminWidth,bboxminLength,bboxminHeight;
    float bboxmaxWidth2,bboxmaxLength2,bboxmaxHeight2;
    float unknown_floats2[2];
    u32 meshCount;
    u32 meshID_Offset;
    meshref somethingtodowithmesh [meshCount] @ meshID_Offset;
}[[name(segmentName)]];

smlNodeSegment SmallNode@0x0;