#!/usr/bin/env python3
"""
目標受注数から必要流入を逆算する簡易シミュレーター。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def calc_required_visits(
    target_deals: float,
    consult_to_deal_rate: float,
    lead_to_consult_rate: float,
    visit_to_lead_rate: float,
) -> tuple[int, int, int]:
    if consult_to_deal_rate <= 0 or lead_to_consult_rate <= 0 or visit_to_lead_rate <= 0:
        raise ValueError("all rates must be > 0")

    required_consults = target_deals / consult_to_deal_rate
    required_leads = required_consults / lead_to_consult_rate
    required_visits = required_leads / visit_to_lead_rate
    return (
        int(round(required_visits)),
        int(round(required_leads)),
        int(round(required_consults)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="受注目標から必要流入を逆算")
    parser.add_argument("--target-deals", type=float, default=5.0)
    parser.add_argument("--consult-to-deal", type=float, default=0.25, help="相談->受注率")
    parser.add_argument("--lead-to-consult", type=float, default=0.40, help="リード->相談率")
    parser.add_argument("--visit-to-lead", type=float, default=0.025, help="流入->リード率")
    parser.add_argument("--output")
    args = parser.parse_args()

    visits, leads, consults = calc_required_visits(
        args.target_deals,
        args.consult_to_deal,
        args.lead_to_consult,
        args.visit_to_lead,
    )

    result = {
        "target_deals": args.target_deals,
        "assumptions": {
            "consult_to_deal": args.consult_to_deal,
            "lead_to_consult": args.lead_to_consult,
            "visit_to_lead": args.visit_to_lead,
        },
        "required_monthly": {
            "visits": visits,
            "leads": leads,
            "consultations": consults,
            "deals": int(round(args.target_deals)),
        },
    }

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"output={out}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

