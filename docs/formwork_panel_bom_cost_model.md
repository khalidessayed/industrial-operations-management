# Heavy Modular Steel Formwork Panel (2.4m x 1.2m) - BOM & Costing Formework 📐

This document outlines the standard engineering **Bill of Materials (BOM)**, fabrication routing steps, and job-order costing breakdown used for manufacturing heavy-duty steel formwork wall panels.

---

## 1. Bill of Materials (BOM) Breakdown

| Item No | Component Description | Material Spec | Dimension / Cut Size | Qty | Unit Wt (kg) | Total Wt (kg) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **01** | Outer Frame Long Member | Rectangular Tube (RHS 100x50x3) | 2400 mm | 2 | 15.60 | 31.20 |
| **02** | Outer Frame Short Member | RHS 100x50x3 | 1100 mm | 2 | 7.15 | 14.30 |
| **03** | Internal Stiffener Ribs | Square Tube (SHS 50x50x2.5) | 1100 mm | 5 | 3.96 | 19.80 |
| **04** | Tie Rod Conical Sleeves | Cast Steel / Seamless Pipe | Ø28 mm x 100 mm | 4 | 0.85 | 3.40 |
| **05** | Corner Gusset Plates | Mild Steel Plate (t=6mm) | 120 x 120 mm | 4 | 0.68 | 2.72 |
| **06** | Facing Skin Sheet (Facing) | High-Strength Sheet (t=2.5mm) | 2400 x 1200 mm | 1 | 56.52 | 56.52 |
| **TOTAL**| **Total Raw Steel per Panel** | — | — | — | — | **127.94 kg** |

---

## 2. Fabrication Routing & Production Workflow

```mermaid
graph LR
    A[Raw Steel Pipes & Sheets] --> B[Cutting & Beveling]
    B --> C[Tack Welding & Fixture Jig Assembly]
    C --> D[Full GMAW/MIG Robotic/Manual Welding]
    D --> E[Quality Inspection & Dimensional Check]
    E --> F[Shot Blasting Sa 2.5]
    F --> G[Industrial Powder Coating / Paint]
    G --> H[Finished Goods Warehouse]
