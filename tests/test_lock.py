import os.path
import pytest

from conda.lock import Locked, LockError


def test_lock_passes(tmpdir):
    file_tmp = "conda_file_1"
    with Locked(tmpdir.strpath, file_tmp) as lock:
        path = os.path.basename(lock.lock_path)
        assert tmpdir.join(path).exists() and tmpdir.join(path).isfile()

    # lock should clean up after itself
    assert not tmpdir.join(path).exists()
    assert not tmpdir.exists()

def test_lock_locks(tmpdir):

    file_tmp = "conda_file_2"
    with Locked(tmpdir.strpath, file_tmp) as lock1:
        path = os.path.basename(lock1.lock_path)
        assert tmpdir.join(path).exists() and tmpdir.join(path).isfile()

        with pytest.raises(LockError) as execinfo:
            with Locked(tmpdir.strpath, file_tmp, retries=1) as lock2:
                assert False  # this should never happen
            assert lock2.lock_path == lock1.lock_path
        assert "LOCKERROR" in str(execinfo)
        assert "conda is already doing something" in str(execinfo)

        assert tmpdir.join(path).exists() and tmpdir.join(path).isfile()

    # lock should clean up after itself
    assert not tmpdir.join(path).exists()
    assert not tmpdir.exists()
