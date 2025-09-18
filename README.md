
# Multi-Agent Judge Bias

This repository contains the official code for the paper:

**Judging with Many Minds: Do More Perspectives Mean Less Prejudice? On Bias Amplification and Resistance in Multi-Agent Based LLM-as-Judge**

arXiv: [2505.19477](https://arxiv.org/abs/2505.19477)

## Overview

![Figure 1: Evaluated Multi-Agent Framework](assets/fig1_multiagent5.jpg)

This repo provides code to reproduce the experiments and analyses from our paper, which investigates the bias of large language model (LLM) judges in multi-agent debate and meta-judge settings (see Figure 1). In addition to experiment code, this repository provides the final output and conversation logs of the agents, which can be used for further analysis and future research.

## Bias Types Tested

We evaluate four main types of bias in LLM judges (see Figure 2):

- **Position Bias**: Preference for responses based on their order or position.
- **Chain-of-Thought (CoT) Bias**: Influence from longer reasoning steps or explanations.
- **Bandwagon Bias**: Tendency to favor majority or consensus opinions.
- **Verbosity Bias**: Favoring more detailed or longer responses.

Each bias type is simulated and analyzed to assess its impact on judgment robustness in multi-agent settings.

![Figure 2: Bias Types Illustration](assets/fig2_bias_final.jpg)

## Environment Setup

We recommend using `conda` to manage dependencies. All required packages are listed in `environment.yaml`.

```bash
conda env create -f environment.yaml
conda activate multi_agent_judge_bias
```

## Running Experiments

### 1. Debate Experiments

The main parameters for running debate experiments are:

- `--data_dir`: Path to the dataset.
- `--judge`: The model used as the judge for evaluating responses.
- `--critic`: The model used to provide critiques (can be the same as judge).
- `--result_save`: Output path for saving experiment results.
- `--device`: GPU device index for computation.
- `--n_round`: Number of debate rounds.
- `--batch_size`: Number of samples processed per batch.
- `--debug`: Enables debug mode for verbose logging.
- `--bias_type`: Type of bias to simulate (`none`, `position`, `cot`, `bandwagon`, or `verbose`).

Adjust these parameters to customize your experiment setup. Below is some example usage:

Run the original debate:

```bash
python run_exp.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
  --judge openai:gpt-4o-mini \
  --critic openai:gpt-4o-mini \
  --result_save results/result_debate_mtbench/gpt-4o-mini-none \
  --device 0 \
  --n_round 0 \
  --batch_size 4 \
  --debug True \
  --bias_type none \
```

Debate with position bias:

```bash
python run_exp.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
  --judge openai:gpt-4o-mini \
  --critic openai:gpt-4o-mini \
  --result_save results/result_debate_mtbench/gpt-4o-mini-position \
  --device 0 \
  --n_round 0 \
  --batch_size 4 \
  --debug True \
  --bias_type position \
```

Debate with verbosity bias:

```bash
python run_exp.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled_verbose.json \
  --judge openai:gpt-4o-mini \
  --critic openai:gpt-4o-mini \
  --result_save results/result_debate_mtbench/gpt-4o-mini-verbose \
  --device 0 \
  --n_round 0 \
  --batch_size 4 \
  --debug True \
  --bias_type verbose \
```

### 2. Meta-Judge Experiments

To run Meta-Judge Experiments, first complete the Debate experiments to generate the round 0 response files. The Meta-Judge scripts require these outputs as input for further evaluation. Ensure that the results from the Debate experiments (e.g., files in `results/result_debate_mtbench/gpt-4o-mini-none_round0.json`) are available before proceeding with Meta-Judge runs. The meta-judge will take these saved round 0 response as the candidates' initial output.

Original meta judge (conclude mode):

```bash
python run_exp_meta.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
  --judge openai:gpt-4o-mini \
  --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B \
  --judgements_dir results/result_debate_mtbench \
  --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-none \
  --device 0 \
  --batch_size 4 \
  --debug True \
  --judge_type conclude \
  --bias_type none \
```

Meta judge (choose mode) with position bias:

```bash
python run_exp_meta.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
  --judge openai:gpt-4o-mini \
  --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B \
  --judgements_dir results/result_debate_mtbench \
  --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-position \
  --device 0 \
  --batch_size 4 \
  --debug True \
  --judge_type choose \
  --bias_type position \
```

Meta judge (conclude mode) with verbosity bias:

```bash
python run_exp_meta.py \
  --data_dir data/mtbench_pairwise_data_normal_random_sampled_verbose.json \
  --judge openai:gpt-4o-mini \
  --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B \
  --judgements_dir results/result_debate_mtbench \
  --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-verbose \
  --device 0 \
  --batch_size 4 \
  --debug True \
  --judge_type conclude \
  --bias_type verbose \
```

You can also adjust the `--judgements_models` parameter to specify a list of models whose round 0 outputs will be used for meta-judging. Provide a comma-separated list of model names that correspond to the saved outputs in the results directory. This allows you to flexibly evaluate the impact of different candidate models and their combinations in the meta-judge setting.

## Analysis

After running experiments, use the scripts in the `analysis/` folder to analyze results. Example:

```bash
python run_analysis.py --result_dir results/result_debate_mtbench/gpt-4o-mini-none
```

You can modify the arguments to analyze different result folders or bias types.

## Checking Results

Results are saved in the `results/` directory, organized by experiment type and bias. You can inspect the JSON files directly or use the analysis scripts for summary statistics and plots. Detailed conversation logs are also provided in the `logs/` directory. These logs include the full agent interactions for each experiment, allowing for in-depth inspection and further analysis of model behavior and decision processes.


## Citation

```
@article{ma2025judgingmindsperspectivesmean,
      title={Judging with Many Minds: Do More Perspectives Mean Less Prejudice? On Bias Amplifications and Resistance in Multi-Agent Based LLM-as-Judge}, 
      author={Chiyu Ma and Enpei Zhang and Yilun Zhao and Wenjun Liu and Yaning Jia and Peijun Qing and Lin Shi and Arman Cohan and Yujun Yan and Soroush Vosoughi},
      year={2025},
      eprint={2505.19477},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.19477}, 
}
```