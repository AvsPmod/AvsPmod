# Optimize script parameters specified on user sliders
# See http://forum.doom9.org/showpost.php?p=935347&postcount=503

def main():
    import random
    import math
    import subprocess
    import os
    import os.path
    
    app = avsp.GetWindow()
    params = []
    scriptTemplate = ''
    logfilename = 'log.txt'
    avs2avidir = os.path.join(app.toolsfolder, 'avs2avi.exe')
    
    # Simple Genetic Algorithm implementation
    class SGA(object):
        def __init__(self,
                chromosome_length,
                objective_function,
                population_size=100,
                probability_crossover=0.5,
                probability_mutation=0.01,
                selection_pressure=4,
                max_generations=10,
                minimize=True,
                dump_function=None):
            # Define the variables for the key GA parameters
            SGA.length = chromosome_length
            self.objfn = objective_function
            self.n = population_size - population_size % 2
            self.pc = probability_crossover
            self.pm = probability_mutation
            self.s = selection_pressure
            self.maxgen = max_generations
            SGA.minimize = minimize
            self.dump = dump_function
            self.generation = 0
            self.scoreDict = {}
            # Define the individual class
            class Individual(object):
                def __init__(self, chromosome=None):
                    self.length = SGA.length
                    self.minimize = SGA.minimize
                    self.score = None
                    self.chromosome = chromosome
                    if self.chromosome is None:
                        self.chromosome = [random.choice((0,1)) for i in xrange(self.length)]
                        
                def __cmp__(self, other):
                    if self.minimize:
                        return cmp(self.score, other.score)
                    else:
                        return cmp(other.score, self.score)                    
                        
                def copy(self):
                    twin = self.__class__(self.chromosome[:])
                    twin.score = self.score
                    return twin
            self.Individual = Individual
            
        def run(self):
            # Create the initial population (generation 0)
            self.population = [self.Individual() for i in range(self.n)]
            try:
                pb = avsp.ProgressBox(self.n, _('Initial evaluation...'), _('Generation 0 Progress'))
            except NameError:
                pb = None
            try:
                for i, individual in enumerate(self.population):
                    self.evaluate(individual)
                    if pb is not None:
                        if not pb.Update(i)[0]:
                            pb.Destroy()
                            return False
                # Dump the best data from this generation
                best = min(self.population)
                initialscore = best.score
                if self.dump is not None:
                    self.dump(best.chromosome, best.score)
                if pb is not None:
                    pb.Destroy()
                self.generation += 1
                # Run the genetic algorithm
                while self.generation < self.maxgen:
                    # Create a progress bar for this generation
                    if pb is not None:
                        pb = avsp.ProgressBox(
                            self.n,
                            _('Initial best score: %.3f, Current best score: %.3f') % (initialscore, best.score),
                            'Generation %i Progress' % self.generation
                        )
                    newpopulation = [best.copy()]
                    count = len(newpopulation)
                    while count < self.n:
                    #~ for i in xrange(self.n/2):
                        # Selection
                        mate1 = self.selection()
                        mate2 = self.selection()
                        # Crossover
                        children = self.crossover(mate1, mate2)
                        for individual in children:
                            # Mutation
                            self.mutation(individual)
                            # Evaluate the individual and add it to the new population
                            self.evaluate(individual)
                            newpopulation.append(individual)
                        # Update the progress bar
                        count = len(newpopulation)
                        if pb is not None:
                            i = min(count-1, self.n-1)
                            if not pb.Update(i)[0]:
                                pb.Destroy()
                                return False
                    # Update the internally stored population
                    self.population = newpopulation[:self.n]
                    # Dump the best data from this generation
                    best = min(self.population)
                    if self.dump is not None:
                        self.dump(best.chromosome, best.score)
                    # Destroy the progress bar for this generation
                    if pb is not None:
                        pb.Destroy()
                    self.generation += 1
            finally:
                if pb is not None:
                    pb.Destroy()
            return True
            
        def crossover(self, individual1, individual2):
            '''Two point crossover'''
            if random.random() < self.pc:
                # Pick the crossover points randomly
                left = random.randrange(1, self.length-2)
                right = random.randrange(left, self.length-1)
                # Create the children chromosomes
                p1 = individual1.chromosome
                p2 = individual2.chromosome
                c1 = p1[:left] + p2[left:right] + p1[right:]
                c2 = p2[:left] + p1[left:right] + p2[right:]
                # Return the new individuals
                return self.Individual(c1), self.Individual(c2)
            else:
                # Don't perform crossover
                return individual1.copy(), individual2.copy()
            
        def mutation(self, individual):
            '''Bit-flip mutation'''
            # Randomly flip each bit in the chromosome
            chromosome = individual.chromosome
            for gene in xrange(self.length):
                if random.random() < self.pm:
                    chromosome[gene] = int(not chromosome[gene])
                    
        def selection(self):
            '''Tournament selection with replacement'''
            # Return best individual from s randomly selected members
            competitors = [random.choice(self.population) for i in range(self.s)]
            #~ competitors.sort()
            #~ return competitors[0]
            return min(competitors)
            
        def evaluate(self, individual):
            intChromosome = binary2int(individual.chromosome)
            if self.scoreDict.has_key(intChromosome):
                # The chromosome was evaluated previously
                individual.score = self.scoreDict[intChromosome]
            else:
                # Run the objective function to evaluate the chromosome
                individual.score = self.objfn(individual.chromosome)
                self.scoreDict[intChromosome] = individual.score
                
    def binary2int(x):
        '''decode a binary list to a single unsigned integer'''
        return sum(map(lambda z: int(x[z]) and 2**(len(x) - z - 1),  range(len(x)-1, -1, -1)))
        
    def decode_params(bitlist, params):
        '''returns dictionary of values for each param'''
        iA = 0
        paramDict = {}
        for name, valuelist, nbits in params:
            iB = iA + nbits
            sublist = bitlist[iA:iB]
            #~ value = min + binary2int(sublist) * (max-min)/float(2**nbits - 1)
            #~ if type(min) == bool:
                #~ value = bool(value)
            index = int(binary2int(sublist) * (len(valuelist) - 1) / float(2 ** nbits - 1))
            paramDict[name] = valuelist[index]
            iA = iB
        return paramDict    
        
    def evaluate(chromosome):
        # Decode the bit string into the individual parameters
        paramDict = decode_params(chromosome, params)
        # Create the AviSynth script
        script = scriptTemplate % paramDict
        inputavsname = os.path.join(scriptdir, 'ga_evaluate.avs')
        script = app.GetEncodedText(script, bom=True)
        f = open(inputavsname, 'w')
        f.write(script)
        f.close()
        # Encode the video to get the results (dumped to log.txt)
        try:
            os.remove(logfilename)
        except OSError:
            pass
        subprocess.call([avs2avidir, inputavsname, '-q', '-o', 'n', '-c','null'], shell=True)
        # Read the results in log.txt
        if os.path.isfile(logfilename):
            f = open(logfilename, 'r')
            lines = f.readlines()
            f.close()
            score = float(lines[-1].split()[2])
            #~ print 'good!', score
        else:
            score = 0
            #~ print '*** Error, bad script:'
            #~ print script
            #~ print '*** End script'
        return score
        
    def dump(chromosome, score=None):
        '''Write the script to a file'''
        paramDict = decode_params(chromosome, params)
        script = scriptTemplate % paramDict
        script = app.GetEncodedText(script, bom=True)
        f = open(os.path.splitext(filename)[0] + '-optimized.avs', 'w')
        f.write(script)
        f.close()
        if score is not None:
            print _('Best score: %.2f') % score
            
    # MAIN SECTION
    if not avs2avidir or not os.path.isfile(avs2avidir):
        avsp.MsgBox(_('Must configure avs2avi directory to use this macro!'), _('Error'))
        return
    # Save the script
    filename = avsp.SaveScript()
    if not filename:
        return
    if not avsp.UpdateVideo():
        avsp.MsgBox(_('The current Avisynth script contains errors.'), _('Error'))
        return
    scriptdir = os.path.dirname(filename)
    scriptTemplate = avsp.GetText()
    # Parse the script to determine the log filename
    
    # Create the parameters to optimize based on user sliders in the script
    sliderInfoList = avsp.GetSliderInfo()
    if not sliderInfoList:
        avsp.MsgBox(_('Not user sliders on the current Avisynth script!'), _('Error'))
        return
    length = 0
    for text, label, valuelist, nDecimal in sliderInfoList:
        if valuelist is None:
            continue
        mantissa, nbits = math.frexp(len(valuelist))
        if mantissa == 0.5:
            nbits -= 1
        params.append([label, valuelist, nbits])
        length += nbits
        scriptTemplate = scriptTemplate.replace(text, '%('+label+').'+str(nDecimal)+'f')
    # Get basic encoder options with a dialog box
    title = _('Enter optimization info    (%i bits, %i possibilities)') % (length, 2**length)
    message = [_('SSIM log filename:'), [_('max generations:'), _('population size:'), 
              _('crossover probability:'), _('mutation probability:'), _('selection pressure:')]]
    dirname, basename = os.path.split(logfilename)
    if not os.path.isdir(dirname):
        logfilename = os.path.join(app.GetProposedPath(only='dir'), basename)
    default = [logfilename, [(10, 1), (30, 1), (0.6, 0, 1, 2, 0.05), (0.03, 0, 1, 2, 0.05), 4]]
    types = ['file_save', ['spin', 'spin', 'spin', 'spin', 'spin']]
    entries = avsp.GetTextEntry(message, default, title, types)
    if not entries:
        return
    # First clear the AVI from memory (to close the log file)
    txt = avsp.GetText()
    avsp.HideVideoWindow()
    avsp.CloseTab()
    avsp.OpenFile(filename)
    avsp.SetText(txt)
    avsp.SaveScript()
    # Run the optimization
    logfilename, maxgen, n, pc, pm, s = entries
    print _('Begin optimization...')
    print 'n=%s, pc=%s, pm=%s, s=%s, maxgen=%s (%i bits)' % (n, pc, pm, s, maxgen, length)
    sga = SGA(length, evaluate, int(n), float(pc), float(pm), int(s), int(maxgen), False, dump)
    sga.run()
    os.remove(os.path.join(scriptdir, 'ga_evaluate.avs'))
    print _('Finished optimization.')
    # Show the optimized results
    avsp.OpenFile(os.path.splitext(filename)[0] + '-optimized.avs')
    avsp.ShowVideoFrame()
    
main()