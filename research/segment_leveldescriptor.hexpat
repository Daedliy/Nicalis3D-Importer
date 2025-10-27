//Level-Descriptor Segment

struct leveldescriptorInfo{
    char segmentName[256];
    float moveX,moveY,moveZ;//X+ -> right, Y+ -> down, Z+ -> forward
    float moveX2,moveY2,moveZ2;//Unsure, same as previous?
    float shadingTemp;// -1 for coolest, 1 for warmest
    float shadingWeight;//-1 for heaviest shading, 1 for fullbright
    float unknownFloat1; //Couldn't find any changes when tampered with
    float unknownFloat2; //Couldn't find any changes when tampered with
    u32 segmentTypeCount[11];//is always only 11 segment types
    u32 segmentTypeOffset[11];
    //Each segment is represented by their ID and listed by type here
    //Not every segment type is listed here, we are missing JOINTLIST, ACTORANIM, etc
    u32 PROPNODE1     [segmentTypeCount[0]]  @ segmentTypeOffset[0]; //May have unknown ids
    u32 PROPNODE2     [segmentTypeCount[1]]  @ segmentTypeOffset[1]; //Identical to PROPNODE1 (???)
    u32 LIGHT         [segmentTypeCount[2]]  @ segmentTypeOffset[2]; //Should only be in maps
    u32 TYPE4         [segmentTypeCount[3]]  @ segmentTypeOffset[3]; //Not encountered yet (?)
    u32 ANIMPROPNODE  [segmentTypeCount[4]]  @ segmentTypeOffset[4]; //Non-skeletal animations
    u32 TEXTURE       [segmentTypeCount[5]]  @ segmentTypeOffset[5]; //
    u32 MATERIAL      [segmentTypeCount[6]]  @ segmentTypeOffset[6]; //
    u32 MESH          [segmentTypeCount[7]]  @ segmentTypeOffset[7]; //May have unknown ids
    u32 TYPE9         [segmentTypeCount[8]]  @ segmentTypeOffset[8]; //Not encountered yet, possibly MESHES2 (?)
    u32 SKIN          [segmentTypeCount[9]]  @ segmentTypeOffset[9]; //Should just be one per-actor (?)
    u32 ACTORNODE     [segmentTypeCount[10]] @ segmentTypeOffset[10];//Should just be one per-actor (?)
    //remaining bytes are garbage (?)
}[[name(segmentName)]];

leveldescriptorInfo LevelDescriptorSegment @0x00;
//Segment ID is always 2186838753
/* TODO: 
*   Investigate differences in PROPNODE1 and PROPNODE2, i think it could be some limit of how many IDs can be listed
    per-type?

*   Investigate unknown IDs, they may have a relation to separate animation files

*   Investigate unknownFloat1 & unknownFloat2
*/