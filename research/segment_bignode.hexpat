//Bignode?
struct subsgmnt{ //may be exactly 324 bytes large
    char subsegmentName[12]; //zero terminated, extra zeros may be problematic

}[[name(subsegmentName)]];

struct subsgmnt_info{
    u32 subsegmentOffset;
};
struct bigNodeSegmentHeader{
    char segmentName [256];
    float unknownfloats1 [18];
    u32 SmallNodeID;
    u32 subsegmentCount;
    u32 unknown2;
    u32 subsegmentInfoOffset;
    subsgmnt_info subsegmentInfo [subsegmentCount] @ subsegmentInfoOffset;
    subsgmnt Segments @ subsegmentInfo[0].subsegmentOffset;//set as for loop
    subsgmnt Segments2 @ subsegmentInfo[1].subsegmentOffset;
}[[name(segmentName)]];

bigNodeSegmentHeader BigNode@0x0;