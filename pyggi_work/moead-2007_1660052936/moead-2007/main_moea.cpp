/*==========================================================================
//  Implementation of MOEA/D Based on Differential Evolution (DE) for Continuous Multiobjective 
//  Optimization Problems with Complicate Pareto Sets (2007)
//
//  See the details of MOEA/D-DE and test problems in the following paper
//  H. Li and Q. Zhang, Comparison Between NSGA-II and MOEA/D on a Set of Multiobjective Optimization 
//  Problems with Complicated Pareto Sets, Technical Report CES-476, Department of Computer Science,
//  University of Essex, 2007
//
//  The component functions of each test instance can be found in "objective.h". 
//
//  The source code of MOEA/D-DE and NSGA-II-DE were implemented by Hui Li and Qingfu Zhang  
//
//  If you have any questions about the codes, please contact 
//  Qingfu Zhang at qzhang@essex.ac.uk  or Hui Li at hzl@cs.nott.ac.uk
===========================================================================*/

#include <cassert>
#include <cstdlib>

#include "common/global.h"
#include "DMOEA/dmoeafunc.h"
#include "NSGA2/nsga2func.h"

void execute(char *alg);
void reassess(char *alg);

int main(int argc, char **argv) {
  // Argument parsing (inst, seed, algo flag, reassess flag)
  assert(argc == 5);
  int instance = atoi(argv[1]);
  assert(instance >= 0 && instance < 9);
  seed = atoi(argv[2]);
  bool use_moead = atoi(argv[3]);
  bool exe_or_reassess = atoi(argv[4]);

  // The settings of test instances F1-F9
  // char *ins[] = {"F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"}
  int pof[]      = {  21,   21,   21,   21,   21,   31,   21,   21,  22};       // type of pareto front
  int pos[]      = {  21,   22,   23,   24,   26,   32,   21,   21,  22};       // type of pareto set
  int dis[]      = {   1,    1,    1,    1,    1,    1,    3,    4,   1};       // type of non-negative function
  int var[]      = {  30,   30,   30,   30,   30,   10,   10,   10,  30};       // dimensionality of search space
  int obj[]      = {   2,    2,    2,    2,    2,    3,    2,    2,   2};       // number of objective functions

  // The settings of algorithms
  int pop[] = {300, 300, 300, 300, 300, 595, 300, 300, 300};     // population size
  int gen[] = {500, 500, 500, 500, 500, 500, 500, 500, 500};     // number of generations

  // the parameter setting of test instance
  dtype = dis[instance];
  ptype = pof[instance];
  ltype = pos[instance];
  nvar  = var[instance];
  nobj  = obj[instance];

  // the parameter setting of MOEA/D-DE and
  pops    = pop[instance];
  max_gen = gen[instance];

  sprintf(strTestInstance,"P%dD%dL%d",ptype, dtype, ltype);
  printf("Instances: pf shape %d  - distance %d, - ps shape %d \n ", ptype, dtype, ltype);

  if (exe_or_reassess) {
    if (use_moead)
      execute("DMOEA");
    else
      execute("NSGA-II");
  } else {
    if (use_moead)
      reassess("DMOEA");
    else
      reassess("NSGA-II");
  }
}

void execute(char *alg) {
  std::fstream fout;
  char filename[1024];
  // compute IGD-values
  if (strcmp(alg,"DMOEA")==0)
    sprintf(filename,"GD/GD_DMOEA_%s.dat",strTestInstance);
  else
    sprintf(filename,"GD/GD_NSGA2_%s.dat",strTestInstance);

  fout.open(filename,std::ios::out);

  for (int run=1; run<=max_run; run++) {
      vector<double> gd;
      if (strcmp(alg,"DMOEA")==0) {
          CMOEAD  MOEAD;
          gd = MOEAD.execute(run, "_TCHE1", "_DE");
      } else {
        CNSGA2  NSGA2;
        gd = NSGA2.execute(run);
      }
      for (int k=0; k<gd.size(); k++)
        fout<<gd[k]<<" ";
      fout<<"\n";
      gd.clear();
    }
  fout.close();
}

void reassess(char *alg) {
  char filename[1024];
  vector <CMOEADInd>  ps, pf;
  double distance = 0;
  int run = 1;

  sprintf(filename, "PF/pf_%s.dat", strTestInstance);
  loadpfront(filename, ps);

  if (strcmp(alg, "DMOEA")==0)
    sprintf(filename, "POF/PF_DMOEA_%s_R%d_G%d.dat", strTestInstance, run, max_gen);
  else
    sprintf(filename, "POF/PF_NSGA2_%s_R%d_G%d.dat", strTestInstance, run, max_gen);
  loadpfront(filename, pf);

  for (int i=0; i<ps.size(); i++) {
    double min_d = 1.0e+10;
    for (int j=0; j<pf.size(); j++) {
      double d = dist_vector(ps[i].y_obj, pf[j].y_obj);
      if (d<min_d)
        min_d = d;
    }
    distance += min_d;
  }
  distance /= ps.size();
  std::cout << "Final reassess: " << distance << std::endl;
}
