//level-descriptor
struct lvldesc_header{
    char segmentname     [256];
    float offsetx, offsety, offsetz;// x+ ->right, y+ -> down, z+ -> forward
    float offsetx2, offsety2,offsetz2;
    float colortemp;// -1 for coolest, 1 for warmest
    float shadingweight;//-1 for heaviest shading, 1 for fullbright
    float unknown[2]; //did not encounter any changes when modified
    //segments, only 11 types exist
    u32 idcount          [11];
    u32 idoffset         [11];
    u32 PropNodeSegmentIDs [idcount[0]] @ idoffset[0];//props, may have unknown ids
    u32 ID2                [idcount[1]] @ idoffset[1];//not encountered yet
    u32 LightSegmentIDs    [idcount[2]] @ idoffset[2];//exclusive to maps?
    u32 ID4                [idcount[3]] @ idoffset[3];//not encountered yet
    u32 AnimNodeSegmentIDs [idcount[4]] @ idoffset[4];//prop animation nodes?
    u32 TextureSegmentIDs  [idcount[5]] @ idoffset[5];
    u32 MaterialSegmentIDs [idcount[6]] @ idoffset[6];
    u32 MeshSegmentIDs     [idcount[7]] @ idoffset[7];//may have unknown ids
    u32 ID9                [idcount[8]] @ idoffset[8];//not encountered yet
    u32 SkinSegmentIDs     [idcount[9]] @ idoffset[9];//actors, skin info for skeleton
    u32 SkeletonSegmentIDs [idcount[10]] @ idoffset[10];//actors, bone info for skeleton 
    
    //last bytes left over may just be garbage?
}[[name(segmentName)]];

lvldesc_header LevelDescriptor @0x00;