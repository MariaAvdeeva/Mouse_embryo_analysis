import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def plot_dynamicss(dat, 
                   vari, 
                   color, 
                   stacks = [1,2,7,8], 
                   palette = 'Reds',
                   lin_palette = ['lime','darkgreen', 'deepskyblue', 'mediumblue'],
                   perc_max = 98, 
                   perc_min = 2,
                   lineages = None,):
    sns.set(font_scale = 1.5, style = 'white')
    for i in stacks:#range(num_embryos):
        cur_stack = 'stack_'+str(i)
        #_, _, out = mydirs(indir, cur_stack, outdir = outdir) 
        both = dat.loc[cur_stack].copy()#.query('Cell_Volume < 60000*4*4*0.208*2').copy()
        #both = both.query('Norm_NC_Yap_Diff<1')
        #both = both.query('Norm_NC_Yap_Diff>-1')
        dd = both.reset_index()
        cdx_all = dd.reset_index()[color].copy()
        plt.figure(figsize = (40,20))
        if lineages == None:
            lineages = np.unique(dd['Lineage']).astype(str)
        for i in lineages:
            try:
                ln=i
                dd = both.reset_index()
                ax = plt.subplot(3,3,int(ln))
                #cdx = dd['Cdx2']
                dd['Lineage'] = dd['Lineage'].astype(str)
                
                sns.lineplot(data=dd, x = 'Hour', y = vari, 
                             estimator = None,
                                units = 'Fact_branch',
                                ax = ax,
                                color = 'black',
                             alpha = 0.1,
                            lw = 0.1)
                sns.scatterplot(data=dd, x = 'Hour', y = vari, 
                                color = 'lightgrey',
                                ax = ax,
                                s = 70,
                                marker = 's',
                                alpha = 0.4,
                               palette = 'Reds')
                dd = dd.query('Lineage == "'+str(i)+'"')

                cdx = dd[color]
                hue = np.array(cdx.tolist())
                #print(hue)
                vmax = np.percentile(cdx_all[~np.isnan(cdx_all)], perc_max)
                vmin = np.percentile(cdx_all[~np.isnan(cdx_all)], perc_min)
                hue[hue>vmax] = vmax
                hue[hue<vmin] = vmin
                #print(vmax, vmin)

                norm = plt.Normalize(vmin, vmax)
                sns.lineplot(data=dd, x = 'Hour', y = vari, 
                             estimator = None,
                                units = 'Fact_branch',
                             hue = 'Fact_branch',
                                ax = ax,
                                palette = lin_palette,
                             alpha = 0.7,
                            lw = 2)
                sns.scatterplot(data=dd, x = 'Hour', y = vari, 
                                hue = hue,
                                hue_norm = norm,
                                ax = ax,
                                s = 200,
                                marker = 's',
                                #edgecolor='white',
                                #linewidth = 2,
                                alpha = 1,
                               palette = palette)

                
                sm = plt.cm.ScalarMappable(cmap=palette, norm=norm)
                sm.set_array([])

                # Remove the legend and add a colorbar
                ax.get_legend().remove()
                cbar = ax.figure.colorbar(sm)
                cbar.ax.set_title(color, y = 1.05)
                plt.title('Lineage '+str(ln), fontsize = 30)
                #plt.ylim(0.,3)
            except:
                continue
        plt.tight_layout()
        plt.suptitle(vari+' dynamics '+color+', '+cur_stack, y = 1.04, fontsize = 50)
    #    plt.savefig(out+'figures/'+out_regime+'/'+cur_stack+'_norm_NC_Yap_and_solidity_all_lineages_clean.png', dpi = 200)
        #plt.show()