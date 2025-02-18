*******************************************************************
*                                                                 *
*               ML-shift - A toy x-ray project                    *
*                                                                 *
*******************************************************************

TDDFT functionals (especially GGA and standard hybrids) are woefully inaccurate when it comes to prediciting correct x-ray spectra. Often requiring large shifts to match with experimental results.
This model has been trained to predict shifts for a set of functionals, essentially as an automated correction to give high quality results at 
TDDT costs. 
The functionals suited for the mode are- PBE, PBE0, BLYP,SCAN, N3LYP, CAM-B3LYP, TPSS, rSCAN, SCAN0, wB97, BHHLYP, LDA and plain old Hartree-Fock.
The training was done using a simple Neural network (which might be overkill for this problem, but this a toy project aimed mostly at teaching myself how these work).
The file Xray_model.pth contains the model, testNN.py runs it.
