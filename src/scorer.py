def score_email(features, llm_result):
    """
    Combine rule-based features and LLm output into a final phishing score.
    """
    
    feature_score = calculate_feature_score(features)
    llm_score = extract_llm_score(llm_result)

    final_score = feature_score + llm_score
    risk_level = get_risk_level(final_score)
    final_verdict = get_final_verdict(risk_level)

    return {
        "feature_score": feature_score,
        "llm_score": llm_score,
        "final_score": final_score,
        "risk_level": risk_level,
        "final_verdict": final_verdict
    }

def calculate_feature_score(features):
    """
    Assign points based on extracted rule-based features.
    Link alone should not dominate the score.
    """

    score = 0

    num_keywords = features.get("num_suspicious_keywords", 0)
    num_links = features.get("num_links", 0)

    score += num_keywords * 8

    if features.get("has_urgency"):
        score += 15

    # links alone are weak, but links + keywords are stronger
    if num_links > 0 and num_keywords > 0:
        score += 10
    elif num_links > 0:
        score += 5

    if num_links >= 5:
        score += 10

    if features.get("has_generic_greeting"):
        score += 10

    return score

def extract_llm_score(llm_result):
    """
    Convert LLM risk level into a numberic score.
    """

    llm_result_lower = llm_result.lower()

    if "risk level: high" in llm_result_lower:
        return 40
    elif "risk level: medium" in llm_result_lower:
        return 25
    elif "risk level: low" in llm_result_lower:
        return 10

    return 0

def get_risk_level(final_score):
    """
    Convert numeric score into risk category.
    """

    if final_score >= 70:
        return "High"
    elif final_score >= 35:
        return "Medium"
    return "Low"

def get_final_verdict(risk_level):
    """
    Convert risk category into final verdict.
    """

    if risk_level == "High":
        return "Phishing"
    elif risk_level == "Medium":
        return "Suspicious"
    return "Legitimate"
