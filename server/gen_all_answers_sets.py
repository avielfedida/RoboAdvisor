from sqlalchemy import create_engine
from sqlalchemy.orm import create_session


template = '''
INSERT INTO public.answers_sets(
	ans_set_val, ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8, risk)
	VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {});
'''

e = create_engine('postgresql+psycopg2://postgres:16941694@127.0.0.1:5432/robo_advisor')
session = create_session(bind=e, autocommit=False, autoflush=True)



def run_me():
    for risk in range(1,5+1):
        for ans_1 in range(1,6+1):
            for ans_2 in range(1,4+1):
                for ans_3 in range(1,3+1):
                    for ans_4 in range(1, 3+1):
                        for ans_5 in range(1,5+1):
                            for ans_6 in range(1,5+1):
                                for ans_7 in range(1,5+1):
                                    for ans_8 in range(1,4+1):
                                        # print(
                                        #     template.format("'{}_{}_{}_{}_{}_{}_{}_{}'".format(ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8),
                                        #                     ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8, risk)
                                        # )
                                        #
                                        new_answers_set = AnswersSet(ans_set_val="{}_{}_{}_{}_{}_{}_{}_{}".format(ans_1, ans_2, ans_3, ans_4, ans_5, ans_6, ans_7, ans_8),
                                                                     ans_1=str(ans_1),
                                                                     ans_2=str(ans_2),
                                                                     ans_3=str(ans_3),
                                                                     ans_4=str(ans_4),
                                                                     ans_5=str(ans_5),
                                                                     ans_6=str(ans_6),
                                                                     ans_7=str(ans_7),
                                                                     ans_8=str(ans_8),
                                                                     risk=risk)
                                        session.add(new_answers_set)
    session.commit()

if __name__ == '__main__':
    run_me()