"""Closed-form pharmacokinetic calculations.

Covers one-compartment IV bolus disposition, the elimination-rate /
half-life relationship, clearance, loading dose, multiple-dose steady
state, and a two-compartment bi-exponential model.

Rate constants are in 1/h, half-lives and the dosing interval tau in h,
volumes (Vd) in L, doses in the same mass unit you want concentrations
reported in (e.g. mg gives mg/L). f is the bioavailable fraction (0-1).
"""

from math import log, exp

__version__ = "0.6.5"

__all__ = [
    "ke_from_half_life",
    "half_life",
    "concentration",
    "clearance",
    "loading_dose",
    "steady_state_peak",
    "accumulation_ratio",
    "two_compartment",
]

LN2 = log(2.0)


def ke_from_half_life(t_half):
    """Elimination rate constant ke (1/h) for a given half-life (h)."""
    if t_half <= 0:
        raise ValueError("t_half must be positive")
    return LN2 / t_half


def half_life(ke):
    """Half-life (h) implied by an elimination rate constant ke (1/h)."""
    if ke <= 0:
        raise ValueError("ke must be positive")
    return LN2 / ke


def concentration(dose, vd, ke, t):
    """Plasma concentration at time t after a single IV bolus.

    C(t) = (dose / Vd) * exp(-ke * t), so at t=0 it collapses to the
    initial concentration dose/Vd.
    """
    if vd <= 0:
        raise ValueError("vd must be positive")
    return dose / vd * exp(-ke * t)


def clearance(ke, vd):
    """Clearance (L/h) as the product of ke (1/h) and Vd (L)."""
    return ke * vd


def loading_dose(target, vd, f=1.0):
    """Loading dose needed to reach a target concentration.

    For an IV bolus leave f at its default of 1; for extravascular
    routes pass the bioavailable fraction.
    """
    if f <= 0:
        raise ValueError("f must be positive")
    return target * vd / f


def steady_state_peak(dose, vd, ke, tau):
    """Peak steady-state concentration for repeated IV bolus dosing.

    With a dose given every tau hours the peaks accumulate to
    (dose/Vd) / (1 - exp(-ke*tau)); the denominator is the reciprocal
    of the accumulation ratio.
    """
    if vd <= 0:
        raise ValueError("vd must be positive")
    if ke <= 0 or tau <= 0:
        raise ValueError("ke and tau must be positive")
    return (dose / vd) / (1 - exp(-ke * tau))


def accumulation_ratio(ke, tau):
    """Steady-state accumulation ratio for a dosing interval tau (h).

    Equal to 1 / (1 - exp(-ke*tau)); it tends to 1 for very long
    intervals and grows as doses are stacked more frequently.
    """
    if ke <= 0 or tau <= 0:
        raise ValueError("ke and tau must be positive")
    return 1.0 / (1 - exp(-ke * tau))


def two_compartment(dose, A, alpha, B, beta, t):
    """Bi-exponential disposition for a two-compartment model.

    C(t) = dose * (A*exp(-alpha*t) + B*exp(-beta*t)), where alpha is the
    distribution rate and beta the (slower) terminal rate. A and B are
    the unit-dose intercept coefficients.
    """
    return dose * (A * exp(-alpha * t) + B * exp(-beta * t))
