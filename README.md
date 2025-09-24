# MiniOpt: Reasoning to Model and Solve General Optimization Problems with Limited Resources

MiniOpt is an end-to-end optimization solving paradigm based on reinforcement learning with verifiable reward (RLVR). It enables small language models (1.5B-14B parameters) to achieve state-of-the-art performance in solving optimization problems from natural language descriptions, significantly reducing computational costs while maintaining competitive accuracy.

## 📊 Performance

MiniOpt achieves remarkable performance across 9 optimization benchmarks.

<table border="0" style="border-collapse: collapse; text-align: center;">
  <thead>
    <tr>
      <th rowspan="2">Category</th>
      <th rowspan="2">Model / Method</th>
      <th colspan="2">Performance</th>
    </tr>
    <tr>
      <th>SA Avg.</th>
      <th>ER Avg.</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4" style="vertical-align: middle;"><strong>General Models</strong></td>
      <td>Qwen2.5-3B-Instruct</td>
      <td>9.98</td>
      <td>17.11</td>
    </tr>
    <tr>
      <td>Qwen2.5-7B-Instruct</td>
      <td>30.05</td>
      <td>41.69</td>
    </tr>
    <tr>
      <td>Qwen2.5-14B-Instruct</td>
      <td>43.59</td>
      <td>63.53</td>
    </tr>
    <tr>
      <td>DeepSeek V3</td>
      <td>57.81</td>
      <td>83.50</td>
    </tr>
    <tr>
      <td rowspan="6" style="vertical-align: middle;"><strong>General Models (Thinking)</strong></td>
      <td>Qwen3-4B</td>
      <td>10.25</td>
      <td>14.15</td>
    </tr>
    <tr>
      <td>Qwen3-8B</td>
      <td>19.77</td>
      <td>25.55</td>
    </tr>
    <tr>
      <td>Qwen3-14B</td>
      <td>22.54</td>
      <td>31.17</td>
    </tr>
    <tr>
      <td>DeepSeek R1</td>
      <td>58.51</td>
      <td>83.07</td>
    </tr>
    <tr>
      <td>Gemini 2.5 Pro</td>
      <td>57.04</td>
      <td>89.65</td>
    </tr>
    <tr>
      <td>GPT-5</td>
      <td>56.57</td>
      <td>83.26</td>
    </tr>
    <tr>
      <td rowspan="3" style="vertical-align: middle;"><strong>Prompt-based Methods</strong></td>
      <td>Chain-of-Experts</td>
      <td>41.03</td>
      <td>61.72</td>
    </tr>
    <tr>
      <td>OptiMUS</td>
      <td>18.76</td>
      <td>52.13</td>
    </tr>
    <tr>
      <td>Reflexion</td>
      <td>41.28</td>
      <td>80.42</td>
    </tr>
    <tr>
      <td rowspan="2" style="vertical-align: middle;"><strong>Learning-based Models</strong></td>
      <td>OptMATH-7B</td>
      <td>52.37</td>
      <td>85.07</td>
    </tr>
    <tr>
      <td>LLMOPT-14B</td>
      <td>54.81</td>
      <td>90.03</td>
    </tr>
    <tr>
      <td rowspan="3" style="vertical-align: middle;"><strong>Ours</strong></td>
      <td>MiniOpt-3B</td>
      <td>56.94</td>
      <td>88.04</td>
    </tr>
    <tr>
      <td>MiniOpt-7B</td>
      <td>62.76</td>
      <td>90.61</td>
    </tr>
    <tr>
      <td>MiniOpt-14B</td>
      <td><strong>66.10</strong></td>
      <td><strong>92.35</strong></td>
    </tr>
  </tbody>
</table>

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

