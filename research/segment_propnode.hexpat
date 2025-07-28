//Prop Node

struct mshID{
    u32 meshidoffs;
    u32 meshid @ meshidoffs;
};

struct smlNodeSegment{
    char segmentName [256];
    u32 selfID;
    padding[8];
    
    float scale_x;
    float shear_1;//left and right bbox faces shear y axis
    float shear_2;//left and right bbox faces shear on z axis
    float explode_x; //???
    float shear_3;//top and bottom bbox shear on x axis
    float scale_y;
    float shear_4;//top and bottom bbox faces shear on z axis
    float explode_y;//???
    float shear_5;//front and back bbox faces shear on x axis
    float shear_6;//front and back bbox faces shear on y axis
    float scale_z;
    float explode_z;//???
    float x,y,z;
    float scale;//default value 1
    float bboxminWidth,bboxminLength,bboxminHeight;
    float bboxmaxWidth2,bboxmaxLength2,bboxmaxHeight2;
    float unknown3, unknown4; //no notable changes when modified
    u32 meshcount;
    mshID meshID[meshcount];
}[[name(segmentName)]];

smlNodeSegment SmallNode@0x0;