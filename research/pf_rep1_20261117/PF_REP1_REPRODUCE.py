#!/usr/bin/env python3
"""THE SKRAUN PF-REP1: reproducible source-only register/colour screen.

NOT a Stella emulator, not a measured scanline trace, and not a rendering
authorisation. Only uses actual R3 source-derived masks from the adjacent JSON.
Requires Python 3.10+ stdlib. Run: python3 PF_REP1_REPRODUCE.py
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/"R3_SOURCE_EXACT_MASKS.json").read_text(encoding="utf-8"))

def source_rows(mode:str, pos:int):
    flat=bytes.fromhex(DATA["modes"][mode][str(pos)])
    assert len(flat)==95, (mode,pos,len(flat))
    chunks=[flat[j*19:(j+1)*19] for j in range(5)]
    rowmap=bytes.fromhex(DATA["rowmap_hex"])
    assert len(rowmap)==177
    return [(0,*(a[rowmap[x]] for a in chunks)) for x in range(176,0,-2)]

def pf20(a,b,c):
    """TIA PF0 bits 4..7, PF1 bits 7..0, PF2 bits 0..7.
       These are PF bit cells; each occupies four colour clocks.
    """
    return ([(a>>i)&1 for i in range(4,8)]
          + [(b>>i)&1 for i in range(7,-1,-1)]
          + [(c>>i)&1 for i in range(8)])

def visible_pf(row):
    assert len(row)==6
    bits=pf20(*row[:3])+pf20(*row[3:])
    assert len(bits)==40
    return bits

def go():
    assert DATA["schema"]=="skraun.pf-rep1.r3-source-mask-snapshot.v1"
    assert DATA["origin_github_blob_sha"]=="3c9ed79078eee6a0c63100614a593f92e240b5e8"
    assert DATA["x_positions"]==list(range(56,105,4))
    stats=[]
    for xpos in DATA["x_positions"]:
        hrows=source_rows("halo",xpos)
        srows=source_rows("scenery",xpos)
        assert len(hrows)==len(srows)==88
        prev_fields=(0,)*6
        prev_actual=[0,0,0]
        multi_count=0
        phase_hist=Counter()
        phase_events=0
        colour_coactive=0
        colour_same_half=0
        overlapping_bit_rows=0
        priority_halo_hist=Counter()
        priority_scenery_hist=Counter()
        first_mult=None
        first_overlap=None
        for row_index,(halo,scenery) in enumerate(zip(hrows,srows)):
            # Count field transitions between successive R3 pair source states.
            changed=sum(a!=b for a,b in zip(halo,prev_fields))
            if changed>1:
                multi_count+=1
                if first_mult is None:
                    first_mult={"pair":row_index,"R3_index":176-2*row_index,
                                "prior":list(prev_fields),"new":list(halo),
                                "changed_fields":changed}
            prev_fields=halo

            # Two identical source mask lines per R3Pair, each with left
            # then right asymmetric PF register phase.
            for _ in range(2):
                for phase in (halo[:3],halo[3:]):
                    n=sum(a!=b for a,b in zip(phase,prev_actual))
                    phase_hist[n]+=1
                    phase_events+=n
                    prev_actual=list(phase)

            hb=visible_pf(halo)
            sb=visible_pf(scenery)
            if any(hb) and any(sb):
                colour_coactive+=1
                if any(any(hb[t:t+20]) and any(sb[t:t+20])
                       for t in (0,20)):
                    colour_same_half+=1
                if any(a and b for a,b in zip(hb,sb)):
                    overlapping_bit_rows+=1
                    if first_overlap is None:
                        first_overlap={"pair":row_index,"R3_index":176-2*row_index,
                                       "x":xpos}
                for priority,hist in (("halo",priority_halo_hist),
                                      ("scenery",priority_scenery_hist)):
                    # Experimental priority choices, neither user authorised.
                    tags=[]
                    for a,b in zip(hb,sb):
                        if a and b:
                            tags.append("H" if priority=="halo" else "S")
                        elif a:
                            tags.append("H")
                        elif b:
                            tags.append("S")
                        else:
                            tags.append(".")
                    live=[t for t in tags if t!="."]
                    switches=sum(live[i]!=live[i-1] for i in range(1,len(live)))
                    hist[switches]+=1
        stats.append({
            "x":xpos,
            "two_line_pairs":88,
            "source_fields_changed_gt1":multi_count,
            "first_source_burst":first_mult,
            "minimum_PF_zero_page_store_events_in_original_asymmetric_phase_model":phase_events,
            "PF_register_writes_per_half_phase_histogram":dict(sorted(phase_hist.items())),
            "halo_and_scenery_both_nonempty_pairs":colour_coactive,
            "both_within_same_half_pairs":colour_same_half,
            "same_PF_pixel_cell_overlap_pairs":overlapping_bit_rows,
            "first_same_pixel_overlap":first_overlap,
            "colour_switch_lower_bound_HaloPriority":dict(sorted(priority_halo_hist.items())),
            "colour_switch_lower_bound_SceneryPriority":dict(sorted(priority_scenery_hist.items())),
        })
    # Hard negative controls on original-source data.
    assert len(stats)==13
    assert all(v["source_fields_changed_gt1"]>0 for v in stats)
    assert all(v["halo_and_scenery_both_nonempty_pairs"]==16 for v in stats)
    assert all(v["both_within_same_half_pairs"]==16 for v in stats)
    assert any(v["same_PF_pixel_cell_overlap_pairs"]>0 for v in stats)
    assert all(sum(v["PF_register_writes_per_half_phase_histogram"].values())==352 for v in stats)
    summary={
        "status":"SOURCE-ONLY NEGATIVE for direct simple 1-reg/2-lines on exact R3 masks; no full renderer acceptance",
        "source_github_blob_sha":DATA["origin_github_blob_sha"],
        "scope":"R3 synthetic HALO and SCENERY variants, not approved full game maps",
        "note":"Raw source 5-field differences and theoretical PF-register phase event counts are different measures. Physical writes in an actual 6507 kernel also have deadlines; STA-cycle, register setup and RAM not proven. Overlap priority is hypothetical.",
        "results":stats
    }
    (ROOT/"PF_REP1_RESULTS.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS: all source-only assertions", "x_positions":len(stats),
                      "min_burst":min(v["source_fields_changed_gt1"] for v in stats),
                      "max_burst":max(v["source_fields_changed_gt1"] for v in stats),
                      "dual_colour_source_pair_count_total":sum(v["halo_and_scenery_both_nonempty_pairs"] for v in stats),
                      "real_6507_timing":"NOT TESTED"},indent=2))
if __name__=="__main__":
    go()
