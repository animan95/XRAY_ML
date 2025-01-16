awk '{printf "%.4f\t%.6f\n", $1 + 12.1575, $2}' ammonia_plot.txt > ammonia_plot_shift.txt

awk '{printf "%.4f\t%.6f\n", $1 + 15.3916, $2}' h2o_plot.txt > h2o_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 9.3838, $2}' hcn_plot.txt > hcn_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 6.8463, $2}' co2_plot.txt > co2_C_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 15.6546, $2}' chf3_plot.txt > chf3_F_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 63.8537, $2}' ch3cl_plot.txt > ch3cl_Cl_plot_shift.txt
