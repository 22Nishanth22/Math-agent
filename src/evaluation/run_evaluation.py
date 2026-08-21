def classify_result(item):
    if item["error"]:
        return "error"

    expected = item["expected_tool"]
    called = set(item["tools_called"])

    retrieval_tool_name = "search_math_knowledge"
    compute_tool_name = "equations"

    if not called:
        return "no_tool"

    if expected == "retrieval":
        correct = called == {retrieval_tool_name}
    elif expected == "compute":
        correct = called == {compute_tool_name}
    elif expected == "both":
        correct = {retrieval_tool_name, compute_tool_name}.issubset(called)
    else:
        correct = False

    return "correct" if correct else "wrong_tool"


def score_evaluation(results):
    from collections import Counter

    labels = [classify_result(r) for r in results]
    counts = Counter(labels)

    total = len(results)
    accuracy = counts.get("correct", 0) / total

    return {
        "total": total,
        "accuracy": accuracy,
        "breakdown": dict(counts)
    }
