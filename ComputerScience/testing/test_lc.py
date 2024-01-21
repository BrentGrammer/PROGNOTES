from testing.lc import minWindow


def test_min_window_handles_too_long_input():
    result = minWindow('a','aa')
    assert result == ""

def test_min_window_handles_empty_t_string():
    result = minWindow('a','')
    assert result == ""

def test_min_window_handles_matching_string():
    result = minWindow('ab','ab')
    assert result == "ab"

def test_min_window_handles_same_len_strs_not_ordered():
    result = minWindow('ab','ba')
    assert result == "ab"

def test_min_window_handles_substring_out_of_order():
    result = minWindow('abc','cb')
    assert result == "bc"