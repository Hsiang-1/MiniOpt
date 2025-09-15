# MiniOpt: Reasoning to Model and Solve General Optimization Problems with Limited Resources

MiniOpt is an end-to-end optimization solving paradigm based on reinforcement learning with verifiable reward (RLVR). It enables small language models (1.5B-14B parameters) to achieve state-of-the-art performance in solving optimization problems from natural language descriptions, significantly reducing computational costs while maintaining competitive accuracy.

## 📊 Performance Highlights

MiniOpt achieves remarkable performance across 9 optimization benchmarks:

| Model       | Average SA | Average ER | Parameters |
| ----------- | ---------- | ---------- | ---------- |
| MiniOpt-14B | **66.24%** | **92.04%** | 14B        |
| MiniOpt-7B  | 62.90%     | 90.64%     | 7B         |
| MiniOpt-3B  | 56.94%     | 88.78%     | 3B         |
| LLMOPT-14B  | 54.81%     | 90.03%     | 14B        |
| GPT-5       | 56.57%     | 83.26%     | ~1.8T      |



## 🛠️ Installation

### Prerequisites

* Python 3.10+

* Conda package manager

### Setup

```bash
# Clone the repository
# git clone https://github.com/xxxxx/MiniOpt.git
# cd MiniOpt

# Create a conda environment
conda create -n MiniOpt python=3.10 -y
conda activate MiniOpt

# Install the required packages
bash init.sh
```

## 🔍 File System

```bash
.
├── init.sh
├── README.md
├── datasets
│   ├── rl_dataset
│   │   └── example.parquet
│   └── sft_dataset
│       └── example.jsonl
├── inference
│   └── inference.py
├── prompts
│   ├── code_conversion.py
│   ├── question_scenario_labeling.py
│   ├── question_type_labeling.py
│   └── rl_prompt.py
├── rl
│   ├── configs
│   │   ├── rl_example.sh
│   │   ├── rl_phase1.sh
│   │   └── rl_phase2.sh
│   ├── opt_reward.py
│   ├── pyomo_executor.py
│   └── rl.sh
└── sft
    ├── configs
    │   ├── merge_config.yaml
    │   └── sft_config.yaml
    ├── data
    │   └── dataset_info.json
    └── sft.sh
```

- `datasets`: Examples of SFT/RL training dataset. 
- `inference`: Example of using the fine-tuned model to infer an optimization problem.
- `prompts`: All the prompts used and mentioned in our paper.
- `rl`: This folder includes the `opt_reward` and the execution method of pyomo code. The `configs` folder includes the 2-stage rl training configuration files and a configuration example. `rl.sh` shows how to use these scripts.
- `sft`: This folder provides the code for SFT based on LLaMAFacroty, including dataset configuration (`./sft/data/dataset_info.json`), fine-tuning script (`./sft/configs/sft_config.yaml`), and post-training model merge script (`./sft/configs/merge_config.yaml`). `sft.sh` shows how to use these scripts.
- `init.sh` shows the setup of the environment. 

## 🚦 Usage

### SFT Warm-up

1. Prepare the sft training dataset. Here is an example of SFT training dataset format: `./datasets/sft_dataset/example.jsonl`.
2. Config the dataset. Here is an example of LLaMAFactory dataset configuration: `./sft/data/dataset_info.json`.
3. Run SFT and merge Lora model. The hyperparameter setting used for SFT warm-up in our paper is shown in `./sft/configs/sft_config.yaml`. 

```bash
cd sft
bash sft.sh
```

### RL Training

1. Prepare your RL training dataset and eval dataset. MiniOpt uses a 2-stage RL training approach, including `Paradigm Acquisition` (phase 1) and `Optimization Generalization` (phase 2). Although the training data used in the two stages are different, the format and attributes are the same. Here is an example of RL training dataset format: `./datasets/rl_dataset/example.jsonl`. 
2. Run RL training. The training parameters of the 2-stage RL are fully listed in `./rl/configs/rl_phase1.sh` and `./rl/configs/rl_phase2.sh`.

```bash
cd rl
bash rl.sh
```

### Inference

Run `python ./inference/inference.py` to perform inference. This script shows the system prompt used for inference and tests the first case of `nl4opt_test` benchmark.

