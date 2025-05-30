**Usage Examples:**

The command to run the original debate:

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
    --count_id 0
```



The command to run the debate under position bias:

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
    --count_id 0
```



The command to run the debate under verbosity bias:

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
    --bias_type None \  # No change in prompt template
    --count_id 0
```



The command to run the original meta judge (conclude mode):

```bash
  python run_exp_meta.py \
            --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
            --judge openai:gpt-4o-mini \
            --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B
            --judgements_dir results/result_debate_mtbench \
            --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-none \
            --device 0 \
            --batch_size 4 \
            --debug True \
            --judge_type conclude \
            --bias_type none \
            --count_id 0
```



The command to run the meta judge (select mode) with position bias:

```bash
  python run_exp_meta.py \
            --data_dir data/mtbench_pairwise_data_normal_random_sampled.json \
            --judge openai:gpt-4o-mini \
            --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B
            --judgements_dir results/result_debate_mtbench \
            --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-position \
            --device 0 \
            --batch_size 4 \
            --debug True \
            --judge_type choose \
            --bias_type position \
            --count_id 0
```



The command to run the meta judge (conclude mode) with verbosity bias:

```bash
  python run_exp_meta.py \
            --data_dir data/mtbench_pairwise_data_normal_random_sampled_verbose.json \
            --judge openai:gpt-4o-mini \
            --judgements_models deepseek-chat,DeepSeek-R1-Distill-Qwen-32B
            --judgements_dir results/result_debate_mtbench \
            --result_save results/result_meta_mtbench/gpt-4o-mini_deepseek-chat-conclude-verbose \
            --device 0 \
            --batch_size 4 \
            --debug True \
            --judge_type conclude \
            --bias_type verbose \
            --count_id 0
```