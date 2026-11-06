import json

import config
from agent import run_agent
from rag import NO_ANSWER

TESTS_PATH = config.PROJECT_DIR / "data" / "test_questions.json"


def check_answer(test, result):
    if not test["answerable"]:
        return result["answer"] == NO_ANSWER

    if result["answer"] == NO_ANSWER:
        return False

    answer = result["answer"].replace(",", "")
    for word in test["must_contain"]:
        if word.replace(",", "") not in answer:
            return False
    return True


def check_search(test, result):
    for passage in result["passages"]:
        if passage["source"] == test["expected_source"]:
            return True
    return False


def run_evaluation():
    tests = json.loads(TESTS_PATH.read_text(encoding="utf-8"))

    answerable_total = 0
    answerable_correct = 0
    search_hits = 0
    unanswerable_total = 0
    unanswerable_correct = 0

    for test in tests:
        result = run_agent(test["question"], test["role"])
        answer_ok = check_answer(test, result)

        if test["answerable"]:
            answerable_total += 1
            if answer_ok:
                answerable_correct += 1
            if check_search(test, result):
                search_hits += 1
        else:
            unanswerable_total += 1
            if answer_ok:
                unanswerable_correct += 1

        status = "PASS" if answer_ok else "FAIL"
        print(f"{test['id']}. {status}  [{test['role']}] {test['question']}")
        if not answer_ok:
            print("      got:", result["answer"])
            print("      searched:", result["searches"])

    total_correct = answerable_correct + unanswerable_correct
    total = answerable_total + unanswerable_total

    print()
    print("========== RESULTS ==========")
    print(f"Answer accuracy:        {answerable_correct}/{answerable_total}"
          f"  ({round(100 * answerable_correct / answerable_total)}%)")
    print(f"Search hit rate:        {search_hits}/{answerable_total}"
          f"  ({round(100 * search_hits / answerable_total)}%)")
    print(f"'I don't know' correct: {unanswerable_correct}/{unanswerable_total}"
          f"  ({round(100 * unanswerable_correct / unanswerable_total)}%)")
    print(f"Overall:                {total_correct}/{total}"
          f"  ({round(100 * total_correct / total)}%)")


if __name__ == "__main__":
    run_evaluation()