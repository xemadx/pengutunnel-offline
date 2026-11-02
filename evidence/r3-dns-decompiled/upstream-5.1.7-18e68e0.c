/* Decompiled observation, not original source. Go ABI/types incomplete. SHA256: 9cfe9837524fee120043fe52e61164bdb2bf70c47172970d84e3b7337659d895 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [32] recovered_18e68e0(void)

{
  int iVar1;
  undefined8 extraout_RAX;
  int *extraout_RAX_00;
  int *piVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  int extraout_RBX;
  int extraout_RBX_00;
  undefined *puVar10;
  undefined8 extraout_RCX;
  undefined8 extraout_RCX_00;
  undefined *puVar9;
  undefined1 auVar6 [32];
  undefined1 auVar7 [32];
  undefined1 auVar8 [32];
  undefined *puVar11;
  int *extraout_R11;
  undefined8 *extraout_R11_00;
  undefined8 *extraout_R11_01;
  undefined8 *extraout_R11_02;
  undefined8 *extraout_R11_03;
  int unaff_R14;
  undefined1 auVar12 [16];
  undefined1 auVar13 [16];
  undefined1 auVar14 [16];
  undefined8 in_stack_00000028;
  undefined8 in_stack_00000030;
  undefined8 in_stack_00000118;
  undefined8 in_stack_00000120;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined *puStack_30;
  undefined *puStack_28;
  undefined8 uStack_20;
  undefined8 uStack_18;
  undefined8 uStack_10;
  
  while (&uStack_60 <= *(undefined8 **)(unaff_R14 + 0x10)) {
    func_0x0047c9e0();
  }
  auVar12 = func_0x018e80e0(in_stack_00000028,in_stack_00000030,&UNK_01f66118,2);
  func_0x00800380(&UNK_01f6656e,3,auVar12._0_8_,auVar12._8_8_);
  if (extraout_RBX != 0) {
    auVar8._0_16_ = ZEXT816(0);
    auVar8._16_8_ = extraout_RBX;
    auVar8._24_8_ = extraout_RCX;
    return auVar8;
  }
  func_0x00800ea0(&UNK_01f6656e,3,extraout_RAX);
  if (extraout_RBX_00 != 0) {
    auVar12 = (*(code *)*_DAT_02d87c08)(*_DAT_02d87c20,0x8bfd91228a3027d2,_DAT_02d87c38);
    uStack_60 = auVar12._0_8_;
    puStack_28 = &UNK_02ab11a8;
    if (extraout_RBX_00 == 0) {
      uStack_18 = 0;
    }
    else {
      uStack_18 = *(undefined8 *)(extraout_RBX_00 + 8);
    }
    uStack_20 = extraout_RAX;
    uStack_10 = extraout_RCX_00;
    auVar14 = func_0x0066c760();
    if (auVar14._0_8_ == 0) {
      puVar4 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bbc888,1);
      puVar4[1] = auVar12._8_8_;
      if (_DAT_02e18cd0 != 0) {
        puVar4 = (undefined8 *)func_0x0047e260();
        *extraout_R11_03 = uStack_60;
      }
      *puVar4 = uStack_60;
      auVar14._8_8_ = puVar4;
      auVar14._0_8_ = &UNK_02c96978;
    }
    auVar7._24_8_ = auVar14._8_8_;
    auVar7._0_16_ = ZEXT816(0);
    auVar7._16_8_ = auVar14._0_8_;
    return auVar7;
  }
  if (*extraout_RAX_00 == 0) {
    puVar9 = &UNK_02c96a78;
    piVar2 = (int *)0x0;
    puVar10 = (undefined *)0x0;
    puVar11 = &UNK_01fe7490;
  }
  else {
    iVar1 = *extraout_RAX_00;
    piVar2 = (int *)func_0x0041f020(8,&UNK_02bbd788,1);
    if (_DAT_02e18cd0 != 0) {
      piVar2 = (int *)func_0x0047e260();
      *extraout_R11 = iVar1;
    }
    *piVar2 = iVar1;
    puVar9 = (undefined *)0x0;
    puVar10 = &UNK_02c9a950;
    puVar11 = (undefined *)0x0;
  }
  if (puVar9 == (undefined *)0x0) {
    uStack_40 = recovered_18e50a0(in_stack_00000118,in_stack_00000120);
    uStack_48 = func_0x00416cc0(&UNK_02b200a8,0x10);
    uStack_50 = func_0x00416cc0(&UNK_02b20228,0);
    uStack_58 = func_0x00475c00();
    puVar4 = (undefined8 *)func_0x004204c0(0x50,&UNK_02c78d28,1);
    if (_DAT_02e18cd0 != 0) {
      puVar4 = (undefined8 *)func_0x0047e300();
      *extraout_R11_01 = extraout_RAX_00;
      extraout_R11_01[1] = piVar2;
      extraout_R11_01[2] = uStack_40;
      extraout_R11_01[3] = uStack_48;
      extraout_R11_01[4] = uStack_50;
      extraout_R11_01[5] = uStack_58;
    }
    *puVar4 = extraout_RAX_00;
    puVar4[1] = puVar10;
    puVar4[2] = piVar2;
    puVar4[3] = uStack_40;
    puVar4[4] = uStack_48;
    puVar4[5] = uStack_50;
    puVar4[9] = uStack_58;
    puVar5 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bc6e38,1);
    *puVar5 = &UNK_01967340;
    if (_DAT_02e18cd0 != 0) {
      puVar5 = (undefined8 *)func_0x0047e260();
      *extraout_R11_02 = puVar4;
    }
    puVar5[1] = puVar4;
    func_0x00450a80();
    return ZEXT1632(CONCAT88(puVar4,&UNK_02c99050));
  }
  func_0x007e9940(extraout_RAX_00);
  auVar12 = (*(code *)**(undefined8 **)(_DAT_02d87c20 + 0x20))
                      (*(undefined4 *)(_DAT_02d87c20 + 0xc),0xffffb04b,0x66b1,_DAT_02d87b88,
                       _DAT_02d87b98);
  uVar3 = auVar12._0_8_;
  uStack_38 = 0;
  if (puVar9 != (undefined *)0x0) {
    uStack_38 = *(undefined8 *)(puVar9 + 8);
  }
  puStack_30 = puVar11;
  auVar13 = func_0x0066c760(uVar3,auVar12._8_8_,&uStack_38,1,1);
  if (auVar13._0_8_ == 0) {
    puVar4 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bbc888,1);
    puVar4[1] = auVar12._8_8_;
    if (_DAT_02e18cd0 != 0) {
      puVar4 = (undefined8 *)func_0x0047e260();
      *extraout_R11_00 = uVar3;
    }
    *puVar4 = uVar3;
    auVar13._8_8_ = puVar4;
    auVar13._0_8_ = &UNK_02c96978;
  }
  auVar6._24_8_ = auVar13._8_8_;
  auVar6._0_16_ = ZEXT816(0);
  auVar6._16_8_ = auVar13._0_8_;
  return auVar6;
}

