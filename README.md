# Phun-Bench: Evaluating LLMs on Phonological Understanding in Chinese

<a href="https://arxiv.org/abs/2606.07300" target="_blank">
    <img src="https://img.shields.io/badge/arXiv-b31b1b.svg?style=for-the-badge&logo=arXiv&logoColor=white"
         alt="arXiv" />
</a>

**Phun-Bench** evaluates phonological understanding in Chinese, across three dimensions: homophony, rhyme, and phonetic similarity.

This repository contains the Phun-Bench datasets and evaluation code.

<p align="center">
  <img src="paper/image/data_sample.png" width="900" alt="Examples of the three Phun-Bench dimensions">
</p>

## News

- [2026/06/13]🎁 The datasets and evaluation code are released.
- [2026/06/05]🍓 The [paper](https://arxiv.org/abs/2606.07300) is available on arXiv.
- [2026/04/20]⭐ The repository is created.

## Installation

Python 3.10 or later is recommended. Install the evaluation dependencies with:

```zsh
pip install -r requirements.txt
```

The `dashscope` and `requests` packages are only used by the audio experiment.

## Running Evaluations

Edit the defaults in the corresponding
file under `scripts/`, or override them when invoking it:

```zsh
LLM_BASE_URL="https://api.example.com/v1" \
LLM_API_KEY="your-api-key" \
LLM_MODEL_NAME="your-model-name" \
EVAL_SUBSET_NUM=10 \
./scripts/run_homo2idiom.sh
```

The launchers also expose generation settings such as `LLM_TEMPERATURE`,
`LLM_TOP_P`, `LLM_MAX_TOKENS`, `LLM_ENABLE_THINKING`, and
`LLM_CONCURRENCY`. Set `EVAL_SUBSET_NUM` to limit the number of examples from
each dataset. Evaluation outputs are written under `results/`.

## Datasets

### Verification Experiment

**Character-to-Pinyin Conversion**

```zsh
./scripts/run_char2py.sh
```

Data: `dataset/char_tier_1.json`, `dataset/char_tier_2.json`, and
`dataset/char_tier_3.json`.

### Dimension 1: Homophony-Based Understanding

**Homophonic Idiom Recall**

```zsh
./scripts/run_homo2idiom.sh
```

Data: `dataset/idioms_homo_4_perturbed.json`.

**Contextual Homophone Recognition**

This task evaluates pun detection and recognition.

```zsh
./scripts/run_pun.sh
```

Data: `dataset/puns_filter_homo_public.json`.

### Dimension 2: Rhyme-Based Understanding

**Rhymed Sentence Generation**

This launcher evaluates single-rhyme and double-rhyme generation.

```zsh
./scripts/run_rhyming.sh
```

Data: `dataset/rhyme_gen_public.json`.

### Dimension 3: Phonetic-Similarity-Based Understanding

**Similarity Comparison**

```zsh
# Word form
./scripts/run_sim_word4word.sh

# Pinyin form
./scripts/run_sim_py4py.sh
```

Data: `dataset/sim_word_pert1.json` through
`dataset/sim_word_pert4.json`.

## RQ1 Experiments

**Idiom decomposition tasks**

```zsh
# Homophonic idiom to Pinyin
./scripts/run_homo2py.sh

# Pinyin to idiom
./scripts/run_py2idiom.sh

# Homophonic idiom to idiom
./scripts/run_homo2idiom.sh
```

Data: `dataset/idioms_homo_4_perturbed.json`.

**Pun decomposition tasks**

```zsh
# Pun phrase to Pinyin
./scripts/run_phrase2py.sh

# Pinyin to alternative phrase
./scripts/run_py2phrase.sh

# Contextual pun recognition
./scripts/run_pun.sh
```

Data: `dataset/puns_filter_homo_public.json`.

**Character decomposition tasks**

```zsh
# Character to Pinyin
./scripts/run_char2py.sh

# Pinyin to homophonic characters
./scripts/run_py2chars.sh

# Character to homophonic characters
./scripts/run_char2chars.sh
```

Data: `dataset/char_tier_*.json` and `dataset/char_group_5_plus.json`.

## Audio Model Experiments

```zsh
./scripts/run_audio_sim_word4word.sh
```

This launcher also uses `TTS_API_KEY`, `TTS_MODEL_NAME`, and `TTS_VOICE` for
speech synthesis. The evaluated model endpoint is configured through the same
`LLM_*` variables used by the text experiments.

Data: `dataset/sim_word_pert1.json` through
`dataset/sim_word_pert4.json`.

## Legacy Experiment

**Quasi-Homophone Recall**

This task was originally part of Dimension 3. It perturbs idioms and asks the
model to recover them. We later excluded it because low human performance
suggested that it was not a reliable test of phonological understanding.

```zsh
./scripts/run_sim_pert2idiom.sh
```

Data: `dataset/idioms_base_*_perturbed.json` and
`dataset/idioms_tone_*_perturbed.json`.

## Citation

If you use Phun-Bench, please cite:

```bibtex
@article{yue2026phunbench,
  title   = {Phun-Bench: Evaluating LLMs on Phonological Understanding in Chinese},
  author  = {Yue, Xing and Shen, Yongliang and Lu, Weiming},
  journal = {arXiv preprint arXiv:2606.07300},
  year    = {2026}
}
```

## Publishing

Maintainers can stage the public release files, run safety checks, commit, and
push the current branch with:

```sh
./scripts/push_to_github.sh "Release Phun-Bench"
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
