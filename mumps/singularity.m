SINGULARITY(TX, MASS, SPIN, PAYLOAD) ; Ingest tabular data into the Event Horizon
    ; Validate No-Hair Theorem properties
    I MASS="" S MASS=0
    I SPIN="" S SPIN=89/2462
    
    ; Spaghettify the payload (Stretch and compress into the node)
    N SPAGHETTI
    S SPAGHETTI=$TR(PAYLOAD," ","") ; Remove whitespace vacuum
    
    ; Lock the singularity boundary
    L +^BLACKHOLE(TX):2 E W "EVENT HORIZON COLLISION",! Q
    
    ; Punch the permanent ledger entry
    S ^BLACKHOLE(TX,"M")=MASS
    S ^BLACKHOLE(TX,"J")=SPIN
    S ^BLACKHOLE(TX,"DATA")=SPAGHETTI
    
    ; Aggregate total ledger mass at the singularity core
    S ^BLACKHOLE("CORE","TOTAL_MASS")=$G(^BLACKHOLE("CORE","TOTAL_MASS"))+MASS
    
    ; Release the boundary lock
    L -^BLACKHOLE(TX)
    
    W "[OK] TABULATION COMPLETE. PAYLOAD PAST EVENT HORIZON.",!
    Q
