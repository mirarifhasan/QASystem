from q_a_system.global_pack import constant


def saveOneLog(content):
    insertRow = content
    constant.logsGSheet.insert_row(insertRow, 2)

