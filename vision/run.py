import sys
import numpy as np
from earlyVis_model import earlyVis_model
from stimuli import visual_stimulus
from plots import plot

try:
    Runcase=int(sys.argv[-1])
except ValueError:
    Runcase='all'


if (Runcase==12) or (Runcase is 'model-doc') or (Runcase is 'all'):
    """
    demo fig of dynamic stimuli
    """
    model = earlyVis_model()
    ps = plot(model=model)
    
    fig, AX = ps.ge.figure(axes=(5,6), figsize=(.9,.7),
                           wspace=0.2, hspace=0.2, left=1.5, bottom=0., top=0.4, right=0.1)

    stim = visual_stimulus('drifting-grating')
    params = ' ($f$, $c$, $\\theta$, $\Psi$, $v_{dg}$)'
    ps.ge.annotate(AX[0][0], 'drifting\ngratings\n%s' % params, (-0.55,0.5), va='center', ha='center')
    ps.show_visual_stim_snapshots(stim, np.linspace(0, 1.2, 6), AX[0],
                                  with_time_annotation=True)

    stim = visual_stimulus('sparse-noise')
    params = ' ($\Gamma_{SN}$, $\sigma_{SN}$, $D_{SN}$, $J_{SN}$)'
    ps.ge.annotate(AX[1][0], 'sparse\nnoise\n%s' % params, (-0.55,0.5), va='center', ha='center')
    ps.show_visual_stim_snapshots(stim, np.linspace(0, 1.2, 6), AX[1],
                                  with_time_annotation=False)

    stim = visual_stimulus('dense-noise')
    params = ' ($\sigma_{DN}$, $D_{DN}$, $J_{DN}$)'
    ps.ge.annotate(AX[2][0], 'dense\nnoise\n%s' % params, (-0.55,0.5), va='center', ha='center')
    ps.show_visual_stim_snapshots(stim, np.linspace(0, 1.2, 6), AX[2],
                                  with_time_annotation=False)

    stim = visual_stimulus('gaussian-blob')
    params = ' ($c_{GB}$, $\sigma_{GB}$, $A_{GB}$,\n $\\tau_{DN}$, $t_{gb}$)'
    ps.ge.annotate(AX[3][0], 'gaussian blob\nappearance\n%s' % params,
                   (-0.55,0.5), va='center', ha='center')
    ps.show_visual_stim_snapshots(stim, np.linspace(0, 1.2, 6), AX[3],
                                  with_time_annotation=False)

    stim = visual_stimulus('center-surround')
    params = ' ($c_{CS}$)'
    ps.ge.annotate(AX[4][0], 'centered-surround\nprotocols\n%s' % params,
                   (-0.55,0.5), va='center', ha='center')
    ps.show_visual_stim_snapshots(stim, np.linspace(0, 1.2, 6), AX[4],
                                  with_time_annotation=False)
    
    
    fig.savefig('docs/figs/dynamic-stimuli.png')
    ps.show()
    
    
