# Copyright (c) 2016, Imperial College London
# Copyright (c) 2016, Benedikt Lorch
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the BSD license. See the accompanying LICENSE file
# or read the terms at https://opensource.org/licenses/BSD-3-Clause.

'''
Description:
	Given a 2D object as input, simulate a very basic MR acquisition with a radial trajectory.
	Reconstruct the simulated k-space data once with and once without weights compensating for the sampling density.
	Visualize the results and the point spread function.
'''

from __future__ import division
import numpy as np
from nfft.nfft import Plan
from scipy.io import loadmat


def constructRadialKnots2D(numSpokes, numSamplesPerSpoke):
	'''
	Generates the 2D locations of data samples within the range [-0.5, 0.5] ** 2 lying on a radial trajectory
	:param numSpokes: number of spokes to generate
	:param numSamplesPerSpoke: number of data points along one spoke
	:return: ndarray of size (numSpokes * numSamplesPerSpoke, 2) indicating the location of each sample point in k-space
	'''

	# Make sure numSamplesPerSpoke is an odd number such that we have a center sample
	assert numSamplesPerSpoke % 2 == 1

	# M: number of samples in total
	M = numSamplesPerSpoke * numSpokes
	knots = np.zeros((M, 2))
	for i in xrange(numSpokes):
		# ith spoke
		for j in xrange(numSamplesPerSpoke):
			# jth sample on the current spoke

			# Alternating forward and backward spokes
			if i % 2 == 0:
				r = -j / (numSamplesPerSpoke - 1) + 1/2.0
			else:
				r = j / (numSamplesPerSpoke - 1) - 1/2.0

			knots[i*numSamplesPerSpoke + j] = [r * np.sin((i * np.pi / numSpokes)), r * np.cos(i * np.pi / numSpokes)]

	return knots


# Load phantom with original size 256x256
phantom = loadmat('phantom256.mat')["p"]
# Number of samples in phase encoding and frequency encoding direction
nPE, nFE = 256, 256
# Field-of-view (FOV) of input image and reconstruction
Nx, Ny = 256, 256

# Usually we oversample in frequency direction by factor 2
oFE = 2
nFE = nFE * oFE
# Pad the image with zeros to account for the oversampling
zeropadding = int(Nx * (oFE - 1) / 2.0)
phantom = np.pad(phantom, zeropadding, mode='constant', constant_values=0)
# Update FOV
Nx = Nx + 2 * zeropadding
Ny = Ny + 2 * zeropadding
lfov = zeropadding
rfov = Nx - zeropadding

# Create radial trajectory
# To change the reconstruction quality, you can take only half of the phase encoding steps (make sure that numSpokes is an integer value) or double the number
numSpokes = nPE
# The number of samples in k-space is inversely related to the FOV
numSamplesPerSpoke = (nFE * oFE) + 1
knots = constructRadialKnots2D(numSpokes, numSamplesPerSpoke)

# Compute analytical weights to compensate for sampling density
# For details, see "Non-Cartesian Reconstruction" by John Pauly
rr = np.arange(1 + numSamplesPerSpoke // 2)
dkr = 1.0 / (1.0 * numSamplesPerSpoke)
# Note that we leave out a factor of 2 here to account for the fact that we are only considering the disks from 0 to pi instead of 2 pi and mirroring the other half
dka = np.pi / numSpokes
w = rr * dka * dkr ** 2
w[0] = dka * dkr ** 2 / 8.0
wAnaly = np.hstack((w[::-1], w[1:]))
# Scale weights to preserve the intensity range
wAnaly = wAnaly / (nPE * oFE / Nx)

# Forward transform
plan = Plan((Nx, Ny), knots.shape[0])
np.copyto(plan.f_hat, phantom)
np.copyto(plan.x, knots)
plan.precompute()
plan.forward()
kspace = np.copy(plan.f)

# Compute point spread function
np.copyto(plan.f, np.ones(numSpokes * numSamplesPerSpoke) * np.tile(wAnaly, numSpokes))
psfAnaly = np.copy(plan.adjoint())

# Compute adjoint without the sampling density compensation
np.copyto(plan.f, kspace)
fHatNoDcf = np.copy(plan.adjoint())

# and with the sampling density compensation
np.copyto(plan.f, kspace * np.tile(wAnaly, numSpokes))
fHatDcfAnaly = np.copy(plan.adjoint())

import matplotlib
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', size=4)
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.cm as cm

# Crop to original FOV
phantom = phantom[lfov:rfov, lfov:rfov]
psfAnaly = np.abs(psfAnaly)[lfov:rfov, lfov:rfov]
fHatNoDcf = np.abs(fHatNoDcf)[lfov:rfov, lfov:rfov]
fHatDcfAnaly = np.abs(fHatDcfAnaly)[lfov:rfov, lfov:rfov]

# Radial mask
dmask = np.sum((np.mgrid[0:Nx-2*zeropadding, 0:Nx-2*zeropadding] - (Nx-2*zeropadding) // 2) ** 2, axis=0) ** 0.5
rmask = dmask < (1.0 * Nx / 2)

# Plot
fig, axes = plt.subplots(2, 2, figsize=(4, 4), dpi=300)
axes[0, 0].imshow(phantom * rmask, cmap=cm.gray, interpolation='none')
axes[0, 0].set_title("Original")
axes[0, 0].axis('off')
axes[0, 1].imshow(fHatNoDcf * rmask, cmap=cm.gray, interpolation='none')
axes[0, 1].set_title("Adjoint - no density compensation")
axes[0, 1].axis('off')
axes[1, 0].imshow(psfAnaly, cmap=cm.gray, norm=LogNorm(), interpolation='None')
axes[1, 0].set_title("Point spread function")
axes[1, 0].axis('off')
axes[1, 1].imshow(fHatDcfAnaly * rmask, cmap=cm.gray, interpolation='none')
axes[1, 1].set_title("Adjoint with density compensation")
axes[1, 1].axis('off')

fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, hspace=0.25, wspace=0.25)
plt.show()