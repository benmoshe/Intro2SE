import pytest

# --- count: the pure logic ---


@pytest.mark.parametrize(
    ("text", "lines", "words", "chars"),
    [
        ("", 0, 0, 0),
        ("hello", 1, 1, 5),
        ("hello world\nfoo\n", 2, 3, 16),
        ("  spaced   out  \n", 1, 2, 17),
        ("a\n\nb\n", 3, 2, 5),
    ],
)
def test_count(impl, text, lines, words, chars):
    assert impl.count(text) == impl.Counts(lines=lines, words=words, chars=chars)


# --- main: the command-line interface ---


@pytest.fixture
def notes(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("hello world\nfoo\n")
    return str(path)


@pytest.fixture
def single(tmp_path):
    path = tmp_path / "single.txt"
    path.write_text("one\n")
    return str(path)


def test_prints_all_counts_by_default(impl, notes, capsys):
    assert impl.main([notes]) == 0
    assert capsys.readouterr().out == f"2 3 16 {notes}\n"


@pytest.mark.parametrize(
    ("flag", "expected"),
    [("--lines", "2"), ("--words", "3"), ("--chars", "16"), ("-l", "2"), ("-w", "3"), ("-c", "16")],
)
def test_single_flag_prints_only_that_count(impl, notes, capsys, flag, expected):
    assert impl.main([flag, notes]) == 0
    assert capsys.readouterr().out == f"{expected} {notes}\n"


def test_columns_keep_a_fixed_order_whatever_the_flag_order(impl, notes, capsys):
    impl.main(["--chars", "--lines", notes])
    assert capsys.readouterr().out == f"2 16 {notes}\n"


def test_flags_may_follow_the_file_names(impl, notes, capsys):
    impl.main([notes, "--words"])
    assert capsys.readouterr().out == f"3 {notes}\n"


def test_multiple_files_print_one_line_each(impl, notes, single, capsys):
    assert impl.main([notes, single]) == 0
    assert capsys.readouterr().out == f"2 3 16 {notes}\n1 1 4 {single}\n"


def test_missing_file_is_reported_on_stderr_with_exit_code_1(impl, tmp_path, capsys):
    missing = str(tmp_path / "nope.txt")

    assert impl.main([missing]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith(f"wordcount: {missing}: ")


def test_a_missing_file_does_not_stop_the_others(impl, tmp_path, notes, single, capsys):
    missing = str(tmp_path / "nope.txt")

    assert impl.main([notes, missing, single]) == 1

    captured = capsys.readouterr()
    assert captured.out == f"2 3 16 {notes}\n1 1 4 {single}\n"
    assert missing in captured.err


def test_no_arguments_is_a_usage_error(impl, capsys):
    with pytest.raises(SystemExit) as exit_info:
        impl.main([])
    assert exit_info.value.code == 2
    assert "usage" in capsys.readouterr().err.lower()


def test_help_describes_the_options(impl, capsys):
    with pytest.raises(SystemExit) as exit_info:
        impl.main(["--help"])
    assert exit_info.value.code == 0
    help_text = capsys.readouterr().out
    assert all(flag in help_text for flag in ["--lines", "--words", "--chars"])
