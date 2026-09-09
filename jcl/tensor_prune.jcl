//SPIRALJB JOB (SOV,2026),'TENSOR-PRUNE-RBG',CLASS=A,MSGCLASS=X,
// NOTIFY=&SYSUID,TIME=1440
//*-------------------------------------------------------------------*
//* LOGARITHMIC SPIRAL: TENSOR LINEAR PRUNING OF RBG LIBRARY
//*-------------------------------------------------------------------*
//STEP01 EXEC PGM=IDCAMS
//SYSPRINT DD SYSOUT=*
//SYSIN DD *
  DELETE SOVEREIGN.RBG.TENSOR.TEMP SCRATCH PURGE
  SET MAXCC = 0
/*
//STEP02 EXEC PGM=IKJEFT01,REGION=0M,DYNAMNBR=250
//SYSTSPRT DD SYSOUT=*
//RBGLIB DD DSN=SOVEREIGN.RBG.LIBRARY,DISP=SHR
//PRUNEOUT DD DSN=SOVEREIGN.RBG.PRUNED,
// DISP=(NEW,CATLG,DELETE),
// UNIT=SYSDA,SPACE=(CYL,(500,100),RLSE),
// DCB=(RECFM=U,BLKSIZE=32760)
//SYSTSIN DD *
  BPXBATCH SH +
    python3 /u/sovereign/burt_imma/tensor_prune_rbg.py \
      --manifold=logarithmic_spiral \
      --input_dd=RBGLIB \
      --output_dd=PRUNEOUT \
      --decay_threshold=linear \
      --cuda_offload=disable
/*
//
