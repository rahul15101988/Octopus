#!/bin/bash

#ulimit -n 102400

sippIP='10.206.151.26'
dmaSutIP='10.206.151.56'

runTimeHr=72
runTimeMin=0
runTimeSec=0

########################################
#scenario='scen-uac.xml'
#scenario='scen-reguac.xml'
scenario='scen-reguac-audioonly.xml'

# ########################################
# # vmr sip endurance - nominal for 1*rmx1800d(3)
# #                   - these are the values that I used for H.323 calls
# #                   
# #
# #     1.875 cps              (~1.875 obs on sipp)
# #       160 ccvmr            (~173 obs on DMA)
# #        20 conc conf        (~33 obs on DMA)
# #         8 part / conf
# #
# rate=1875
# holdTimeMil=85333
# ratePeriodMil=1000000
# injectionFile="8partconf.inf"
# runTimeHr=8
# runTimeMin=10
# runTimeSec=0
########################################
# vmr sip endurance - nominal for 1*rmx4000-4mpmxd
#
#     1.875 cps              (~1.875 obs on sipp)
#       160 ccvmr            (~173 obs on DMA)
#        20 conc conf        (~33 obs on DMA)
#         8 part / conf
#
rate=5000/2000 (5cps/2cps) milliseconds
holdTimeMil=70000 

# in case of ninja 150, 2k 300 4k 600 ccvmrs for 2 cps
# in case of ninja 
# hold time  = ccvmr/(rate in seconds) and then convert to milliseconds

ratePeriodMil=1000000
injectionFile="20partconfaudio.inf"
runTimeHr=72
runTimeMin=0
runTimeSec=0
########################################
# # forharmon - callrate
# #
# ##    2.500 cps              (
# #     1.875 cps              (~1.875 obs on sipp)
# #       160 ccvmr            (~173 obs on DMA)
# #        20 conc conf        (~33 obs on DMA)
# #         8 part / conf
# #
# ##rate=2500
# ##holdTimeMil=64000
# rate=1875
# holdTimeMil=85333
# ratePeriodMil=1000000
# injectionFile="8partconf.inf"
# #####
# # forharmon - callcapacity
# #
# #     1.000 cps              (
# #       200 ccvmr            (~188 obs on DMA)
# ##      175 ccvmr            (~179 obs on DMA)
# #        20 conc conf        (~33 obs on DMA)
# #         8 part / conf
# #
# rate=1000
# ##holdTimeMil=200000
# holdTimeMil=175000
# ratePeriodMil=1000000
# injectionFile="8partconf.inf"
#####
# # forharmon - confrate
# #
# #     1.000 cps              (
# ##      160 ccvmr            (~    obs on DMA)
# ##      160 conc conf        (~    obs on DMA)
# ###     DMA "design issue" reduced to ~55/200 conferences
# ##       60 ccvmr            (~ 60 obs on DMA)
# ##       60 conc conf        (~100 obs on DMA)
# #        40 ccvmr            (~ 40 obs on DMA)
# #        40 conc conf        (~ 88 obs on DMA)
# #         1 part / conf
# #
# #rate=1000
# rate=1200
# ##holdTimeMil=160000
# #holdTimeMil=60000
# #holdTimeMil=40000
# holdTimeMil=28000
# ratePeriodMil=1000000
# injectionFile="1partconf.inf"
# #####
# # forharmon - confcapacity
#
#     0.800 cps              (
#       200 ccvmr            (~173 obs on DMA)
#       200 conc conf        (~33 obs on DMA)
### DMA "design issue" reduced to ~55/200 conferences
# ##       60 ccvmr            (~ 60 obs on DMA)
# ##       60 conc conf        (~100 obs on DMA)
# #        40 ccvmr            (~ 40 obs on DMA)
# #        40 conc conf        (~ 80 obs on DMA)
# #         1 part / conf
# #
# rate=800
# ##holdTimeMil=250000
# #holdTimeMil=75000
# holdTimeMil=50000
# ratePeriodMil=1000000
# injectionFile="1partconf.inf"
# #####

########################################
########################################
#   audio only    audio only   audio only
########################################
########################################
#injectionFile="8partconfaudio.inf"
#injectionFile="tp.inf"
# injectionFile="20partconfaudio.inf"
# scenario='scen-reguac-audioonly.xml'

# runTimeHr=0
# runTimeMin=30
# runTimeSec=0
# ########################################
# # callrate
# #
# ##    10.000 cps
# #     5.000 cps
# ##     2.500 cps
# ##     1.875 cps              (~1.875 obs on sipp)
# #       160 ccvmr            (~173 obs on DMA)
# #        20 conc conf        (~33 obs on DMA)
# #         8 part / conf
# #
# rate=10000
# holdTimeMil=16000
# #rate=5000
# #holdTimeMil=32000
# #rate=2500
# #holdTimeMil=64000
# #rate=1875
# #holdTimeMil=85333
# ratePeriodMil=1000000
# #####

########################################
########################################
now=`date +%F_%M-%S`
statFile=sipp-statistics_${now}.csv

runTime="`echo "${runTimeHr} * 3600  + ${runTimeMin} * 60 + ${runTimeSec}" | bc`s"

#/opt/SIPp/sipp                          \
/usr/local/bin/sipp                     \
    -i ${sippIP}  -p 5060               \
    ${dmaSutIP}                         \
        -sf    ${scenario}              \
        -inf   ${injectionFile}         \
        -t u1  -max_socket 15000        \
    -r ${rate} -rp ${ratePeriodMil}     \
    -d ${holdTimeMil}			\
    -timeout ${runTime}                 \
        -aa                             \
        -stf   ${statFile}  -fd 5       \
        -trace_err -trace_screen -trace_shortmsg -trace_stat -trace_rtt -trace_msg 

########################################
# extra notes:
#
# totalSAPS= 5
#
#        -m ${totalSAPS}                 \
#        -inf sipp-info.dat  -ip_field 2 \
#        -t un  -max_socket 1000         \
########################################
