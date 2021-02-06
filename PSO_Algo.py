import numpy as np

class PSO():
  def __init__(self, benchmark, ideal_target, error_threshold, num_particles,
                a_const = 0.9, b_const= 2, c_const = 2):
    self.benchmark = benchmark
    self.a_const = a_const
    self.b_const = b_const
    self.c_const = c_const
    self.ideal_target = ideal_target
    self.error_threshold = error_threshold
    self.num_particles = num_particles
    self.error_recorder = []
    self.gbest_val = float('inf')
    self._create_particles()
    self._init_global_best_pos()

  def _create_particles(self):
    self.particle_best_pos = np.zeros(shape=(self.num_particles, 2)) #2d Array for best x and y
    self.particle_best_val = np.zeros(self.num_particles)
    self.particle_curr_pos = np.zeros(shape=(self.num_particles, 2))
    self.particle_curr_velo = np.zeros(shape=(self.num_particles, 2)) # initial velocity = 0

    # Setting the initial params of the particles
    for ind_particle in range(self.num_particles):
      self.particle_curr_pos[ind_particle][0] = (-1)**(bool(random.getrandbits(1))) * \
                                                random.random()   # random start point x
      self.particle_curr_pos[ind_particle][1] = (-1)**(bool(random.getrandbits(1))) * \
                                                random.random()   # random start point y
      self.particle_best_pos[ind_particle][0] = self.particle_curr_pos[ind_particle][0]  # init best pos x = start pos x
      self.particle_best_pos[ind_particle][1] = self.particle_curr_pos[ind_particle][1]  # init best pos y = start pos y

  def _init_global_best_pos(self):
    self.gbest_pos = np.zeros(2)    # universally one in global topology, therefore just a 2d array required
    # self.gbest_pos[0] = random.random()
    # self.gbest_pos[1] = random.random()
    self.gbest_pos[0] = -1
    self.gbest_pos[1] = -1


  def pbest_setter(self):
    for particle in range(self.num_particles):
      benchmark_reward_candidate = benchmark(self.particle_curr_pos[particle][0], \
                                             self.particle_curr_pos[particle][1]) #TODO: restructure how rosenbrock and other is defined! 
      if(self.particle_best_val[particle] > benchmark_reward_candidate):
        #update best value and corresponding position
        self.particle_best_val[particle] = benchmark_reward_candidate
        self.particle_best_pos[particle] = self.particle_curr_pos[particle]

  def gbest_setter(self):
    for particle in range(self.num_particles):
      benchmark_reward_candidate = benchmark(self.particle_curr_pos[particle][0], \
                                             self.particle_curr_pos[particle][1])
      if(self.gbest_val > benchmark_reward_candidate):
        self.gbest_val = benchmark_reward_candidate
        self.gbest_pos = self.particle_curr_pos[particle]

  def start_particle_motion(self):
    for particle in range(self.num_particles):
      new_velocity = (self.a_const * self.particle_curr_velo[particle]) \
                      + (self.b_const * random.random() * (self.particle_best_pos[particle] - self.particle_curr_pos[particle])) \
                      + (self.c_const * random.random() * (self.gbest_pos - self.particle_curr_pos[particle]))

      # TODO: discuss the significance of del t in the position equation.
      new_position = self.particle_curr_pos[particle] + new_velocity  
      self.particle_curr_velo[particle] = new_velocity # update particle velocity
      self.particle_curr_pos[particle] = new_position  # update particle position

  def ps_optimizer(self, num_iterations):
    iter = 0
    while(iter < num_iterations):
      self.pbest_setter()
      self.gbest_setter()

      self.error_recorder.append(abs(self.ideal_target - self.gbest_val))

      if (self.error_threshold >= abs(self.ideal_target - self.gbest_val)):
        '''
        If the defined error threshold is acheived, return it.
        '''
        return self.error_recorder
        break;
      
      '''
      Parameter Optimization: 
      Here, we compare the results of a constant inertia 
      and time-varying inertia.
      SOTA for PSO paramtere optimzation states that
      inertia(a) should be gradually decreased from 0.9 to 0.4 over the defined
      iterations. The code below will start with a=0.9 and linearly reduce the 
      inertia parameter to 0.4
      '''
      self.a_const = 0.9 - (float(0.5)*(float(iter)/num_iterations))
      self.start_particle_motion()
      iter += 1
    return self.error_recorder