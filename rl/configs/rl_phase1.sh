OUTPUT_PATH="./ckpts/MiniOpt-rl-phase1"
PRETRAIN_MODEL="../models/MiniOpt-Warmup"
TRAIN_DATA="../datasets/rl_dataset/phase1/train.parquet"
VAL_DATA="../datasets/rl_dataset/phase1/test.parquet"
OPT_REWARD_PATH="./opt_reward.py"

max_prompt_length=8192
max_response_length=8192
max_token_len=16384

use_kl_in_reward=False
kl_coef=0.0
use_kl_loss=False
kl_loss_coef=0.0

clip_ratio_low=0.2
clip_ratio_high=0.28

loss_agg_mode="token-mean"

mkdir ./log

python -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    algorithm.use_kl_in_reward=$use_kl_in_reward \
    algorithm.kl_ctrl.kl_coef=$kl_coef \
    reward_model.reward_manager=batch \
    custom_reward_function.path=$OPT_REWARD_PATH \
    custom_reward_function.name=compute_score_batched \
    data.train_files=$TRAIN_DATA \
    data.val_files=$VAL_DATA \
    data.train_batch_size=512 \
    data.max_prompt_length=$max_prompt_length \
    data.max_response_length=$max_response_length \
    actor_rollout_ref.model.path=$PRETRAIN_MODEL \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.ppo_mini_batch_size=32 \
    actor_rollout_ref.actor.use_dynamic_bsz=True \
    actor_rollout_ref.actor.use_kl_loss=$use_kl_loss \
    actor_rollout_ref.actor.kl_loss_coef=$kl_loss_coef \
    actor_rollout_ref.actor.clip_ratio_low=$clip_ratio_low \
    actor_rollout_ref.actor.clip_ratio_high=$clip_ratio_high \
    actor_rollout_ref.actor.clip_ratio_c=10.0 \
    actor_rollout_ref.actor.loss_agg_mode=$loss_agg_mode \
    actor_rollout_ref.model.enable_gradient_checkpointing=True \
    actor_rollout_ref.actor.fsdp_config.param_offload=False \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.6 \
    actor_rollout_ref.rollout.temperature=1.0 \
    actor_rollout_ref.rollout.n=16 \
    actor_rollout_ref.ref.fsdp_config.param_offload=False \
    actor_rollout_ref.actor.ppo_max_token_len_per_gpu=$max_token_len \
    actor_rollout_ref.ref.log_prob_max_token_len_per_gpu=$max_token_len \
    actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=$max_token_len \
    actor_rollout_ref.rollout.enable_chunked_prefill=True \
    actor_rollout_ref.rollout.max_num_batched_tokens=$max_token_len \
    trainer.critic_warmup=0 \
    trainer.logger=['console','tensorboard'] \
    trainer.nnodes=2 \
    trainer.n_gpus_per_node=8 \
    trainer.save_freq=15 \
    trainer.test_freq=15 \
    trainer.default_local_dir=$OUTPUT_PATH \
    trainer.total_epochs=5  $@ > ./log/training_phase1.log 2> ./log/training_phase1.error.log;  


latest_step=$(cat $OUTPUT_PATH/latest_checkpointed_iteration.txt)
python -m verl.model_merger merge \
    --backend fsdp \
    --local_dir $OUTPUT_PATH/global_step_$latest_step/actor/ \
    --target_dir ../models/MiniOpt-rl-phase1