//Prop Node Segment

struct meshids{
    u32 meshidoffs;
    u32 meshid @ meshidoffs;
};

struct matrix44{
    float m11,m12,m13,m14,//scale_x  shear_yy shear_yz explode_x
          m21,m22,m23,m24,//shear_xy scale_y  shear_xx explode_y
          m31,m32,m33,m34,//shear_xz shear_yx scale_z  explode_z
          m41,m42,m43,m44;//move_x   move_y   move_z   size
}[[single_color]];

struct propnodeinfo{
    char segmentname [256];
    u32 nodeid;//seems always it's own ID
    u32 unknown1[2];//no notable changes when modified
    matrix44 transformmatrix;
    float nodebboxminwidth,nodebboxminlength,nodebboxminheight;
    float nodebboxmaxwidth,nodebboxmaxlength,nodebboxmaxheight;
    float unknown2[2];//no notable changes when modified
    u32 meshidcount;//assuming many meshes can be affected by one node
    meshids meshids[meshidcount];//Mesh affected by propnode
}[[name(segmentname)]];

propnodeinfo PropNodeSegment@0x0;