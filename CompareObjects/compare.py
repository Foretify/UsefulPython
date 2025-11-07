from difflib import SequenceMatcher
import json
import math

def compare_objects(obj1, obj2):
    results = {}

    # 1️⃣ Direct Equality
    results["direct_equality"] = obj1 == obj2

    # 2️⃣ Type Comparison
    results["same_type"] = type(obj1) == type(obj2)
    results["type_info"] = (type(obj1).__name__, type(obj2).__name__)

    # 3️⃣ Similarity Score (string-based or JSON structure)
    try:
        str1 = json.dumps(obj1, sort_keys=True)
        str2 = json.dumps(obj2, sort_keys=True)
    except TypeError:
        str1, str2 = str(obj1), str(obj2)
    
    results["similarity_score"] = round(SequenceMatcher(None, str1, str2).ratio(), 3)

    # 4️⃣ Set-based Comparison (for lists, tuples, or dict keys)
    set1 = set(obj1) if isinstance(obj1, (list, tuple, set)) else set(getattr(obj1, "keys", lambda: [])())
    set2 = set(obj2) if isinstance(obj2, (list, tuple, set)) else set(getattr(obj2, "keys", lambda: [])())

    results["set_intersection"] = list(set1 & set2)
    results["set_difference"] = {
        "only_in_obj1": list(set1 - set2),
        "only_in_obj2": list(set2 - set1)
    }

    # 5️⃣ Structural Comparison (recursive depth or length)
    try:
        len1, len2 = len(obj1), len(obj2)
        results["length_difference"] = abs(len1 - len2)
    except TypeError:
        results["length_difference"] = math.nan

    return results


# 🧪 Example usage
if __name__ == "__main__":
    obj_a = {"name": "Lyle", "age": 40, "skills": ["Python", "GIS"]}
    obj_b = {"name": "Lyle", "age": 41, "skills": ["Python", "AI"]}

    comparison = compare_objects(obj_a, obj_b)
    for k, v in comparison.items():
        print(f"{k}: {v}")
    
    number_a = {"15"}
    number_b = {"20"}

    print(f"================================")

    comparison = compare_objects(number_a, number_b)
    for k, v in comparison.items():
        print(f"{k}: {v}")

    string_a = {"sample"}
    string_b = {"Sample"}

    print(f"================================")

    comparison = compare_objects(string_a, string_b)
    for k, v in comparison.items():
        print(f"{k}: {v}")
    
    string_a = {"sample"}
    string_b = {"sample a"}

    print(f"================================")

    comparison = compare_objects(string_a, string_b)
    for k, v in comparison.items():
        print(f"{k}: {v}")


