"""
This script sets up an afferent inhomogenous Poisson process onto the populations
"""
import brian2, string
import numpy as np


def set_spikes_from_time_varying_rate(time_array, rate_array, N, Nsyn, SEED=1):
    
    brian2.seed(SEED) # setting the seed !
    
    ## time_array in ms !!
    # so multplying rate array
    
    indices, times = [], []
    DT = (time_array[1]-time_array[0])
    
    # trivial way to generate inhomogeneous poisson events
    for it in range(len(time_array)):
        rdm_num = np.random.random(N)
        for ii in np.arange(N)[rdm_num<DT*Nsyn*rate_array[it]*1e-3]:
            indices.append(ii) # all the indicces
            times.append(time_array[it]) # all the same time !

    return np.array(indices), np.array(times)*brian2.ms


def construct_feedforward_input(POPS, AFFERENCE_ARRAY,\
                                time_array, rate_array,\
                                pop_for_conductance='A', SEED=1):
    """
    POPS and AFFERENCE_ARRAY should be 1D arrrays as their is only one 
    source population

    'pop_for_conductance' is the string identifying the source conductance
    that will be incremented by the afferent input !!
    """

    SPKS, SYNAPSES = [], []

    for ii in range(len(POPS)):
        # number of synapses per neuron
        Nsyn = AFFERENCE_ARRAY[ii]['pconn']*AFFERENCE_ARRAY[ii]['N']
        if Nsyn>0:
            indices, times = set_spikes_from_time_varying_rate(\
                            time_array, rate_array,\
                            POPS[ii].N, Nsyn, SEED=(SEED+ii)**2%100)
            SPKS.append(brian2.SpikeGeneratorGroup(POPS[ii].N, indices, times))
            pre_increment = 'G'+pop_for_conductance+string.ascii_uppercase[ii]+' += w'
            SYNAPSES.append(brian2.Synapses(SPKS[-1], POPS[ii], on_pre=pre_increment,\
                                            model='w:siemens'))
            SYNAPSES[-1].connect('i==j')
            SYNAPSES[-1].w = AFFERENCE_ARRAY[ii]['Q']*brian2.nS

    return SPKS, SYNAPSES

if __name__=='__main__':
    
    import sys
    sys.path.append('../')
    from ntwk_build.syn_and_connec_construct import build_populations,\
        build_up_recurrent_connections,\
        initialize_to_rest
    from ntwk_build.syn_and_connec_library import get_connectivity_and_synapses_matrix
    from waveform_library import double_gaussian
    
    DT, tstop =0.1, 100.
    brian2.defaultclock.dt = DT*brian2.ms
    t_array = np.arange(int(tstop/DT))*DT

    NTWK = [{'name':'exc', 'N':4000, 'type':'LIF'},
            {'name':'inh', 'N':1000, 'type':'LIF'}]
    
    M = get_connectivity_and_synapses_matrix('Vogels-Abbott', number=len(NTWK))
    POPS, RASTER = build_populations(NTWK, M, with_raster=True)

    initialize_to_rest(POPS, NTWK) # (fully quiescent State as initial conditions)
    
    AFFERENCE_ARRAY = [{'Q':10., 'N':400, 'pconn':0.02},
                       {'Q':10., 'N':400, 'pconn':0.02}]


    rate_array = double_gaussian(t_array, 60., 30., 20., 10.)
    AFF_SPKS, AFF_SYNAPSES = construct_feedforward_input(POPS, AFFERENCE_ARRAY,\
                                                     t_array, rate_array,\
                                                     pop_for_conductance='A')

    SYNAPSES = build_up_recurrent_connections(POPS, M)
    
    net = brian2.Network(brian2.collect())
    # manually add the generated quantities
    net.add(POPS, SYNAPSES, RASTER, AFF_SPKS, AFF_SYNAPSES) 

    net.run(tstop*brian2.ms)

    # plotting 
    fig1 = brian2.figure(figsize=(5,3.5))
    brian2.plot(RASTER[0].t/brian2.ms, RASTER[0].i, '.g',\
         RASTER[1].t/brian2.ms, RASTER[1].i+NTWK[0]['N'], '.r')
    brian2.xlabel('Time (ms)');brian2.ylabel('Neuron index')
    
    fig1.savefig('fig.png')

    

    
