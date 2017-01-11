Python wrapper for NuPoP created by Ji-Ping Wang and Liqun Xi.
NuPoP was originally published by Xi et al, 2010; Wang et al, 2008.

NuPoP fortan code is was distributed under the GPL-2 License and
original sources should be cited.

python_NuPoP is a python package for Nucleosome Positioning Prediction.

Data Format
===========

Input files must be in FASTA format::

	>Sample
	ATCGATCGATCG

Simple Example:

    https://raw.githubusercontent.com/kylessmith/python_NuPoP/master/example/SAMPLE.fasta

Invocation
==========

Running the following command will result in a more detailed help message::

    $ python -m NuPoP -h

Gives::

	  --fa FA            fasta file name
	  --species SPECIES  species number Default=1 (e.g. 1=Human, 2=mouse)
	  --order ORDER      Order of Markov model (1 or 4) (default=4)
	  --plot PLOT        Name of plot output file (default=no plot)

QuickStart
==========
::

	$ python -m NuPoP \
		--fa example/SAMPLE.fasta\
		--plot example/SAMPLE.png

The output will be shown in the following files::

	example/SAMPLE.fasta_Prediction4.txt
	example/SAMPLE.png
	
Importation
===========
::

	>>> import NuPoP
	>>> NuPoP.nupop("SAMPLE.fasta", species=1, order=4) #run NuPoP
	>>> results = NuPoP.read_nupop("SAMPLE.fasta_Prediction4.txt") #read results
	>>> results
	{'NL': array([0, 0, 0, ..., 0, 0, 0]),
	'affinity': array([ nan,  nan,  nan, ...,  nan,  nan,  nan]),
	'occup': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
	'position': array([   1,    2,    3, ..., 8278, 8279, 8280]),
	'pstart': array([ 0.,  0.,  0., ...,  0.,  0.,  0.])}
	>>> NuPoP.plot_nupop("SAMPLE.fasta_Prediction4.txt", "SAMPLE.png") #plot NuPoP results
	>>> NuPoP.plot_nupop(results, "SAMPLE.png") #can also be done like this

Installation
============

If you dont already have numpy and matplotlib installed, it is best to download
`Anaconda`, a python distribution that has them included.  

    https://continuum.io/downloads

Dependencies can be installed by::

    pip install -r requirements.txt

python_NuPoP also depends on a fortran and c compiler. If `Anaconda` is installed::

	conda install gcc
	
If running on OS X, xcode commandline tools are required::

	xcode-select --install

License
=======

python_NuPoP is available under the GPL-2 License