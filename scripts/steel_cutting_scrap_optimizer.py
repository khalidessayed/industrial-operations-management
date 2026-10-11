"""
Project : Heavy Formwork & Steel Fabrication - 1D Cutting Stock Optimizer
Author  : Eng. Khalid Mohamed Sayed
Domain  : Manufacturing Operations, Scaffolding & Steel Fabrication
Purpose : Solves the 1D Cutting Stock Problem (CSP) using First-Fit Decreasing
          heuristic to minimize off-cut scrap and calculate material utilization.
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CutRequirement:
    component_name: str
    length_mm: float
    quantity: int

class SteelCuttingOptimizer:
    def __init__(self, stock_length_mm: float = 6000.0, blade_kerf_mm: float = 5.0, cost_per_ton: float = 850.0):
        """
        stock_length_mm: Standard commercial raw steel pipe/profile length (Default: 6000 mm / 6m)
        blade_kerf_mm   : Saw blade thickness lost per cut (Default: 5 mm)
        cost_per_ton    : Steel cost estimate in USD or SAR per ton
        """
        self.stock_length = stock_length_mm
        self.blade_kerf = blade_kerf_mm
        self.cost_per_ton = cost_per_ton

    def optimize_cutting(self, requirements: List[CutRequirement]) -> Dict:
        # 1. Unroll all required parts
        all_pieces = []
        for req in requirements:
            all_pieces.extend([(req.length_mm, req.component_name)] * req.quantity)

        # 2. Sort descending (First-Fit Decreasing Algorithm)
        all_pieces.sort(key=lambda x: x[0], reverse=True)

        bars = []  # Each element is a list of cuts made from one standard bar

        for length, name in all_pieces:
            placed = False
            for bar in bars:
                current_used = sum(p[0] for p in bar) + (len(bar) * self.blade_kerf)
                if current_used + length <= self.stock_length:
                    bar.append((length, name))
                    placed = True
                    break
            
            if not placed:
                bars.append([(length, name)])

        # 3. Calculate Operational KPIs
        total_bars_used = len(bars)
        total_raw_material_mm = total_bars_used * self.stock_length
        total_finished_product_mm = sum(p[0] for p in all_pieces)
        total_kerf_loss_mm = sum((len(bar) - 1) * self.blade_kerf for bar in bars if len(bar) > 0)
        total_scrap_mm = total_raw_material_mm - (total_finished_product_mm + total_kerf_loss_mm)

        utilization_rate = (total_finished_product_mm / total_raw_material_mm) * 100
        scrap_rate = (total_scrap_mm / total_raw_material_mm) * 100

        return {
            "total_bars_needed": total_bars_used,
            "total_raw_meters": total_raw_material_mm / 1000.0,
            "net_product_meters": total_finished_product_mm / 1000.0,
            "scrap_meters": total_scrap_mm / 1000.0,
            "utilization_percentage": round(utilization_rate, 2),
            "scrap_percentage": round(scrap_rate, 2),
            "cutting_patterns": bars
        }

if __name__ == "__main__":
    # Example Case: Fabricating 20 Heavy-Duty Formwork Waler & Prop Assemblies
    optimizer = SteelCuttingOptimizer(stock_length_mm=6000.0, blade_kerf_mm=5.0)

    production_order = [
        CutRequirement(component_name="Formwork Soldier (Vertical)", length_mm=2750, quantity=24),
        CutRequirement(component_name="Steel Waler (Horizontal)",     length_mm=1800, quantity=30),
        CutRequirement(component_name="Diagonal Push-Pull Brace",    length_mm=1250, quantity=40),
        CutRequirement(component_name="Base Plate Spacer Sleeves",    length_mm=450,  quantity=60),
    ]

    results = optimizer.optimize_cutting(production_order)

    print("=" * 65)
    print(" 🏭 STEEL FABRICATION & FORMWORK - CUTTING OPTIMIZATION REPORT")
    print("=" * 65)
    print(f" Total Standard 6.0m Raw Bars Required : {results['total_bars_needed']} Bars")
    print(f" Total Raw Material Purchased          : {results['total_raw_meters']:.2f} m")
    print(f" Net Product Material Finished         : {results['net_product_meters']:.2f} m")
    print(f" Scrap / Off-cut Loss                  : {results['scrap_meters']:.2f} m")
    print(f" Material Utilization Rate             : {results['utilization_percentage']}%")
    print(f" Scrap Rate (Target < 4.0%)            : {results['scrap_percentage']}%")
    print("=" * 65)
