class valid_data():
    MUST_EXIST =    ["WIDTH",
                    "HEIGHT",
                    "ENTRY",
                    "EXIT",
                    "OUTPUT_FILE",
                    "PERFECT"]

    BONUS       =     ["SEED",
                       "LOG_FILE"] #must heck the validation of log file

    INVALID_FILES = []

    PERFECT_VALUES = ["TRUE",
                      "FALSE",
                      "1",
                      "0",
                      "-0",
                      "+0",
                      "+1"]