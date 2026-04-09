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
    """

    score = 0
    score += features.get("num_suspicious_keywords", 0) * 10

    if features.get("has_urgency"):
        score += 15

    if features.get("has_links"):
        score += 15

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
    elif final_score >= 40:
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
