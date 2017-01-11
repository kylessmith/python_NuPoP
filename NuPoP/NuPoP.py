'''
Python wrapper for NuPop

Reference:
    Xi et al. "Predicting nucleosome positioning using a
               duration Hidden Markov Model" BMC Bioinformatics 2010
'''
import numpy as np
import argparse
import os
import npred
import matplotlib.pyplot as plt

#load nupop input files
inputs_path = '/'.join(os.path.realpath(__file__).split("/")[:-1])
inputs = np.load(inputs_path+"/nupop_inputs.npz")


def nupop(filename, species=1, order=4):
    '''
    run NuPop and write results to a file
    
    Arguements:
        filename: FASTA file
        species: species number Default=1 (e.g. 1=Human, 2=mouse)
        order: Order of Markov model (1 or 4) (default=4)
    
    Returns:
        writes results to file
    '''
    
    mlL = 500
    rep = 1
    lfn = len(filename)
        
    if order == 1:
        npred.vtbfb(lfn,filename,inputs["freqL1"],inputs["tranL1"],inputs["freqN1"],
                    inputs["tranN1"],rep,species,inputs["Pd"])
        #npred.vtbfb(lfn,filename,freqL1,tranL1,freqN1,tranNN,mlL,rep,species,Pdd)

    elif order == 4:
        npred.vtbfbnl4(lfn,filename,inputs["freqL1"],inputs["tranL1"],inputs["tranL2"],
                        inputs["tranL3"],inputs["tranL4"],inputs["freqN4"][:64],inputs["tranN4"],
                        rep,species,inputs["Pd"])
    
    else:
        print "order must be 1 or 4"
        

def read_nupop(filename):
    '''
    Read NuPop results into python
    
    Arguments:
        filename: NuPop results file name
    
    Returns:
        nupop_results: {"position": position in the input DNA sequence
                        "pstart":  probability that the current position is the start of a nucleosome.
                        "occup": nucleosome occupancy score. The nucleosome occupancy score is defined as the probability
                                 that the given position is covered by a nucleosome
                        "NL": 1 indicates the given position is covered by nucleosome and 0 for linker linker based on Viterbi
                              prediction
                        "affinity": nucleosome binding affinity score. This affinity score is defined for every 147 bp of
                                    DNA sequence centered at the given position. Therefore for the first and last 73 bp of the DNA
                                    sequence, the affinity score is not defined (indicated as NA).
                        }
    '''
    
    nupop_results = {"position":[], 
                    "pstart":[],
                    "occup":[],
                    "NL":[],
                    "affinity":[]}
    
    for i, line in enumerate(open(filename, "r")):
        fields = filter(None, line.strip().split(" "))
        if i != 0:
            nupop_results["position"].append(int(fields[0]))
            nupop_results["pstart"].append(float(fields[1]))
            nupop_results["occup"].append(float(fields[2]))
            nupop_results["NL"].append(int(fields[3]))
            if fields[4] == "NA":
                nupop_results["affinity"].append(np.nan)
            else:
                nupop_results["affinity"].append(float(fields[4]))
            
    for key in nupop_results:
        nupop_results[key] = np.array(nupop_results[key])
        
    return nupop_results


def plot_nupop(nupop_results, out=""):
    '''
    Plot NuPop results
    
    Arguments:
        nupop_results: nupop results file name or read_nupop output
        out: name to save plot as (e.g. figure.png)(default=show)
    
    Returns:
        saves figure is name provided or prints to screen
    
    '''
    
    if type(nupop_results) == str:
        plot_nupop(read_nupop(nupop_results), out)
    elif type(nupop_results) == dict:
        plt.plot(nupop_results["position"], nupop_results["occup"], color="black")
        plt.fill_between(nupop_results["position"], nupop_results["occup"],
                         where=nupop_results["occup"]>=0, interpolate=True, color='grey')
        plt.plot(nupop_results["position"], nupop_results["NL"], color="red")
        plt.plot(nupop_results["position"], nupop_results["pstart"], color="blue")
        plt.title("Occupancy(grey)/probability(blue)/Viterbi(red)")
        plt.xlabel("position")
        plt.ylabel("probability/occupancy")
        if out == "":
            plt.show()
        else:
            plt.savefig(out)

def main():
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--fa', help='fasta file name', required=True)
    parser.add_argument('--species', help='species number Default=1 (e.g. 1=Human, 2=mouse)', default=1, type=int)
    parser.add_argument('--order', help='Order of Markov model (1 or 4) (default=4)', type=int, default=4)
    parser.add_argument('--plot', help='Name of plot output file (default=no plot)', default="")
    args=parser.parse_args()
    
    filename = args.fa
    species = args.species
    order = args.order
    plot = args.plot
    
    nupop(filename, species, order)
    if plot != "":
        outname = filename+"_Prediction"+str(order)+".txt"
        plot_nupop(outname, plot)

        
if __name__ == "__main__":
    main()