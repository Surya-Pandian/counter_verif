onerror {quit -code 1}

add wave -r sim:/counter_tb/dut/*

configure wave -timelineunits ms

run -all
