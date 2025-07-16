#include <std/io.pat>
enum ImageFormats : u32 {
  BGR565 = 4,
  ABGR4444 = 2,
};

bitfield BGR565 {
  b : 5;
  g : 6;
  r : 5;
} [[sealed, color(std::format("{:02X}{:02X}{:02X}", this.r << 3, this.g << 2, this.b << 3))]];

bitfield ABGR4444 {
  a : 4;
  b : 4;
  g : 4;
  r : 4;
} [[sealed, color(std::format("{:02X}{:02X}{:02X}", this.r << 4, this.g << 4, this.b << 4))]];

struct N3D_BmH{
u32 width;
u32 height;
u32 format;
u32 unknown;
u32 buffer_offset;
};

struct N3D_BmI{
char Name[36];
N3D_BmH Header;
match (Header.format){
(ImageFormats::ABGR4444):ABGR4444 Color[Header.width*Header.height] @ Header.buffer_offset;
(ImageFormats::BGR565): BGR565 Color[Header.width*Header.height] @ Header.buffer_offset;
}

}[[name(Name)]];
N3D_BmI N3D_Bitmap @ 0x0;