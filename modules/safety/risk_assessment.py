def calculate_risk_score(likelihood: float, consequence: float) -> float:
    """Return risk score as likelihood × consequence."""
    return float(likelihood) * float(consequence)


def classify_risk(score: float) -> str:
    """Classify the risk score into low, medium, high, or critical."""
    if 1 <= score <= 4:
        return "Low"
    if 5 <= score <= 9:
        return "Medium"
    if 10 <= score <= 16:
        return "High"
    if 17 <= score <= 25:
        return "Critical"
    return "Low"


def risk_warning_required(score: float) -> bool:
    """Return True if the score is high-visibility and should trigger a warning."""
    return score >= 10
