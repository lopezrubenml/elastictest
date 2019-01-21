import pandas as pd
from pandas import DataFrame
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def match_func_no_counter(test_user, list_db, name_param, doc_param, site_param):
    import pandas as pd
    from pandas import DataFrame
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    res_df = DataFrame()
    df1_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_name), list_db.list_name, scorer = fuzz.partial_ratio))
    res_df['name_score'] = df1_[1]
    df2_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_doc), list_db.list_doc, scorer = fuzz.ratio))
    res_df['doc_score'] = df2_[1]
    df3_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_country), list_db.list_country))
    res_df['country_score'] = df3_[1]
    res_df['final_score'] = (res_df.name_score * name_param) + (res_df.doc_score * doc_param) + (res_df.country_score * site_param)
    return res_df


def match_func_with_counter(test_user, list_db, name_param, doc_param, site_param, name_function):
    res_df = DataFrame()
    df1_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_name), list_db.list_name))
    res_df['name_score'] = df1_[1]
    df2_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_doc), list_db.list_doc, scorer = fuzz.ratio))
    res_df['doc_score'] = df2_[1]
    df3_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_country), list_db.list_country))
    res_df['country_score'] = df3_[1]
    res_df['counter'] = list_db.counter
    res_df['final_score'] = (res_df.name_score * name_param * name_function(res_df.counter)) + (res_df.doc_score * doc_param) + (res_df.country_score * site_param)
    return res_df