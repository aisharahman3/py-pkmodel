# Changelog

## 0.6.5 - 2025-01-18
- Added `__version__` and `__all__`; documented units (1/h, h, L, fraction) on every function.
- Guard against non-positive `t_half`, `ke`, `vd`, and `tau` to avoid division-by-zero on invalid input.

## 0.6.0 - 2024-05-02
- Added `two_compartment` for bi-exponential disposition.

## 0.5.0 - 2023-11-10
- Added `accumulation_ratio`; factored it out of `steady_state_peak`.

## 0.4.0 - 2023-06-21
- Added `steady_state_peak` for repeated IV bolus dosing.

## 0.3.0 - 2023-02-14
- Added `loading_dose` with a bioavailable-fraction parameter.

## 0.2.0 - 2022-09-30
- Added `clearance` and the `ke`/half-life conversions.

## 0.1.0 - 2022-06-05
- Initial public release: one-compartment IV bolus `concentration`.
