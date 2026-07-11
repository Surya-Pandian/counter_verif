onerror {quit -code 1}

add wave -r sim:/counter_tb/*
add wave -r sim:/counter_tb/dut/*

run -all

quit -code 0
