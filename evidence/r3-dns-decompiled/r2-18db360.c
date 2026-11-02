/* Decompiled observation, not original source. Go ABI/types incomplete. SHA256: 5d58cdde3483029a70c8b52b9434c4fe4bb4fbc093e47c5c38aba4be9361fb52 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [32] recovered_18db360(void)

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
  auVar12 = func_0x018dcb80(in_stack_00000028,in_stack_00000030,&UNK_01f57112,2);
  func_0x00800380(&UNK_01f57572,3,auVar12._0_8_,auVar12._8_8_);
  if (extraout_RBX != 0) {
    auVar8._0_16_ = ZEXT816(0);
    auVar8._16_8_ = extraout_RBX;
    auVar8._24_8_ = extraout_RCX;
    return auVar8;
  }
  func_0x00800ea0(&UNK_01f57572,3,extraout_RAX);
  if (extraout_RBX_00 != 0) {
    auVar12 = (*(code *)**(undefined8 **)(_DAT_02d638e8 + 0x18))
                        (*(undefined8 *)(_DAT_02d638e8 + 0x10),0xffffffc2,0xffffffca,
                         *(undefined4 *)(*(int *)(_DAT_02d638e8 + 0x28) + 0x18),0x3bb2f74f,
                         *(undefined8 *)(*(int *)(_DAT_02d638e8 + 0x28) + 0x28));
    uStack_60 = auVar12._0_8_;
    puStack_28 = &UNK_02aa0900;
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
      puVar4 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bac6d0,1);
      puVar4[1] = auVar12._8_8_;
      if (_DAT_02e07dc0 != 0) {
        puVar4 = (undefined8 *)func_0x0047e260();
        *extraout_R11_03 = uStack_60;
      }
      *puVar4 = uStack_60;
      auVar14._8_8_ = puVar4;
      auVar14._0_8_ = &UNK_02c85ff0;
    }
    auVar7._24_8_ = auVar14._8_8_;
    auVar7._0_16_ = ZEXT816(0);
    auVar7._16_8_ = auVar14._0_8_;
    return auVar7;
  }
  if (*extraout_RAX_00 == 0) {
    puVar9 = &UNK_02c860f0;
    piVar2 = (int *)0x0;
    puVar10 = (undefined *)0x0;
    puVar11 = &UNK_01fd8148;
  }
  else {
    iVar1 = *extraout_RAX_00;
    piVar2 = (int *)func_0x0041f020(8,&UNK_02bad5d0,1);
    if (_DAT_02e07dc0 != 0) {
      piVar2 = (int *)func_0x0047e260();
      *extraout_R11 = iVar1;
    }
    *piVar2 = iVar1;
    puVar9 = (undefined *)0x0;
    puVar10 = &UNK_02c89fc8;
    puVar11 = (undefined *)0x0;
  }
  if (puVar9 == (undefined *)0x0) {
    uStack_40 = recovered_18d9b20(in_stack_00000118,in_stack_00000120);
    uStack_48 = func_0x00416cc0(&UNK_02b10258,0x10);
    uStack_50 = func_0x00416cc0(&UNK_02b10418,0);
    uStack_58 = func_0x00475c00();
    puVar4 = (undefined8 *)func_0x004204c0(0x50,&UNK_02c683a0,1);
    if (_DAT_02e07dc0 != 0) {
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
    puVar5 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bb6c00,1);
    *puVar5 = &UNK_01953b60;
    if (_DAT_02e07dc0 != 0) {
      puVar5 = (undefined8 *)func_0x0047e260();
      *extraout_R11_02 = puVar4;
    }
    puVar5[1] = puVar4;
    func_0x00450a80();
    return ZEXT1632(CONCAT88(puVar4,&UNK_02c886c8));
  }
  func_0x007e9940(extraout_RAX_00);
  auVar12 = (*(code *)*_DAT_02d63908)
                      (**(undefined4 **)(_DAT_02d63920 + 8),
                       *(undefined8 *)(*(undefined4 **)(_DAT_02d63920 + 8) + 10),
                       *(undefined8 *)(*(int *)(_DAT_02d638e8 + 0x28) + 0x10));
  uVar3 = auVar12._0_8_;
  uStack_38 = 0;
  if (puVar9 != (undefined *)0x0) {
    uStack_38 = *(undefined8 *)(puVar9 + 8);
  }
  puStack_30 = puVar11;
  auVar13 = func_0x0066c760(uVar3,auVar12._8_8_,&uStack_38,1,1);
  if (auVar13._0_8_ == 0) {
    puVar4 = (undefined8 *)func_0x0041f260(0x10,&UNK_02bac6d0,1);
    puVar4[1] = auVar12._8_8_;
    if (_DAT_02e07dc0 != 0) {
      puVar4 = (undefined8 *)func_0x0047e260();
      *extraout_R11_00 = uVar3;
    }
    *puVar4 = uVar3;
    auVar13._8_8_ = puVar4;
    auVar13._0_8_ = &UNK_02c85ff0;
  }
  auVar6._24_8_ = auVar13._8_8_;
  auVar6._0_16_ = ZEXT816(0);
  auVar6._16_8_ = auVar13._0_8_;
  return auVar6;
}

