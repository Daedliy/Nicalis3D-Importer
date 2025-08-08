//Bitmap Segment
#include <std/io.pat>
enum pixelformat : u32 {
  bgr565 = 4,
  abgr4444 = 2,
};

bitfield bgr565 {
  b : 5;
  g : 6;
  r : 5;
} [[sealed, color(std::format("{:02X}{:02X}{:02X}", this.r << 3, this.g << 2, this.b << 3))]];

bitfield abgr4444 {
  a : 4;
  b : 4;
  g : 4;
  r : 4;
} [[sealed, color(std::format("{:02X}{:02X}{:02X}", this.r << 4, this.g << 4, this.b << 4))]];

struct bitmapinfo{
    char segmentname[36];
    u32 width;
    u32 height;
    u32 format;
    u32 unknown;
    u32 bufferoff;
    match (format){
        (pixelformat::abgr4444):abgr4444 color[width*height] @ bufferoff;
        (pixelformat::bgr565): bgr565 color[width*height] @ bufferoff;
    }
}[[name(segmentname)]];
bitmapinfo BitmapSegment @ 0x0;