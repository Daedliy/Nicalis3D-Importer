# Nicalis3D-Importer
With this WIP plugin, you can view and export Cave Story 3D `.n3d___` model files with [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91)

<details>
<summary>Screenshots</summary>
<img width="1920" height="985" alt="Noesis_yUCRjCNDcF" src="https://github.com/user-attachments/assets/1517c0ec-e6a4-41a4-8a5a-d1650d1a287b" />
<img width="1920" height="985" alt="Noesis_gmwfDiR9Wc" src="https://github.com/user-attachments/assets/2692f743-c557-4ea5-95f5-5e96ecb3c0d0" />
<img width="1920" height="985" alt="Noesis_GGTT7zfDdO" src="https://github.com/user-attachments/assets/d55b29e9-8ece-4528-a23b-7ed45c7aee01" />
<img width="1920" height="985" alt="Noesis_lFEZtlWzCq" src="https://github.com/user-attachments/assets/142d5222-86b2-4811-83ca-2b52af0c9c95" />
<img width="1920" height="985" alt="Noesis_zOsdyVDIym" src="https://github.com/user-attachments/assets/e5932fcd-020b-4875-972d-f043e40fc110" />
</details>

### Getting Started
- Download Noesis and place `fmt_n3d.py` in `\noesis___\plugins\python\`
- Dump romfs from your copy of Cave Story 3D with your 3DS emulator of choice
- Navigate to `\romfs\______________\data\stage3d\` and open any of the files with Noesis


### Reverse Engineering
ImHex patterns for segments of the file spec and notes [can be found here](https://github.com/Daedliy/cs3d_noesis/tree/main/research)

### Roadmap
- [x] Rewrite script to load all segments by ID
- [ ] Implement material & texture flags
- [ ] Implement bounding boxes
- [ ] Implement animations
  - [x] Actor Animations `\anim\_.n3d__`
  - [ ] Prop Animations `prop animation segment`
  - [ ] Animated Textures `.mat`
- [ ] Implement scene objects

### Tools used
- [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91)
- [ImHex](https://imhex.werwolv.net/)
- [Azahar](https://azahar-emu.org/pages/download/)
- [Cheat Engine](https://www.cheatengine.org/)
## Many Thanks To:
>> ``Joschka (@s0me0neelse.)``
>
> Wrote the first version of this script and has been an immense help answering all of my Noesis & reverse engineering questions.

>> ``Annie (@annie.bot)``
>
> Iterated on that first version of the script and is the reason this even exists at all.

>> ``The XeNTaX Discord Community & Rich Whitehouse``
>
> Motivating me to put the work in myself and for providing the resources for learning Noesis.
