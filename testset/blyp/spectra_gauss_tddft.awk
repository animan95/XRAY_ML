#!/usr/bin/awk -f
# get excitation energies from LR-TDDFT and turn into a
# gaussian-broadened spectrum
#
# Usage:
#   ./spect-gauss.awk -v width=XX -v npts=NN qchem.out
# where XX is Gaussian width (in eV) and NN is number of intervals
#
BEGIN{
 N=0
 if(width == 0.0) width=0.6 # in eV
 if(npts == 0) npts=100000
}

#{
# some commands
# N++
# str[N] = $1
# exc[N] = $2 # in eV 
#}

/Excited state/{
  N++
  exc[N] = $8
}

/Strength   :/{
  str[N] = $3
}

END{
 eMin = exc[1] - 5.0
 eMax = exc[N] + 5.0
 de = (eMax-eMin)/npts
 printf("# Gauss width = %.2f eV\n",width)
 printf("# Delta E = %.4f eV\n",de)
 e = eMin
 for (i=1; i <= npts; i++)
 {
   intens=0.0
   for (j=1; j <= N; j++)
   {
     intens += str[j]*Gauss(e,exc[j],width)   
   }
   printf("%10.4f %12.6f\n",e,intens)
   e += de
 }
}

function Gauss(x,x0,sigma)
{
  arg = 0.5*(x-x0)*(x-x0)/(sigma*sigma)
  if (arg > 30.0)
     g = 0.0
  else
     g = exp(-arg)
  #denom = sigma*2.506628274631001   # sigma*sqrt(2pi)
  #return g/denom
  return g
}
