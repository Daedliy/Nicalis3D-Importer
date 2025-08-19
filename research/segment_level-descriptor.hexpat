//Level-Descriptor Segment
//segment id is consistantly 2186838753
struct leveldescriptorinfo{
    char segmentname[256];
    float move_x,move_y,move_z;// x+ ->right, y+ -> down, z+ -> forward
    float move_x2,move_y2,move_z2;//duplicates of movement transform?
    float shadingtemp;// -1 for coolest, 1 for warmest
    float shadingweight;//-1 for heaviest shading, 1 for fullbright
    float unknown[2]; //did not encounter any changes when modified
    u32 idcount[11];
    u32 idoffs[11];
    //segments, only 11 types exist
    u32 segmentids0  [idcount[0]] @ idoffs[0];//props, may have unknown ids
    u32 segmentids1  [idcount[1]] @ idoffs[1];//not encountered yet
    u32 segmentids2  [idcount[2]] @ idoffs[2];//Lights
    u32 segmentids3  [idcount[3]] @ idoffs[3];//not encountered yet
    u32 segmentids4  [idcount[4]] @ idoffs[4];//Prop Animations
    u32 segmentids5  [idcount[5]] @ idoffs[5];//Textures
    u32 segmentids6  [idcount[6]] @ idoffs[6];//Materials
    u32 segmentids7  [idcount[7]] @ idoffs[7];//Meshes, may have unknown ids
    u32 segmentids8  [idcount[8]] @ idoffs[8];//not encountered yet
    u32 segmentids9  [idcount[9]] @ idoffs[9];//Actor Skins
    u32 segmentids10 [idcount[10]] @ idoffs[10];//Actor Skeletons
    //last bytes left over may just be garbage
}[[name(segmentname)]];
leveldescriptorinfo LevelDescriptorSegment @0x00;