# Review notes for `review_me.py`

Try the exercise before reading this.

## Blocking — security

1. **SQL injection in `add_user` and `find_user`.** Both build SQL by string
   formatting. A name such as `x' OR '1'='1` changes the query's meaning.
   Use parameters: `db.execute("... WHERE name = ?", (name,))`.

2. **Backdoor password in `check_login`.** Anyone who supplies
   `ADMIN_PASSWORD` is logged in as *any* existing user. Remove the branch entirely.

3. **Hard-coded secret.** `ADMIN_PASSWORD = "hunter2"` is in source control,
   so it's known to everyone with repository access, forever. Secrets come
   from the environment (module 08) — and this one must now be considered leaked.

4. **Passwords hashed with unsalted MD5.** MD5 is fast and broken for this
   purpose; identical passwords produce identical hashes. Use a slow, salted
   password hash: `hashlib.scrypt`, or a library such as `argon2-cffi`.

5. **Plaintext password printed.** `check_login` prints the password a user
   typed. Never output credentials, to stdout or to logs. Use `logging`, and
   log only the name.

6. **Hash compared with `==`.** Comparison time leaks how many leading
   characters match. Use `hmac.compare_digest`.

## Blocking — correctness

7. **Mutable default argument.** `roles=[]` is created once and shared by
   every call, so each new user accumulates the roles of all previous ones.
   Use `roles=None` and build a new list inside. The function also mutates a
   list the caller passed in — copy it instead.

8. **Bare `except: pass` in `find_user`.** Every failure — a missing table, a
   locked database, a typo in the SQL, even Ctrl-C — is silently turned into
   "user not found". Let unexpected errors propagate.

9. **File never closed in `export_users`.** If a write fails the handle
   leaks, and buffered data may never be flushed. Use `with open(...) as f:`.

10. **Hand-rolled CSV.** A name or role containing a comma or newline
    corrupts the output; roles are already comma-joined, so every multi-role
    user breaks the format. Use the `csv` module.

## Design

11. **Module-level database connection.** `db` is opened at import time, so
    importing the module has a side effect, the path can't be configured, and
    nothing can be tested without touching a real `users.db`. Pass a
    connection in (modules 03 and 07).

12. **Storage, authentication and export in one module.** Three reasons to
    change. Separate them once the fixes above are in.

## Nits

13. `user == None` should be `user is None`.
14. `list` shadows the built-in; `h`, `f`, `i` say nothing. Prefer
    `for name, roles in rows:` to indexing with `range(len(...))`.
15. No type hints or docstrings; `add_user` returning the roles list is surprising.
16. A line well over 100 characters — the formatter would have fixed it.

## What a good review looks like here

The six security problems come first and block the merge on their own. A
review that spent its comments on naming and line length, and missed the SQL
injection, would have failed at its main job. Lead with what matters most.
