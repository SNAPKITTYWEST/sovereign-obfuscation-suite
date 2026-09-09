//RBGQASM JOB (SOV,2026),'SPARSE-RBG-QASM-EXEC',CLASS=A,MSGCLASS=X,
// NOTIFY=&SYSUID,REGION=0M,TIME=1440
//*-------------------------------------------------------------------*
//* COMPILE AND DISPATCH SPARSE RBG GLUE THROUGH QASM COPROCESSOR *
//*-------------------------------------------------------------------*
//STEP01 EXEC PGM=BPXBATCH,REGION=0M
//STDOUT DD SYSOUT=*
//STDERR DD SYSOUT=*
//RBGIN DD DSN=SOVEREIGN.TENSOR.RBG.GLUE,DISP=SHR
//QASMIN DD DSN=SOVEREIGN.CIRCUITS.QASM(SPARSERBG),DISP=SHR
//QASMBOUT DD DSN=SOVEREIGN.QASM.PROCESSED.DATA,
// DISP=(NEW,CATLG,DELETE),
// UNIT=SYSDA,SPACE=(CYL,(200,50),RLSE),
// DCB=(RECFM=VB,LRECL=4096,BLKSIZE=0)
//SYSTSIN DD *
  SH +
  export THETA_INVARIANT="0.036154345"; +
  export SPARSE_DIM="64"; +
  /u/sovereign/bin/sparse_rbg_qasm_bridge.elf \
    --tensor_input=//DD:RBGIN \
    --circuit_input=//DD:QASMIN \
    --output=//DD:QASMBOUT \
    --theta=$THETA_INVARIANT \
    --dim=$SPARSE_DIM
/*
//*-------------------------------------------------------------------*
//* FLUSH VOLATILE MEMORY BUFFERS *
//*-------------------------------------------------------------------*
//STEP02 EXEC PGM=IEFBR14,COND=(0,NE)
//PURGE DD DSN=SOVEREIGN.SHADOW.VOLATILE.MEM,
// DISP=(MOD,DELETE,DELETE),UNIT=SYSDA,SPACE=(TRK,(0,0))
//
