/* Decompiled observation, not original source. Go ABI/types incomplete. SHA256: 9cfe9837524fee120043fe52e61164bdb2bf70c47172970d84e3b7337659d895 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [16] recovered_18e77a0(int *param_1,undefined8 param_2,int param_3)

{
  ushort uVar1;
  int iVar2;
  undefined1 auVar3 [16];
  int *piVar4;
  ushort *puVar5;
  ushort *extraout_RAX;
  ushort *extraout_RAX_00;
  ushort *extraout_RAX_01;
  ushort *extraout_RAX_02;
  uint extraout_RCX;
  uint extraout_RCX_00;
  uint extraout_RCX_01;
  uint extraout_RCX_02;
  uint extraout_RCX_03;
  uint uVar6;
  undefined8 extraout_RCX_04;
  uint uVar7;
  uint extraout_RBX;
  uint uVar8;
  uint extraout_RBX_00;
  uint extraout_RBX_01;
  uint extraout_RBX_02;
  undefined8 extraout_RBX_03;
  undefined8 *puVar9;
  undefined8 uVar10;
  int extraout_R8;
  int *extraout_R11;
  int unaff_R14;
  bool bVar11;
  int *piStack0000000000000008;
  undefined8 uStack0000000000000010;
  int iStack0000000000000018;
  undefined8 uStack_40;
  undefined8 *puStack_38;
  ushort *puStack_30;
  undefined8 uStack_28;
  undefined *puStack_20;
  int iStack_18;
  undefined **ppuStack_10;
  
  piStack0000000000000008 = param_1;
  iStack0000000000000018 = param_3;
  uStack0000000000000010 = param_2;
  while (&uStack_40 <= *(undefined8 **)(unaff_R14 + 0x10)) {
    func_0x0047c9e0();
  }
  LOCK();
  bVar11 = *(sdword *)((int)piStack0000000000000008 + 0x34) == 0;
  if (bVar11) {
    *(sdword *)((int)piStack0000000000000008 + 0x34) = 1;
  }
  UNLOCK();
  if (!bVar11) {
    func_0x004a33c0((int)piStack0000000000000008 + 0x34);
  }
  puStack_20 = &UNK_01967440;
  iStack_18 = (int)piStack0000000000000008 + 0x34;
  ppuStack_10 = &puStack_20;
  uVar6 = piStack0000000000000008[10];
  puVar5 = (ushort *)piStack0000000000000008[8];
  uVar1 = *(ushort *)((int)piStack0000000000000008 + 0x16);
  puVar9 = *(undefined8 **)(*piStack0000000000000008 + 0x18);
  if (uVar6 < 0xc) {
    puStack_38 = *(undefined8 **)(*piStack0000000000000008 + 0x18);
    puVar5 = (ushort *)func_0x00479da0(puVar5,0xc,uVar6,0xc,&UNK_02b6edd8);
    puVar9 = puStack_38;
    uVar6 = extraout_RCX;
  }
  *puVar5 = uVar1 << 8 | uVar1 >> 8;
  *(undefined1 *)(puVar5 + 1) = 0x81;
  *(undefined1 *)((int)puVar5 + 3) = 0x80;
  puVar5[2] = 0x100;
  puVar5[3] = 0;
  puVar5[4] = 0;
  puVar5[5] = 0;
  iVar2 = puVar9[1];
  uVar8 = iVar2 + 0xc;
  uVar10 = *puVar9;
  if (uVar6 < uVar8) {
    uStack_28 = *puVar9;
    func_0x00479da0(puVar5,uVar8,uVar6,iVar2,&UNK_02b6edd8);
    puVar5 = extraout_RAX;
    uVar10 = uStack_28;
    uVar6 = extraout_RCX_00;
    uVar8 = extraout_RBX;
  }
  puStack_30 = puVar5;
  func_0x0047e9c0(puVar5 + 6,uVar10,iVar2);
  uVar8 = uVar8 + 4;
  puVar5 = puStack_30;
  if (uVar6 < uVar8) {
    func_0x00479da0(puStack_30,uVar8,uVar6,4,&UNK_02b6edd8);
    puVar5 = extraout_RAX_00;
    uVar6 = extraout_RCX_01;
    uVar8 = extraout_RBX_00;
  }
  *(undefined4 *)((uVar8 - 4) + (int)puVar5) = 0x1001000;
  uVar8 = uVar8 + 2;
  if (uVar6 < uVar8) {
    func_0x00479da0();
    puVar5 = extraout_RAX_01;
    uVar6 = extraout_RCX_02;
    uVar8 = extraout_RBX_01;
  }
  *(ushort *)((uVar8 - 2) + (int)puVar5) =
       (ushort)iStack0000000000000018 << 8 | (ushort)iStack0000000000000018 >> 8;
  uVar7 = uVar8 + iStack0000000000000018;
  if (uVar6 < uVar7) {
    func_0x00479da0(puVar5,uVar7,uVar6,iStack0000000000000018,&UNK_02b6edd8);
    puVar5 = extraout_RAX_02;
    uVar6 = extraout_RCX_03;
    uVar7 = extraout_RBX_02;
  }
  func_0x0047e9c0((int)puVar5 + uVar8,uStack0000000000000010,iStack0000000000000018);
  piVar4 = piStack0000000000000008;
  piStack0000000000000008[9] = uVar7;
  piStack0000000000000008[10] = uVar6;
  if (_DAT_02e18cd0 != 0) {
    func_0x0047e280();
    *extraout_R11 = (int)puVar5;
    extraout_R11[1] = extraout_R8;
  }
  piVar4[8] = (int)puVar5;
  func_0x008007c0(*(undefined8 *)*piVar4);
  uStack_40 = extraout_RCX_04;
  (*(code *)*ppuStack_10)();
  auVar3._8_8_ = uStack_40;
  auVar3._0_8_ = extraout_RBX_03;
  return auVar3;
}

