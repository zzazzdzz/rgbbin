SECTION "WRAM", ROM0[$D322]

Start:
    ld hl, Start
    jp Start
    call Start

Test:
    ld de, Test-Start
    nop
    nop
    nop
    jr Test
    
SECTION "SRAM", ROM0[$A000]

Potato:
    ld a, b
Tomato:
    ld b, c
Cheese:
    ld c, d
    jp Potato
    jp Tomato
    jp Cheese
