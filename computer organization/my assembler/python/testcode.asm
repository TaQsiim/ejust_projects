        ORG  100
        LDA SUB
        CMA
        INC
        ADD MIN
        STA DIF
        HLT
MIN,    DEC 83
SUB,    DEC -23
DIF,    HEX 0
END