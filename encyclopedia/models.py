from django.db import models

# Create your models here.
def is_substring(string, substring):
    # checking if the words are exactly the same
    if string == substring:
        return False
    
    # declaring variables
    sub_char_indicator = 0
    str_char_indicator = 0
    success = 0
    fail = 0
    
    # ''1'' loop over substring chars
    for sub_char in substring:
        # ''3'' loop over string chars
        for str_char in string:
            # ''4'' if first character in the substring
            if sub_char_indicator == 0:
                # ''4.1'' string char indicator
                str_char_indicator += 1
                # ''4.2'' compare the sub_char and str_char
                if sub_char == str_char:
                    success += 1
                    break
            
            # ''5'' if not the first character in the substring
            else:
                # ''5.1''
                if str_char_indicator == len(string):
                    fail += 1
                    break
                if sub_char == string[str_char_indicator]:
                    str_char_indicator += 1
                    success += 1
                    break
                else:
                    fail += 1

        # ''2'' substring char indicator
        sub_char_indicator += 1

    if success > 0 and fail == 0:
        return True
    else:
        return False
