t/render/project/src/.venv/lib/python3.12/site-packages/passlib/utils/handlers.py", line 2163, in set_backend
    return cls.set_backend(name, dryrun=dryrun)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/utils/handlers.py", line 2188, in set_backend
    cls._set_backend(name, dryrun)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/utils/handlers.py", line 2311, in _set_backend
    super(SubclassBackendMixin, cls)._set_backend(name, dryrun)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/utils/handlers.py", line 2224, in _set_backend
    ok = loader(**kwds)
         ^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/handlers/bcrypt.py", line 626, in _load_backend_mixin
    return mixin_cls._finalize_backend_mixin(name, dryrun)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/handlers/bcrypt.py", line 421, in _finalize_backend_mixin
    if detect_wrap_bug(IDENT_2A):
       ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/handlers/bcrypt.py", line 380, in detect_wrap_bug
    if verify(secret, bug_hash):
       ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/utils/handlers.py", line 792, in verify
    return consteq(self._calc_checksum(secret), chk)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/passlib/handlers/bcrypt.py", line 655, in _calc_checksum
    hash = _bcrypt.hashpw(secret, config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])