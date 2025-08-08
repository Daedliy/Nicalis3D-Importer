//Prop Node Segment

struct meshid{
    u32 meshidoffs;
    u32 meshid @ meshidoffs;
};
struct transformdata{
    float scale_x;//Default:1
    float shear_yy;//Shear on Y axis, facing Y
    float shear_yz;//Shear on Y axis, facing Z
    float explode_x;//Breaks model on X axis
    float shear_xy;//Shear on X axis, facing Y
    float scale_y;//Default:1
    float shear_xx;//Shear on X axis, facing X
    float explode_y;//Breaks model on Y axis
    float shear_xz;//Shear on X axis, facing Z
    float shear_yx;//Shear on Y axis, facing X
    float scale_z;//Default:1
    float explode_z;//Breaks model on Z axis
    float move_x,move_y,move_z;//Position transforms
    float size;//Closer to 0 = Larger, Closer to 2 = Smaller
};
struct propnodeinfo{
    char segmentname [256];
    u32 nodeid;//seems always it's own ID
    u32 unknown1[2];//no notable changes when modified
    transformdata transformdata;
    float nodebboxminwidth,nodebboxminlength,nodebboxminheight;
    float nodebboxmaxwidth,nodebboxmaxlength,nodebboxmaxheight;
    float unknown2[2];//no notable changes when modified
    u32 meshidcount;//Mesh affected by propnode
    meshid meshid[meshidcount];
}[[name(segmentname)]];

propnodeinfo PropNodeSegment@0x0;