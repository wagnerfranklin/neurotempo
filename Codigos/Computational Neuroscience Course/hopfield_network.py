from numpy._core import einsumfunc
from PIL import ImagePalette
from PIL import ImagePalette
from neurodynex3.hopfield_network import network, pattern_tools, plot_tools
import matplotlib.pyplot as plt

# A biblioteca neurodynex3 chama plt.show() dentro de cada função de plotagem,
# o que pausa o código até que a janela seja fechada.
# Redirecionamos temporariamente plt.show para exibir todas as figuras juntas ao final:
_orig_show = plt.show
plt.show = lambda *args, **kwargs: None

pattern_size = 10
M_max_stable = int(10**2*0.14)
# n_flipped_pixels = 40
n_steps = 5
n_random_patterns = 15

# create an instance of the class HopfieldNetwork
hopfield_net = network.HopfieldNetwork(nr_neurons = pattern_size**2)
# # plot network weights (synaptic weights of the Hopfield network)
# plot_tools.plot_network_weights(hopfield_net)
# plt.figure()
# plt.hist(hopfield_net.weights.flatten())
# instantiate a pattern factory
factory = pattern_tools.PatternFactory(pattern_size, pattern_size)
# create a checkerboard pattern and add it to the pattern list
checkerboard = factory.create_checkerboard()
# create an L-shaped pattern and add it to the pattern list
l_shape = factory.create_L_pattern()

pattern_list = [checkerboard]
# pattern_list = [l_shape, checkerboard]

# add random patterns to the list
pattern_list.extend(factory.create_random_pattern_list(nr_patterns=n_random_patterns, on_probability=0.5))
plot_tools.plot_pattern_list(pattern_list)

# how similar are the random patterns and the checkerboard? Check the overlaps
overlap_matrix = pattern_tools.compute_overlap_matrix(pattern_list)
plt.figure()  # Cria uma nova figura dedicada para a matriz de overlap
plot_tools.plot_overlap_matrix(overlap_matrix)

# let the hopfield network "learn" the patterns. Note: they are not stored
# explicitly but only network weights are updated !
hopfield_net.store_patterns(pattern_list)

# plot network weights again (synaptic weights of the Hopfield network)
# plot_tools.plot_network_weights(hopfield_net)
plt.figure()
plt.hist(hopfield_net.weights.flatten())

# use a pattern to initialize the network
hopfield_net.set_state_from_pattern(pattern_list[0])

# from this initial state, let the network dynamics evolve.
states = hopfield_net.run_with_monitoring(nr_steps= n_steps)

# each network state is a vector. reshape it to the same shape used to create the patterns.
states_as_patterns = factory.reshape_patterns(states)
# plot the states of the network
plot_tools.plot_state_sequence_and_overlap(states_as_patterns, pattern_list, reference_idx=0, suptitle="Network dynamics")

# Configura o eixo y de todas as figuras para conter apenas números inteiros
# from matplotlib.ticker import MaxNLocator

# for num in plt.get_fignums():
#     for ax in plt.figure(num).axes:
#         if 'overlap m(i,k)' in ax.get_title():
#             ax.set_yticks(range(n_patterns))
#             ax.set_xticks(range(n_patterns))
#         else:
#             ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# Restaura o plt.show original e abre todas as 3 figuras simultaneamente
plt.show = _orig_show
plt.show()