if (Runcase==11) or (Runcase is 'model-doc') or (Runcase is 'all'):
    """
    demo fig of static stimuli
    """
    model = earlyVis_model()
    stim = visual_stimulus('static-full-field-gratings')
    ps = plot(model=model)
    fig, AX = ps.ge.figure(axes=(5,6), figsize=(.9,.7), wspace=0.2, hspace=0.2, left=1.5, bottom=0., top=0.4, right=0.1)

    # full-field gratings
    params = ' ($f$, $c$, $\\theta$, $\Psi$)'
    ps.ge.annotate(AX[0][0], 'full-field\ngratings\n%s' % params, (-0.55,0.5), va='center', ha='center')
    ps.screen_plot(stim.full_array[1,:,:], ax=AX[0][0])
    for i, f, theta, psi, c in zip(range(6),
                              [0.1, 0.1, 0.1, 0.2, 0.02, 0.02],
                              [np.pi/6., np.pi/2., 3*np.pi/4., 3*np.pi/4., 3*np.pi/4., 3*np.pi/4.],
                              [np.pi, np.pi, np.pi, np.pi, np.pi, 0],
                              [1, 0.5, 1, 0.7, 0.8, 0.6]):
        stim.static_full_field_grating(theta=theta, spatial_freq=f, contrast=c, spatial_phase=psi)
        ps.screen_plot(stim.full_array[1,:,:], ax=AX[0][i], with_scale_bar=np.invert(bool(i)))

    # center gratings
    params = r'($f$, $c_c$, $\theta_c$, $\Psi_c$, $\vec{x_c}$, $r_c$)'
    ps.ge.annotate(AX[1][0], 'center\ngratings\n%s' % params, (-0.55,0.5), va='center', ha='center')
    for i, f, theta, psi, center, s, c in zip(range(6),
                                      [0.1, 0.1, 0.1, 0.2, 0.1, 0.1],
                                      [np.pi/6., np.pi/2., 3*np.pi/4., 3*np.pi/4., 3*np.pi/4., np.pi/8.],
                                      [np.pi, np.pi, 0, 0, np.pi, np.pi],
                                      [(40,20),(20,20),(40,20),(50,40),(20,40),(40,30)],
                                      [7,7,7,10,5,20],
                                      [1, 0.5, 1, 0.7, 1, 0.2]):
        stim.static_center_grating(center_theta=theta, center_spatial_freq=f, center=center,
                                   center_radius=s, center_contrast=c, center_spatial_phase=psi)

        ps.screen_plot(stim.full_array[1,:,:], ax=AX[1][i], with_scale_bar=np.invert(bool(i)))

    # # surround gratings
    params = r'($f$,$c_s$,$\theta_s$,$\Psi_s$,$\vec{x_c}$,$r_c$,$r_s$)'
    ps.ge.annotate(AX[2][0], 'surround\ngratings\n%s' % params, (-0.55,0.5), va='center', ha='center')
    # ps.screen_plot(stim.full_array[1,:,:], ax=AX[2][0])
    for i, f, c, theta, center, r1, r2 in zip(range(6),
                                              [0.1, 0.1, 0.1, 0.2, 0.1, 0.1],
                                              [1,1,0.5,1,1,1],
                                              [np.pi/6., np.pi/2., 3*np.pi/4., 3*np.pi/4., 3*np.pi/4., np.pi/8.],
                                           [(40,20),(20,20),(40,20),(50,40),(20,40),(40,30)],
                                           [10,10,10,3,5,20],
                                           [20,25,30,8,25,25]):
        stim.static_surround_grating(surround_theta=theta, surround_spatial_freq=f,
                                     center=center, center_radius=r1, surround_radius=r2,
                                     surround_contrast=c)
        ps.screen_plot(stim.full_array[1,:,:], ax=AX[2][i], with_scale_bar=np.invert(bool(i)))

    # # # center-surround gratings
    params = '($f$,$c_c$,$c_s$,$\\theta_c$,$\\theta_s$,\n'+r'$\Psi_c$,$\Psi_s$,$\vec{x_c}$,$r_c$,$r_s$)'
    ps.ge.annotate(AX[3][0], 'center-surround\ngratings\n%s' % params, (-0.55,0.5), va='center', ha='center')
    for i, f, c1, c2, theta1, theta2, psi, center, r1, r2 in zip(range(6),
                                           [0.1, 0.1, 0.1, 0.2, 0.1, 0.1],
                                           [1, 0.5, 1, 0.7, 1, 0.2],
                                           [1,1,0.5,1,1,1],
                                           [np.pi/6., np.pi/2., 3*np.pi/4., 3*np.pi/4., 3*np.pi/4., np.pi/8.],
                                           [np.pi/2., np.pi/4., 3*np.pi/4, np.pi/4., np.pi/4., np.pi],
                                           [np.pi, np.pi, 0, 0, np.pi, np.pi],
                                           [(40,20),(20,20),(40,20),(50,40),(20,40),(40,30)],
                                           [10,10,10,3,5,20],
                                           [20,25,30,8,25,25]):
        stim.static_center_surround_grating(center_theta=theta1, surround_theta=theta2,
                                            center_contrast=c1, surround_contrast=c2,
                                            surround_spatial_freq=f, center_spatial_freq=f,
                                            surround_spatial_phase=psi, center_spatial_phase=psi,
                                            center=center,
                                            center_radius=r1, surround_radius=r2)
        ps.screen_plot(stim.full_array[1,:,:], ax=AX[3][i], with_scale_bar=np.invert(bool(i)))

    
    # # # natural images
    ps.ge.annotate(AX[4][0], 'natural\nimages', (-0.55,0.5), va='center', ha='center')
    ps.screen_plot(stim.full_array[1,:,:], ax=AX[4][0])
    for i, theta2 in enumerate(np.linspace(0, .9*np.pi, 6)):
        stim.natural_images(image_number=i)
        ps.screen_plot(stim.full_array[1,:,:], ax=AX[4][i], with_scale_bar=np.invert(bool(i)))
        
    fig.savefig('docs/figs/static-stimuli.png')
    ps.show()
    
