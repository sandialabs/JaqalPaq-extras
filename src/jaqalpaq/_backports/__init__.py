# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.
import sys

__all__ = []

try:
    from pygsti.extras import interpygate
except ImportError:
    try:
        import pygsti
    except ImportError:
        pass
    else:
        from . import _interpygate as interpygate
        from ._interpygate import core, process_tomography

        sys.modules["pygsti.extras.interpygate"] = interpygate
        sys.modules["pygsti.extras.interpygate.core"] = core
        sys.modules["pygsti.extras.interpygate.process_tomography"] = process_tomography
        del core
        del process_tomography
        __all__.append("interpygate")
else:
    __all__.append("interpygate")
