"""
Project : Heavy Modular Formwork Fabrication - Cost & KPI Engine
Author  : Eng. Khalid Mohamed Sayed
Domain  : Cost Control, Job-Order Costing & Operational KPIs
File    : formwork_job_costing_engine.py
Description:
    Calculates direct/indirect manufacturing costs, batch totals,
    unit cost per formwork panel, and validates actual shop-floor KPIs
    against standard targets.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class JobOrderCostParameters:
    batch_size: int = 100  # Number of panels in the production run
    steel_tons: float = 12.79  # Total structural steel weight
    steel_price_per_ton: float = 3400.0  # SAR per ton
    cutting_fitup_hours: float = 180.0  # Total man-hours
    labor_rate_per_hour: float = 35.0  # SAR per man-hour
    welding_consumables_cost: float = 1850.0  # Gas + Wire (ER70S-6)
    paint_cost_per_panel: float = 45.0  # SAR per panel
    factory_overhead_per_panel: float = 35.0  # Machine depreciation & utilities


class FormworkCostEngine:
    def __init__(self, params: JobOrderCostParameters):
        self.p = params

    def calculate_cost_breakdown(self) -> Dict[str, Any]:
        """Calculates itemized costs and percentage share of total cost."""
        # 1. Direct Material Costs
        direct_steel_cost = self.p.steel_tons * self.p.steel_price_per_ton
        direct_consumables = self.p.welding_consumables_cost
        total_material = direct_steel_cost + direct_consumables

        # 2. Direct Labor Costs
        direct_labor_cost = self.p.cutting_fitup_hours * self.p.labor_rate_per_hour

        # 3. Surface Treatment & Painting
        total_paint_cost = self.p.batch_size * self.p.paint_cost_per_panel

        # 4. Factory Overhead (FOH)
        total_overhead_cost = self.p.batch_size * self.p.factory_overhead_per_panel

        # Total Manufacturing Cost
        total_mfg_cost = (
            total_material + direct_labor_cost + total_paint_cost + total_overhead_cost
        )
        cost_per_unit = total_mfg_cost / self.p.batch_size

        return {
            "batch_size": self.p.batch_size,
            "direct_steel": direct_steel_cost,
            "welding_consumables": direct_consumables,
            "direct_labor": direct_labor_cost,
            "surface_paint": total_paint_cost,
            "factory_overhead": total_overhead_cost,
            "total_batch_cost": total_mfg_cost,
            "unit_cost_sar": round(cost_per_unit, 2),
            "cost_shares": {
                "steel_share_pct": round((direct_steel_cost / total_mfg_cost) * 100, 2),
                "labor_share_pct": round((direct_labor_cost / total_mfg_cost) * 100, 2),
                "other_share_pct": round(
                    ((direct_consumables + total_paint_cost + total_overhead_cost) / total_mfg_cost) * 100,
                    2,
                ),
            },
        }

    @staticmethod
    def audit_production_kpis(
        actual_cycle_time_mins: float,
        actual_scrap_rate_pct: float,
        actual_diagonal_tol_mm: float,
    ) -> Dict[str, Any]:
        """
        Audits actual shop-floor performance against standard KPIs:
        - Cycle Time: Target <= 45 mins/panel
        - Scrap Rate: Target <= 3.5%
        - Diagonal Tolerance: Target <= +/- 1.0 mm
        """
        targets = {
            "cycle_time_target": 45.0,
            "scrap_target": 3.5,
            "tolerance_target": 1.0,
        }

        evaluations = {
            "cycle_time_status": (
                "PASS" if actual_cycle_time_mins <= targets["cycle_time_target"] else "DELAY"
            ),
            "scrap_status": (
                "PASS" if actual_scrap_rate_pct <= targets["scrap_target"] else "EXCEEDED"
            ),
            "tolerance_status": (
                "PASS" if abs(actual_diagonal_tol_mm) <= targets["tolerance_target"] else "OUT_OF_SPEC"
            ),
        }

        return {"targets": targets, "status": evaluations}


def print_executive_report(cost_data: Dict[str, Any], kpi_data: Dict[str, Any]):
    print("=" * 70)
    print(" 🏭 JOB-ORDER COST SHEET & PRODUCTION KPI AUDIT REPORT")
    print(f" Order Scope: Batch of {cost_data['batch_size']} Formwork Wall Panels")
    print("=" * 70)
    print(f" 1. Direct Raw Material (Steel)      : SAR {cost_data['direct_steel']:>10,.2f} ({cost_data['cost_shares']['steel_share_pct']}%)")
    print(f" 2. Cutting & Fit-up Labor            : SAR {cost_data['direct_labor']:>10,.2f} ({cost_data['cost_shares']['labor_share_pct']}%)")
    print(f" 3. Welding Consumables (ER70S-6+Gas) : SAR {cost_data['welding_consumables']:>10,.2f}")
    print(f" 4. Surface Preparation & Paint       : SAR {cost_data['surface_paint']:>10,.2f}")
    print(f" 5. Factory Overhead (Depr. & Power)  : SAR {cost_data['factory_overhead']:>10,.2f}")
    print("-" * 70)
    print(f" TOTAL MANUFACTURING COST (BATCH)     : SAR {cost_data['total_batch_cost']:>10,.2f}")
    print(f" TARGET UNIT COST PER PANEL           : SAR {cost_data['unit_cost_sar']:>10,.2f} / Unit")
    print("=" * 70)
    print(" 📊 OPERATIONAL KPI EVALUATION")
    print("-" * 70)
    print(f" Cycle Time per Unit : [Target <= {kpi_data['targets']['cycle_time_target']}m]  --> Status: {kpi_data['status']['cycle_time_status']}")
    print(f" Raw Steel Scrap %   : [Target <= {kpi_data['targets']['scrap_target']}%]   --> Status: {kpi_data['status']['scrap_status']}")
    print(f" Diagonal Tolerance  : [Target <= +-{kpi_data['targets']['tolerance_target']}mm] --> Status: {kpi_data['status']['tolerance_status']}")
    print("=" * 70)


if __name__ == "__main__":
    # 1. Initialize with standard baseline parameters from Job-Order Sheet
    job_params = JobOrderCostParameters(
        batch_size=100,
        steel_tons=12.79,
        steel_price_per_ton=3400.0,
        cutting_fitup_hours=180.0,
        labor_rate_per_hour=35.0,
        welding_consumables_cost=1850.0,
        paint_cost_per_panel=45.0,
        factory_overhead_per_panel=35.0,
    )

    engine = FormworkCostEngine(job_params)
    cost_summary = engine.calculate_cost_breakdown()

    # 2. Audit sample shop-floor execution data
    kpi_audit = engine.audit_production_kpis(
        actual_cycle_time_mins=43.5,
        actual_scrap_rate_pct=3.1,
        actual_diagonal_tol_mm=0.8,
    )

    # 3. Print Output
    print_executive_report(cost_summary, kpi_audit)
