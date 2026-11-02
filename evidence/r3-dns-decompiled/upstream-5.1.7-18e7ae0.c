/* Decompiled observation, not original source. Go ABI/types incomplete. SHA256: 9cfe9837524fee120043fe52e61164bdb2bf70c47172970d84e3b7337659d895 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [24] recovered_18e7ae0(int *param_1,undefined8 *param_2,uint param_3)

{
  ushort uVar1;
  undefined1 auVar2 [24];
  int iVar3;
  uint uVar4;
  ushort *puVar5;
  ushort *extraout_RAX;
  ushort *extraout_RAX_00;
  ushort *extraout_RAX_01;
  ushort *extraout_RAX_02;
  undefined8 *puVar6;
  uint uVar8;
  uint extraout_RCX;
  uint extraout_RCX_00;
  uint extraout_RCX_01;
  uint extraout_RCX_02;
  uint extraout_RCX_03;
  undefined8 extraout_RCX_04;
  int *piVar9;
  uint uVar10;
  undefined1 auVar7 [24];
  uint extraout_RBX;
  uint uVar11;
  uint extraout_RBX_00;
  uint extraout_RBX_01;
  uint extraout_RBX_02;
  undefined8 extraout_RBX_03;
  int *extraout_RSI;
  int iVar12;
  uint extraout_RDI;
  int extraout_R8;
  undefined8 *puVar13;
  undefined8 uVar14;
  int extraout_R8_00;
  int extraout_R9;
  int extraout_R10;
  int *extraout_R11;
  int *extraout_R11_00;
  undefined8 *extraout_R11_01;
  int unaff_R14;
  bool bVar15;
  undefined8 in_XMM15_Qa;
  undefined8 in_XMM15_Qb;
  int *piStack0000000000000008;
  undefined8 *puStack0000000000000010;
  uint uStack0000000000000018;
  int iStack_78;
  int iStack_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  ushort *puStack_58;
  undefined8 uStack_50;
  undefined8 *puStack_48;
  ushort *puStack_40;
  undefined8 uStack_38;
  undefined8 *puStack_30;
  undefined *puStack_28;
  int iStack_20;
  undefined8 *puStack_18;
  undefined **ppuStack_10;
  
  piStack0000000000000008 = param_1;
  uStack0000000000000018 = param_3;
  puStack0000000000000010 = param_2;
  while (&iStack_78 <= *(int **)(unaff_R14 + 0x10)) {
    func_0x0047c9e0();
  }
  LOCK();
  bVar15 = *(sdword *)((int)piStack0000000000000008 + 0x34) == 0;
  if (bVar15) {
    *(sdword *)((int)piStack0000000000000008 + 0x34) = 1;
  }
  UNLOCK();
  uStack_68 = in_XMM15_Qa;
  uStack_60 = in_XMM15_Qb;
  if (!bVar15) {
    func_0x004a33c0((int)piStack0000000000000008 + 0x34);
  }
  puStack_28 = &UNK_01967580;
  iStack_20 = (int)piStack0000000000000008 + 0x34;
  ppuStack_10 = &puStack_28;
  uVar8 = uStack0000000000000018;
  piVar9 = piStack0000000000000008;
  if (piStack0000000000000008[0xd] < (int)uStack0000000000000018) {
    iVar3 = func_0x00479cc0(&UNK_02b1f890,uStack0000000000000018);
    uVar8 = uStack0000000000000018;
    piStack0000000000000008[0xc] = uStack0000000000000018;
    piStack0000000000000008[0xd] = uStack0000000000000018;
    piVar9 = piStack0000000000000008;
    if (_DAT_02e18cd0 != 0) {
      iVar3 = func_0x0047e280();
      *extraout_R11 = iVar3;
      extraout_R11[1] = extraout_R8;
      piVar9 = extraout_RSI;
    }
    piVar9[0xb] = iVar3;
  }
  if (uVar8 <= (uint)piVar9[0xd]) {
    piVar9[0xc] = uVar8;
    uVar4 = 0;
    puVar6 = puStack0000000000000010;
    while( true ) {
      if ((int)uVar8 <= (int)uVar4) {
        puStack_18 = (undefined8 *)func_0x0041e9a0(&UNK_02b6ef98);
        puVar6 = (undefined8 *)func_0x0041f5c0(0x18,&UNK_02be1d88,1);
        *puVar6 = &UNK_01967480;
        if (_DAT_02e18cd0 != 0) {
          puVar6 = (undefined8 *)func_0x0047e280();
          *extraout_R11_01 = puStack_18;
          extraout_R11_01[1] = piStack0000000000000008;
        }
        puVar6[1] = puStack_18;
        puVar6[2] = piStack0000000000000008;
        recovered_18e4f80(*(undefined8 *)(*piStack0000000000000008 + 8),
                          *(undefined8 *)(*piStack0000000000000008 + 0x10),puVar6);
        uVar14 = *puStack_18;
        uStack_68 = extraout_RBX_03;
        uStack_60 = extraout_RCX_04;
        (*(code *)*ppuStack_10)();
        auVar7._8_8_ = uStack_68;
        auVar7._0_8_ = uVar14;
        auVar7._16_8_ = uStack_60;
        return auVar7;
      }
      iVar3 = puVar6[1];
      if ((uint)piVar9[0xc] <= uVar4) break;
      iStack_70 = uVar4 * 3;
      uVar8 = *(uint *)(piVar9[0xb] + 0x10 + uVar4 * 0x18);
      puVar5 = *(ushort **)(piVar9[0xb] + uVar4 * 0x18);
      uVar1 = *(ushort *)((int)piVar9 + 0x16);
      puVar13 = *(undefined8 **)(*piVar9 + 0x18);
      uStack_50 = *puVar6;
      puStack_30 = puVar6;
      if (uVar8 < 0xc) {
        puStack_48 = *(undefined8 **)(*piVar9 + 0x18);
        puVar5 = (ushort *)func_0x00479da0(puVar5,0xc,uVar8,0xc,&UNK_02b6edd8);
        puVar13 = puStack_48;
        uVar8 = extraout_RCX;
      }
      *puVar5 = uVar1 << 8 | uVar1 >> 8;
      *(undefined1 *)(puVar5 + 1) = 0x81;
      *(undefined1 *)((int)puVar5 + 3) = 0x80;
      puVar5[2] = 0x100;
      puVar5[3] = 0;
      puVar5[4] = 0;
      puVar5[5] = 0;
      iVar12 = puVar13[1];
      uVar11 = iVar12 + 0xc;
      uVar14 = *puVar13;
      if (uVar8 < uVar11) {
        iStack_78 = iVar12;
        uStack_38 = uVar14;
        func_0x00479da0(puVar5,uVar11,uVar8,iVar12,&UNK_02b6edd8,uVar14,iVar3,uStack_50);
        iVar12 = iStack_78;
        uVar14 = uStack_38;
        puVar5 = extraout_RAX;
        uVar8 = extraout_RCX_00;
        uVar11 = extraout_RBX;
      }
      puStack_40 = puVar5;
      func_0x0047e9c0(puVar5 + 6,uVar14,iVar12);
      uVar11 = uVar11 + 4;
      puVar5 = puStack_40;
      if (uVar8 < uVar11) {
        func_0x00479da0(puStack_40,uVar11,uVar8,4,&UNK_02b6edd8);
        puVar5 = extraout_RAX_00;
        uVar8 = extraout_RCX_01;
        uVar11 = extraout_RBX_00;
      }
      *(undefined4 *)((uVar11 - 4) + (int)puVar5) = 0x1001000;
      uVar11 = uVar11 + 2;
      if (uVar8 < uVar11) {
        func_0x00479da0();
        puVar5 = extraout_RAX_01;
        uVar8 = extraout_RCX_02;
        uVar11 = extraout_RBX_01;
      }
      *(ushort *)((uVar11 - 2) + (int)puVar5) = (ushort)iVar3 << 8 | (ushort)iVar3 >> 8;
      uVar10 = uVar11 + iVar3;
      if (uVar8 < uVar10) {
        func_0x00479da0(puVar5,uVar10,uVar8,iVar3,&UNK_02b6edd8);
        puVar5 = extraout_RAX_02;
        uVar8 = extraout_RCX_03;
        uVar10 = extraout_RBX_02;
      }
      puStack_58 = puVar5;
      func_0x0047e9c0((int)puVar5 + uVar11,uStack_50,iVar3);
      piVar9 = piStack0000000000000008;
      if ((uint)piStack0000000000000008[0xc] <= uVar4) {
        func_0x0047e620();
        break;
      }
      iVar3 = piStack0000000000000008[0xb];
      *(uint *)(iVar3 + 8 + iStack_70 * 8) = uVar10;
      *(uint *)(iVar3 + 0x10 + iStack_70 * 8) = uVar8;
      iVar12 = iStack_70;
      if (_DAT_02e18cd0 != 0) {
        func_0x0047e280();
        *extraout_R11_00 = (int)puStack_58;
        extraout_R11_00[1] = extraout_R10;
        uVar4 = extraout_RDI;
        iVar3 = extraout_R8_00;
        iVar12 = extraout_R9;
      }
      *(ushort **)(iVar3 + iVar12 * 8) = puStack_58;
      puVar6 = puStack_30 + 3;
      uVar4 = uVar4 + 1;
      uVar8 = uStack0000000000000018;
    }
    func_0x0047e620();
  }
  func_0x0047e620();
  func_0x004451c0();
  auVar2._8_8_ = uStack_60;
  auVar2._0_8_ = uStack_68;
  auVar2._16_8_ = 0;
  return auVar2 << 0x40;
}