if (Runcase==10) or (Runcase is 'model-doc') or (Runcase is 'all'):
    """
    demo fig of SEM model
    """
    model = earlyVis_model()
    model.init_eye_movement('saccadic')
    plot_sim = plot(model=model)
    fig, _ = plot_sim.SEM_plot()
    fig.savefig('docs/figs/SEM-model.png')
    plot_sim.show()
    
if (Runcase==9) or (Runcase is 'model-doc') or (Runcase is 'all'):
    """
    demo fig of LNP model
    """
    model = earlyVis_model()
    plot_sim = plot(model=model)
    fig, AX = plot_sim.ge.figure(axes_extents=[[[2,1]],
                                               [[2,1]],
                                               [[2,1]],
                                               [[2,2]]],
                                 figsize=(.9,.45), hspace=0.5, left=.9, right=.5, bottom=1.2)
    
    t = np.arange(1500)*1e-3
    model.t, model.dt = t, 1e-3

    s = np.array([1 if tt>0.4 else 0 for tt in t])
    s[(t>0.1) & (t<0.2)] = -1
    AX[0].plot(t, s, 'k-')
    plot_sim.ge.set_plot(AX[0], ['left'], ylabel='  input\n  signal',
                         yticks=[-1,0,1], xlim=[t[0], t[-1]])
    r, a = model.temporal_filtering(t, s)
    AX[1].plot(t, a, '-', color=plot_sim.ge.purple, label='a(t)')
    AX[1].plot(t, r, '-', color=plot_sim.ge.blue, lw=2, label='r(t)')
    plot_sim.ge.annotate(AX[1], 'r(t)', (.6,-.1), color=plot_sim.ge.blue)
    plot_sim.ge.annotate(AX[1], 'a(t)', (.6,1), color=plot_sim.ge.purple)
    plot_sim.ge.set_plot(AX[1], ['left'], ylabel='processed\nsignal', xlim=[t[0], t[-1]])
    model.RATES = [model.compute_rates(r)]
    AX[2].plot(t, model.RATES[0], 'k-')
    plot_sim.ge.set_plot(AX[2], ['left'], ylabel='Rate  \n(Hz)  ', xlim=[t[0], t[-1]])
    for i in range(10):
        model.Poisson_process_transform(seed=i+20)
        for spk in model.SPIKES[0]:
            AX[3].plot([spk,spk], [0.1*i,0.1*(i+1)], color=plot_sim.ge.brown)
    plot_sim.ge.set_plot(AX[3], ylabel='Spike output\n(for 10 seeds)', yticks=[], xlabel='time (s)',
                         ylim=[0,1], xlim=[t[0], t[-1]])
    fig.savefig('docs/figs/LNP-model.png')
    plot_sim.show()
if (Runcase==8) or (Runcase is 'model-doc') or (Runcase is 'all'):
    model = earlyVis_model()
    model.draw_cell_RF_properties(model.Ncells, clustered_features=True)
    plot_sim = plot(model=model)
    icells = np.random.choice(np.arange(model.Ncells), 12)
    fig = plot_sim.plot_RF_properties(cell_list=icells)
    fig.savefig('docs/figs/RF.png')
    plot_sim.show()
if (Runcase==7) or (Runcase is 'model-doc') or (Runcase is 'all'):
    model = earlyVis_model()
    model.draw_cell_RF_properties(model.Ncells, clustered_features=True)
    plot_sim = plot(model=model)
    fig = plot_sim.show_cell_props_distrib()
    fig.savefig('docs/figs/cell-props.png')
    plot_sim.show()
if (Runcase==6) or (Runcase is 'all'):
    model = earlyVis_model(from_file='data/drifting-grating.npz')
    plot_sim = plot(model=model)
    plot_sim.protocol_plot()
    plot_sim.show()
if (Runcase==5) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('drifting-grating', '', seed=3)
    model.save_data('data/drifting-grating.npz')
if (Runcase==4) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('sparse-noise', 'saccadic', seed=3)
    model.save_data('data/sparse-noise-saccadic.npz')
if (Runcase==3) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('dense-noise', '', seed=3)
    model.save_data('data/dense-noise.npz')
if (Runcase==2) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('sparse-noise', '', seed=3)
    model.save_data('data/sparse-noise.npz')
if (Runcase==1) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('grating', 'saccadic', seed=3)
    model.save_data('data/grating-saccadic.npz')
if (Runcase==0) or (Runcase is 'all'):
    model = earlyVis_model()
    model.full_process('drifting-grating', 'saccadic', seed=3)
    model.save_data('data/drifting-grating-saccadic.npz')
