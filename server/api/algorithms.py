def updated_risk_keys(old):
    return {
        2: 3,
        3: 4,
        4: 5,
        5: 7,
        6: 8,
        7: 9,
        8: 10
    }[old]


def horizon_score(question, answer):
    score_map = {
        #         1: {
        #             1: 0,
        #             2: 1,
        #             3: 3,
        #             4: 6,
        #             5: 9,
        #             6: 11
        #         },
        1: {
            1: 0,
            2: 2,  # Added 2-1
            3: 6,  # Added 4-1
            4: 10,  # Added 5-1
            5: 14,  # Added 6-1
            6: 15
        },
        2: {
            1: 0,
            2: 2,
            3: 4,
            4: 5,
            5: 6
        }
    }
    if question not in score_map:
        raise Exception(f'Unknown horizon question {str(question)}')
    return score_map[question][answer]


def risk_score(question, answer):
    score_map = {
        3: {
            1: 13,
            2: 8,
            3: 5,
            4: 3
        },
        4: {
            1: 5,  # Added 1
            2: 10,  # Added 3
            3: 15  # Added 4
        },
        5: {
            1: 6,  # Added 2
            2: 9,  # Added 2
            3: 15  # Added 4
        },
        6: {
            1: 3,
            2: 5,
            3: 8,
            4: 13
        },
        7: {
            1: 0,
            2: 4,
            3: 7,
            4: 11,
            5: 17  # Added 4
        },
        8: {
            1: 0,
            2: 4,
            3: 7,
            4: 11,
            5: 17  # Added 4
        },
        9: {
            1: 0,
            2: 4,
            3: 7,
            4: 11,
            5: 17  # Added 4
        },
        10: {
            1: 14,  # Added 1
            2: 8,
            3: 5,
            4: 3
        }
    }
    if question not in score_map:
        raise Exception(f'Unknown risk question {str(question)}')
    return score_map[question][answer]


def total_score(hs, rs):
    if hs < 1:
        return None
    if 1 <= hs < 3:
        return 1
    if 3 <= hs < 6:
        if rs < 24:
            return 1
        return 2
    if 6 <= hs < 8:
        if rs < 24:
            return 1
        if rs < 44:
            return 2
        return 3
    if 8 <= hs < 11:
        if rs < 24:
            return 1
        if rs < 44:
            return 2
        if rs < 65:
            return 3
        return 4
    # rs >= 11
    if rs < 24:
        return 1
    if rs < 44:
        return 2
    if rs < 65:
        return 3
    if rs < 85:
        return 4
    return 5


def get_risk_horizon_score(answers_dict):
    horizon_qa = {q: a for q, a in answers_dict.items() if q == 1}
    risk_qa = {updated_risk_keys(q): a for q, a in answers_dict.items() if q != 1}
    hs = sum([horizon_score(q, a) for q, a in horizon_qa.items()])
    rs = sum([risk_score(q, a) for q, a in risk_qa.items()])
    return total_score(hs, rs)


def check_if_all_questions_with_answers(dict_variable):
    all_questions_dict = {}
    for question_num in dict_variable.keys():
        if type(dict_variable[question_num]) == int:
            all_questions_dict[question_num] = True
        else:
            all_questions_dict[question_num] = False
    all_values = all_questions_dict.values()
    if not any(all_values):
        return "You didn't answer on one or more questions. Please start again"
    else:
        return None
