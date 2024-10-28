# awesome-o1

This is a bibliography of papers that are presumed to be related to OpenAI's [o1](https://openai.com/index/learning-to-reason-with-llms/).

---

## What we would like to actually work?

* Self-Consistency [@Wang2022-px] - Majority voting of LLM output improves a bit.
* Scratchpad [@Nye2021-bx]/ Chain-of-Thought [@Wei2022-uj] - Wouldn't it be cool if an LLM could talk to itself and get better?
* Tree-of-Thought [@Yao2023-nw] - Wouldn't it be cool if you could scale this as a tree?

## Why might this be possible?

* AlphaGo [@Silver2016-ag] - Quantifies value of self-play training vs. test search
* AlphaZero [@Silver2017-bn] - Shows training on guided self-trajectory can be generalized / scaled
* Libratus [@Brown2017-of] - Poker bot built by scaling search
* Scaling Laws for Board Games [@Jones2021-di] - Clean experiments that compare train / test FLOPs in a controlled setting
* Noam [@Paul-G-Allen-School2024-da] - Talk from Noam Brown about the power of search

## How do you turn reasoning into a verifiable game?

* WebGPT [@Nakano2021-iz] - Shows that test time rejection sampling against a reward model is a very strong model.
* GSM8K [@Cobbe2021-gt] - Considers why math reasoning is challenging and introduces ORM models for verification
* Process Reward [@Uesato2022-aw] - Introduces distinction of a process reward / outcome reward model, and use expert iteration RL.
* Let's Verify [@Lightman2023-cr] - Demonstrates that PRMs can be quite effective in efficacy of rejection sampling
* Math-Shepard [@Wang2023-ur] - Experiments with automatic value function learning with roll outs

## How do you turn a verifier into a better LLM?

* Expert Iteration [@Anthony2017-dm] - Search, collect, train. Method for self-improvement in RL.
* Self-Training [@Yarowsky1995-tm] - Classic unsupervised method: generate, prune, retrain
* STaR [@Zelikman2022-id] - Formulates LLM improvement as retraining on rationales that lead to correct answers. Justified as approximate policy gradient.
* ReST [@Singh2023-eb] - Models improvement as offline-RL. Samples trajectories, grow corpus, retrain.
* ReST-EM [@Singh2023-eb] - Formalizes similar methods as EM for RL. Applies to reasoning.

## How can you get your model to play better (planning/search)?

* Stream of Search [@Gandhi2024-vs]
* AlphaZero-like [@Feng2023-sz]  - Plays out an MCTS style training algorithm for LLM planning

## How might this lead to test time scaling?

* Optimal test scaling [@Snell2024-dx] -




---

---
bibliography: o1.bib
nocite: '@*'
...
