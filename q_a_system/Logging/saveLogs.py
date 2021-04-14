from q_a_system.global_pack import constant


def saveOneLog(question, log_var_name_entity_list, stringList, resourceList, keywordList, log_var_property_list, answer):
    insertRow = [question, log_var_name_entity_list, stringList, resourceList, keywordList, log_var_property_list, answer]
    constant.logsGSheet.insert_row(insertRow, 2)

