# ***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
# ***************************************************************************************************
from pygsti.tools.basisconstructors import (
    _basisConstructorDict,
    _check_dim,
    MatrixBasisConstructor,
    mut,
)


def col_matrices(matrix_dim):
    """
    Get the elements of the matrix unit, or "column-stacked", basis of matrix-dimension `matrix_dim`.
    The matrices are ordered so that the column index changes the fastest.

    Constructs the standard basis spanning the density-matrix space given by
    `matrix_dim` x `matrix_dim` matrices.

    The returned matrices are orthonormal basis under
    the trace inner product, i.e. Tr( dot(Mi,Mj) ) == delta_ij.

    Parameters
    ----------
    matrix_dim : int
        matrix dimension of the density-matrix space, e.g. 2
        for a single qubit in a 2x2 density matrix basis.

    Returns
    -------
    list
        A list of N numpy arrays each of shape (matrix_dim, matrix_dim).

    Notes
    -----
    Each element is a matrix containing
    a single "1" entry amidst a background of zeros.
    """
    _check_dim(matrix_dim)
    basisDim = matrix_dim ** 2

    mxList = []
    for row_index in range(matrix_dim):
        for col_index in range(matrix_dim):
            mxList.append(mut(col_index, row_index, matrix_dim))
    assert len(mxList) == basisDim
    return mxList


def col_labels(matrix_dim):
    """
    Return the column-stacked-matrix-basis labels based on a matrix dimension.

    Parameters
    ----------
    matrix_dim : int
        The matrix dimension of the basis to generate labels for (the
        number of rows or columns in a matrix).

    Returns
    -------
    list of strs
    """
    if matrix_dim == 0:
        return []
    if matrix_dim == 1:
        return [""]  # special case - use empty label instead of "I"
    return ["(%d,%d)" % (j, i) for i in range(matrix_dim) for j in range(matrix_dim)]


if "col" not in _basisConstructorDict:
    _basisConstructorDict["col"] = MatrixBasisConstructor(
        "Column-stacked matrix-unit basis", col_matrices, col_labels, False
    )
