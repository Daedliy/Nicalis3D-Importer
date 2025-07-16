/*Nicalis3D -mesh segment pattern*/

#include <std/core.pat>
#include <std/io>
enum N3D_MdlTyp : u32{
    Actor = 33881,
    Prop = 32857,
};
struct N3D_ActrHdr{
    u32 header_count;
    u32 weight_count;
    u32 unknown; //has ALWAYS been 16, guess gets subtracted by offset2offset
    u32 offset2offset; //very bad and likely to break but hasnt yet
    padding[offset2offset -16]; //change -16 to unknown if it genuinely never changes
    u32 weight_offset;

};
struct N3D_MshHdr{
    char name[256];
    char unknown_related_to_node [28];
    N3D_MdlTyp model_type;//Prop or Actor
    u32 material_count;//how many materials do we have
    u32 vertx_count;
    u32 index_count;
    u32 material_offset;
    u32 index_offset;
    u32 vertx_offset;
    padding[16];
    u32 actor_header_offset; //offset for extended header
};
struct N3D_BnWghts{
    u8 weight;//afaik, one weight per vert
};
struct N3D_Indc{
    u16 index[3];
};
struct N3D_MtrlHdr{
    float unknown1,unknown2,unknown3;//set these as floats cause they dont make sense otherwise
    float unknown4,unknown5,unknown6;
    u32 material_face_count;
    u32 material_face_offset;
    u32 material_ID;
};
struct N3D_PrpDta{
    float vx,vy,vz; //vert
    u8 vcr,vcg,vcb;//RGB888 vertex color
    u8 unknown1;//assumed to be vertex color alpha, does nothing?
    float nx,ny,nz;//normal
    float u,v;//UVs
};
struct N3D_ActrDta{
    float vx,vy,vz; //vert
    u8 vcr,vcg,vcb;//RGB888 vertex color
    u8 unknown1;
    float nx,ny,nz;//normal
    float u,v;//UVs
    u8 bone_index;//should be no larger than bone count
    u8 unknown2,unknown3,unknown4; //unknown
};
struct N3D_Msh{
    N3D_MshHdr Header;
    N3D_MtrlHdr Material_Header [Header.material_count] @ Header.material_offset;
    if(Header.actor_header_offset != 0){
        N3D_ActrHdr Actor_Header @ Header.actor_header_offset;
        N3D_BnWghts Weights [Actor_Header.weight_count] @ Header.actor_header_offset+Actor_Header.weight_offset;
    }
    match(Header.model_type){
        (N3D_MdlTyp::Prop): N3D_PrpDta Data[Header.vertx_count] @ Header.vertx_offset;
        (N3D_MdlTyp::Actor): N3D_ActrDta Data[Header.vertx_count] @ Header.vertx_offset;
        (_): std::print("idk man neither types found");
    }
    N3D_Indc Indices [Header.index_count/3] @ Header.index_offset;
    std::print(Header.model_type);

}[[name(Header.name)]];
 
N3D_Msh Mesh @ 0x0;