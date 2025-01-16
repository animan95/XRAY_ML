#awk '{printf "%.4f\t%.6f\n", $1 + 11.2549, $2}' ammonia_plot.txt > ammonia_plot_shift.txt

#awk '{printf "%.4f\t%.6f\n", $1 + 14.4656, $2}' h2o_plot.txt > h2o_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 10.3385, $2}' hcn_plot.txt > hcn_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 7.8210, $2}' co2_plot.txt > co2_C_plot_shift.txt
#awk '{printf "%.4f\t%.6f\n", $1 + 16.7482, $2}' chf3_plot.txt > chf3_F_plot_shift.txt
awk '{printf "%.4f\t%.6f\n", $1 + 63.5632, $2}' ch3cl_plot.txt > ch3cl_Cl_plot_shift.txt
