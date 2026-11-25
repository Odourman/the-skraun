"""FULLGAME-1: event-coded PF1/BL/M1 renderer, early GRP1 on stable scanlines.

SOURCE_ONLY/DEVELOPER_OBSERVED experimental code. 24 world-band events
replace 186 unconditional PF/effect writes per visible arena frame. No
new independent TIA players; this does not solve same-Y 3-actor rendering.
"""

def once(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        raise ValueError(f'{tag}: expected one source anchor, got {n}')
    return s.replace(old, new, 1)


def sparse_kernel_bank3(s):
    # Preserve the generated prefix of each dynamic sprite decoder.
    # Only its register order and PF/effect update policy are changed.
    for label, effect, register, skip in (
        ('Visible:', 'OrbRowPtr', 'ENABL', 'WorldPFHold'),
        ('VisibleArrow:', 'ArrowRowPtr', 'ENAM1', 'ArrowPFHold'),
    ):
        start = s.index(label + '\n') + len(label) + 1
        end = s.index('        txa\n        sec\n        sbc RenderBottom\n', start)
        old = s[start:end]
        assert old.startswith('        sta WSYNC\n        sta GRP0\n')
        actor = old[old.index('        txa\n        sec\n        sbc EnemyBottom\n'):]
        assert actor.count('        sta GRP1') == 1
        new = (
            '        sta WSYNC\n'
            '        sta GRP0\n'
            '        ldy WorldPFIndex,x\n'
            f'        beq {skip}\n'
            '        lda (WorldPFPtr),y\n'
            '        sta PF1\n'
            f'        lda ({effect}),y\n'
            f'        sta {register}\n'
            f'{skip}:\n'
        ) + actor
        s = s[:start] + new + s[end:]
    # F9 missile seed and FD ball seed point one byte earlier because
    # a nonzero event code is (band+1), rather than the original band.
    s = once(s, '        adc #$2A', '        adc #$29', 'M1 seed offset')
    s = once(s, '        lda #$38', '        lda #$37', 'BL seed offset')
    # Avoid DEY on beam-critical rows: shift world data one byte forward,
    # replacing the previously unused sentinel after the 192 world bytes.
    s = once(s, 'PlayPF1:\n', 'PlayPF1:\n        dc.b 0 ; event-index sentinel\n', 'PF1 seed')
    s = once(s, '        dc.b 0\nK1NeutralBytes:', 'K1NeutralBytes:', 'PF1 tail')
    # 0 = no TIA register update. Nonzero event = 1 + world band index.
    # x=186 initializes the display, x=183,175,...,7 change world bands.
    ev = [0] * 193
    ev[186] = 24
    for x in range(7, 184, 8):
        ev[x] = (x // 8) + 1
    assert sum(bool(v) for v in ev) == 24
    start = s.index('WorldPFIndex:\n')
    end = s.index('        ORG $FD00\n', start)
    table = 'WorldPFIndex:\n' + ''.join(
        '        dc.b ' + ','.join(str(v) for v in ev[i:i+16]) + '\n'
        for i in range(0, 193, 16)
    )
    s = s[:start] + table + s[end:]
    # 56 bytes of obsolete original F01 collision tables: active candidate
    # collision uses live per-stage RIOT rectangles at $C0..$CF.
    start = s.index('RectLo:\n')
    end = s.index('        ; PLAY1 code/data inserted below', start)
    assert s[start:end].count('F01Diag_L3:') == 1
    s = s[:start] + '; Obsolete F01 diagnostic ROM tables removed.\n' + s[end:]
    # Two safe branch shortens preserve exact flags at the branch site.
    s = once(s, '        jmp MissileRowReady',
             '        bne MissileRowReady', 'branch shorten M1')
    s = once(s,
        '        dex\n        bne Visible\n        jmp VisibleDone',
        '        dex\n        bne Visible\n        beq VisibleDone', 'branch shorten P0')
    s = once(s, '        ORG $F459\nPF0Choices:',
             '        ORG $F478\nPF0Choices:', 'visible code expansion')
    return s
