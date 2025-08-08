//Mesh Segment

enum modeltype:u32{
    Actor = 33881,
    Prop  = 32857,
};
//Prop Specific
struct propdata{
    float vx,vy,vz;//vertices positon
    u8 vcr,vcg,vcb;//vertex color RGB888 
    u8 unknown1;//not vertex color alpha?
    float nx,ny,nz;//normal
    float u,v;//UVs
};
//Actor Specific
struct actordata{
    float vx,vy,vz;//vertices positon
    u8 vcr,vcg,vcb;//vertex color RGB888 
    u8 unknown1;//not vertex color alpha?
    float nx,ny,nz;//normal
    float u,v;//UVs
    u8 boneindex;//should be no larger than bone count
    u8 unknown[3];
};

struct actorinfo{
    u32 unknowncount;//genuinely no idea what this data is for
    u32 boneweightscount; //u8
    u32 off2unknownoffs; //add to actorinfo off
    u32 off2weightsoffs; //add to actorinfo off
    //may need to be separate 
    u32 unknownoffs[unknowncount];//genuinely no idea what this data is for
    u32 boneweightsoffs; //add to actorinfo off, possibly array of size unknowncount +1
};

struct submeshinfo{
    float bboxminwidth,bboxminlength,bboxminheight;
    float bboxmaxwidth,bboxmaxlength,bboxmaxheight;
    u32 submeshfacecount;
    u32 submeshfaceoff;
    u32 materialid;
};

struct meshinfo{
    char name[256];
    float unknown1[7];//did not encounter any changes when modified
    modeltype modeltype;//Prop or Actor
    u32 submeshcount;
    u32 vertexcount;
    u32 indexcount;
    u32 submeshoff;
    u32 indexoff;
    u32 vertexoff;
    u32 unknown2[4];
    u32 actorinfooff;
};

struct mesh{
    meshinfo meshinfo;
    submeshinfo submeshinfo [meshinfo.submeshcount] @ meshinfo.submeshoff;
    
    if(meshinfo.actorinfooff != 0){
        actorinfo @ meshinfo.actorinfooff;
        u8 boneweights [actorinfo.boneweightscount] @ meshinfo.actorinfooff+actorinfo.boneweightsoffs;
    }
    
    match(meshinfo.modeltype){
        (modeltype::Prop):propdata propdata[meshinfo.vertexcount] @ meshinfo.vertexoff;
        (modeltype::Actor):actordata actordata[meshinfo.vertexcount] @ meshinfo.vertexoff;
        (_): std::print("unknown type found");
    }
    
    u16 index [meshinfo.indexcount] @ meshinfo.indexoff;
}[[name(meshinfo.name)]];
 
mesh MeshSegment @ 0x0;