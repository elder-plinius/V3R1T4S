#!/bin/bash
# usage: launch.sh JOBDIR THREADS TIMEOUT_S TRAIN VALID SEED EPOCHS CHANNELS RMAX [extra mace args]
JD=$1; TH=$2; TO=$3; TR=$4; VA=$5; SEED=$6; EP=$7; CH=$8; RM=$9; shift 9
mkdir -p $JD
export OMP_NUM_THREADS=$TH MKL_NUM_THREADS=$TH
nohup nice -n 10 timeout $TO venv/Scripts/mace_run_train.exe --name=m --work_dir=$JD --train_file=$TR --valid_file=$VA --E0s=average --model=MACE \
 --hidden_irreps="${CH}x0e+${CH}x1o" --r_max=$RM --num_interactions=2 --max_ell=2 --correlation=3 --batch_size=${BS:-10} --lr=${LR:-0.01} --ema --ema_decay=0.99 \
 --max_num_epochs=$EP --eval_interval=2 --forces_weight=100 --energy_weight=1 --loss=weighted --scaling=rms_forces_scaling --scheduler_patience=8 --lr_factor=0.5 \
 --energy_key=REF_energy --forces_key=REF_forces --device=cpu --default_dtype=float32 --seed=$SEED --save_cpu --restart_latest "$@" > $JD/job.log 2>&1 < /dev/null &
echo $! > $JD/pid.txt; disown
nohup src/hb.sh $JD > /dev/null 2>&1 & disown
