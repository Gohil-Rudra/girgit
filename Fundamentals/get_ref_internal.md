> get_ref_internal is the key here. When we **commit**:

- We try to advance HEAD using update_ref
- get_ref_internal() reads HEAD and sees it contains "ref: refs/heads/branch1". This means it's a symbolic ref.
- Since deref=True, _get_ref_internal recursively reads refs/heads/branch1 and returns its path.
- Therefore we actually update refs/heads/branch1.
- And HEAD is still pointing to refs/heads/branch1 !