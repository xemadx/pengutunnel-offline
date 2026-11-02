/* Decompiled observation, not original source. Go ABI/types incomplete. SHA256: 9cfe9837524fee120043fe52e61164bdb2bf70c47172970d84e3b7337659d895 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [24] recovered_18e5960(int param_1,int param_2,int param_3)

{
  dword dVar1;
  undefined1 auVar2 [24];
  undefined1 auVar3 [24];
  undefined1 auVar4 [24];
  uint uVar5;
  undefined8 uVar6;
  undefined8 *puVar7;
  uint extraout_RAX;
  undefined8 extraout_RAX_00;
  undefined8 extraout_RAX_01;
  undefined8 extraout_RCX;
  uint uVar9;
  undefined8 extraout_RCX_00;
  undefined8 extraout_RCX_01;
  int extraout_RCX_02;
  int iVar10;
  undefined8 extraout_RCX_03;
  undefined1 auVar8 [24];
  int extraout_RBX;
  undefined8 extraout_RBX_00;
  undefined8 extraout_RBX_01;
  int extraout_RBX_02;
  char extraout_SIL;
  undefined8 extraout_RSI;
  int extraout_RSI_00;
  int extraout_RSI_01;
  undefined8 extraout_RSI_02;
  undefined8 extraout_RSI_03;
  uint extraout_RDI;
  uint extraout_RDI_00;
  undefined8 extraout_R8;
  int extraout_R8_00;
  int extraout_R8_01;
  int iVar11;
  int extraout_R8_02;
  int extraout_R9;
  undefined8 extraout_R9_00;
  int iVar12;
  undefined8 extraout_R10;
  undefined8 *extraout_R11;
  int *extraout_R11_00;
  undefined8 *extraout_R11_01;
  undefined8 *extraout_R11_02;
  int iVar13;
  undefined8 *extraout_R11_03;
  undefined8 *extraout_R11_04;
  undefined8 *extraout_R11_05;
  undefined8 *extraout_R11_06;
  int unaff_R14;
  undefined8 in_XMM15_Qa;
  undefined8 in_XMM15_Qb;
  undefined1 auVar14 [16];
  int iStack0000000000000008;
  int iStack0000000000000010;
  int iStack0000000000000018;
  int iStack_48;
  undefined1 auStack_40 [16];
  undefined8 uStack_30;
  undefined8 uStack_28;
  undefined *puStack_20;
  int iStack_18;
  undefined **ppuStack_10;
  
  iStack0000000000000008 = param_1;
  iStack0000000000000018 = param_3;
  iStack0000000000000010 = param_2;
  while (&iStack_48 <= *(int **)(unaff_R14 + 0x10)) {
    func_0x0047c9e0();
  }
  uVar5 = 0;
  LOCK();
  dVar1 = *(dword *)(iStack0000000000000008 + 0x24);
  if (dVar1 == 0) {
    *(dword *)(iStack0000000000000008 + 0x24) = 1;
  }
  else {
    uVar5 = (uint)dVar1;
  }
  UNLOCK();
  auStack_40._0_8_ = in_XMM15_Qa;
  auStack_40._8_8_ = in_XMM15_Qb;
  if (dVar1 != 0) {
    uVar5 = func_0x004a33c0(iStack0000000000000008 + 0x24);
  }
  puStack_20 = &UNK_01967180;
  iStack_18 = iStack0000000000000008 + 0x24;
  ppuStack_10 = &puStack_20;
  iVar10 = iStack0000000000000008;
LAB_018e5a35:
  uVar9 = *(uint *)(iVar10 + 0xb0);
  if ((int)uVar9 < (int)*(uint *)(iVar10 + 0xa0)) {
    if (uVar9 < *(uint *)(iVar10 + 0xa0)) {
      iVar11 = *(int *)(*(int *)(iVar10 + 0x98) + 8 + uVar9 * 0x18);
      iVar13 = *(int *)(*(int *)(iVar10 + 0x98) + uVar9 * 0x18);
      *(uint *)(iVar10 + 0xb0) = uVar9 + 1;
      if (iStack0000000000000018 < iVar11) {
        auVar14 = (*(code *)*_DAT_02d87bf8)
                            (0x4fe66be57fb2b6cf,0x2e2a52fb,*(undefined8 *)(_DAT_02d87c20 + 0x10),
                             _DAT_02d87be0,_DAT_02d87ba8);
        uStack_28 = auVar14._0_8_;
        auStack_40 = func_0x0066c760(uStack_28,auVar14._8_8_,0,0,0);
        if (auStack_40._0_8_ == 0) {
          puVar7 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bbc888,1);
          puVar7[1] = auVar14._8_8_;
          if (_DAT_02e18cd0 != 0) {
            puVar7 = (undefined8 *)func_0x0047e260();
            *extraout_R11_03 = uStack_28;
          }
          *puVar7 = uStack_28;
          auStack_40._8_8_ = puVar7;
          auStack_40._0_8_ = &UNK_02c96978;
        }
        (*(code *)*ppuStack_10)();
        auVar2._16_8_ = 0;
        auVar2._0_16_ = auStack_40;
        return auVar2 << 0x40;
      }
      iVar10 = iStack0000000000000018;
      if (iVar11 < iStack0000000000000018) {
        iVar10 = iVar11;
      }
      if (iStack0000000000000010 != iVar13) {
        iStack_48 = iVar10;
        func_0x0047e9c0(iStack0000000000000010,iVar13);
        iVar10 = iStack_48;
      }
      auStack_40._0_8_ = in_XMM15_Qa;
      auStack_40._8_8_ = in_XMM15_Qb;
      (*(code *)*ppuStack_10)();
      auVar8._8_8_ = auStack_40._0_8_;
      auVar8._0_8_ = iVar10;
      auVar8._16_8_ = auStack_40._8_8_;
      return auVar8;
    }
    func_0x0047e620(uVar5);
    uVar6 = extraout_RCX_03;
    iVar10 = extraout_RBX_02;
LAB_018e5e12:
    auStack_40._0_8_ = iVar10;
    auStack_40._8_8_ = uVar6;
    (*(code *)*ppuStack_10)();
    auVar3._8_8_ = auStack_40._8_8_;
    auVar3._0_8_ = auStack_40._0_8_;
    auVar3._16_8_ = 0;
    return auVar3 << 0x40;
  }
  if (*(int *)(iVar10 + 0x68) != 0) goto LAB_018e5aa5;
  uVar6 = func_0x00479cc0(&UNK_02b1f890,0x20,0x20);
  iVar10 = iStack0000000000000008;
  *(undefined8 *)(iStack0000000000000008 + 0x70) = 0x20;
  *(undefined8 *)(iStack0000000000000008 + 0x78) = 0x20;
  if (_DAT_02e18cd0 != 0) {
    uVar6 = func_0x0047e280();
    *extraout_R11 = uVar6;
    extraout_R11[1] = extraout_RSI;
  }
  *(undefined8 *)(iVar10 + 0x68) = uVar6;
  uVar5 = 0;
  do {
    if ((int)uVar5 < 0x20) {
      uVar6 = func_0x00479cc0(&UNK_02b6edd8,0xffff,0xffff);
      if (*(uint *)(iStack0000000000000008 + 0x70) <= uVar5) {
        func_0x0047e620();
        func_0x004451c0();
        auVar4._8_8_ = auStack_40._8_8_;
        auVar4._0_8_ = auStack_40._0_8_;
        auVar4._16_8_ = 0;
        return auVar4 << 0x40;
      }
      iVar10 = *(int *)(iStack0000000000000008 + 0x68);
      iVar11 = uVar5 * 3;
      *(undefined8 *)(iVar10 + 8 + uVar5 * 0x18) = 0xffff;
      *(undefined8 *)(iVar10 + 0x10 + uVar5 * 0x18) = 0xffff;
      if (_DAT_02e18cd0 != 0) {
        uVar6 = func_0x0047e280();
        *extraout_R11_04 = uVar6;
        extraout_R11_04[1] = extraout_R9_00;
        iVar10 = extraout_RSI_01;
        uVar5 = extraout_RDI_00;
        iVar11 = extraout_R8_02;
      }
    }
    else {
      uVar6 = func_0x00479cc0(&UNK_02b6ef98,0x20,0x20);
      iVar10 = iStack0000000000000008;
      *(undefined8 *)(iStack0000000000000008 + 0x88) = 0x20;
      *(undefined8 *)(iStack0000000000000008 + 0x90) = 0x20;
      if (_DAT_02e18cd0 != 0) {
        uVar6 = func_0x0047e280();
        *extraout_R11_05 = uVar6;
        extraout_R11_05[1] = extraout_RSI_02;
      }
      *(undefined8 *)(iVar10 + 0x80) = uVar6;
      uVar6 = func_0x00479cc0(&UNK_02b1f890,0,0x20);
      iVar10 = iStack0000000000000008;
      *(undefined8 *)(iStack0000000000000008 + 0xa0) = 0;
      *(undefined8 *)(iStack0000000000000008 + 0xa8) = 0x20;
      if (_DAT_02e18cd0 != 0) {
        uVar6 = func_0x0047e280();
        *extraout_R11_06 = uVar6;
        extraout_R11_06[1] = extraout_RSI_03;
      }
      *(undefined8 *)(iVar10 + 0x98) = uVar6;
LAB_018e5aa5:
      puVar7 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bc6fb8,1);
      *puVar7 = &UNK_01967120;
      if (_DAT_02e18cd0 != 0) {
        puVar7 = (undefined8 *)func_0x0047e260();
        *extraout_R11_00 = iStack0000000000000008;
      }
      puVar7[1] = iStack0000000000000008;
      recovered_18e4e60(*(undefined8 *)(iStack0000000000000008 + 8),
                        *(undefined8 *)(iStack0000000000000008 + 0x10),puVar7);
      uVar6 = extraout_RCX;
      iVar10 = extraout_RBX;
      if (extraout_RBX != 0) goto LAB_018e5e12;
      *(undefined8 *)(iStack0000000000000008 + 0xa0) = 0;
      *(undefined8 *)(iStack0000000000000008 + 0xb0) = 0;
      uVar9 = 0;
      iVar10 = iStack0000000000000008;
      while( true ) {
        uVar5 = extraout_RAX;
        if ((int)extraout_RAX <= (int)uVar9) goto LAB_018e5a35;
        if (*(uint *)(iVar10 + 0x88) <= uVar9) goto LAB_018e5e6a;
        uVar5 = *(uint *)(*(int *)(iVar10 + 0x80) + uVar9 * 8);
        if (*(uint *)(iVar10 + 0x70) <= uVar9) goto LAB_018e5e65;
        uVar6 = *(undefined8 *)(*(int *)(iVar10 + 0x68) + uVar9 * 0x18);
        if (*(uint *)(*(int *)(iVar10 + 0x68) + 0x10 + uVar9 * 0x18) < uVar5) break;
        recovered_18e5320(*(undefined8 *)(iVar10 + 0x18),uVar6,uVar5);
        iVar10 = iStack0000000000000008;
        if (extraout_SIL != '\0') {
          uVar5 = *(int *)(iStack0000000000000008 + 0xa0) + 1;
          auVar14._8_8_ = uVar5;
          auVar14._0_8_ = *(undefined8 *)(iStack0000000000000008 + 0x98);
          uVar6 = extraout_RAX_00;
          if (*(uint *)(iStack0000000000000008 + 0xa8) < uVar5) {
            uStack_30 = extraout_RAX_00;
            func_0x00479da0(*(undefined8 *)(iStack0000000000000008 + 0x98),uVar5,
                            *(uint *)(iStack0000000000000008 + 0xa8),1,&UNK_02b1f890);
            iVar10 = iStack0000000000000008;
            auVar14._8_8_ = extraout_RBX_01;
            auVar14._0_8_ = extraout_RAX_01;
            *(undefined8 *)(iStack0000000000000008 + 0xa8) = extraout_RCX_01;
            if (_DAT_02e18cd0 != 0) {
              auVar14 = func_0x0047e280();
              *extraout_R11_01 = auVar14._0_8_;
              extraout_R11_01[1] = extraout_R8;
            }
            *(int *)(iVar10 + 0x98) = auVar14._0_8_;
            uVar6 = uStack_30;
          }
          iVar12 = auVar14._8_8_;
          iVar13 = auVar14._0_8_;
          *(int *)(iVar10 + 0xa0) = iVar12;
          iVar11 = iVar12 * 3;
          *(undefined8 *)(iVar13 + -0x10 + iVar12 * 0x18) = extraout_RBX_00;
          *(undefined8 *)(iVar13 + -8 + iVar12 * 0x18) = extraout_RCX_00;
          if (_DAT_02e18cd0 != 0) {
            uVar6 = func_0x0047e280(uVar6,extraout_RBX_00,iVar13);
            *extraout_R11_02 = uVar6;
            extraout_R11_02[1] = extraout_R10;
            iVar10 = extraout_R8_00;
            iVar11 = extraout_R9;
            iVar13 = extraout_RCX_02;
          }
          *(undefined8 *)(iVar13 + -0x18 + iVar11 * 8) = uVar6;
        }
        uVar9 = uVar9 + 1;
      }
      func_0x0047e620(extraout_RAX,uVar6);
LAB_018e5e65:
      func_0x0047e620();
LAB_018e5e6a:
      uVar6 = func_0x0047e620();
      iVar10 = extraout_RSI_00;
      uVar5 = extraout_RDI;
      iVar11 = extraout_R8_01;
    }
    *(undefined8 *)(iVar10 + iVar11 * 8) = uVar6;
    uVar5 = uVar5 + 1;
  } while( true );
}

