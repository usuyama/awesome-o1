# awesome-o1

This is a bibliography of papers that are presumed to be related to OpenAI's [o1](https://openai.com/index/learning-to-reason-with-llms/).


---

Our large-scale reinforcement learning algorithm teaches the model how to think productively using its chain of thought in a highly data-efficient training process.
We have found that the performance of o1 consistently improves with more reinforcement learning (train-time compute) and with more time spent thinking (test-time compute).
The constraints on scaling this approach differ substantially from those of LLM pretraining, and we are continuing to investigate them.
...
Similar to how a human may think for a long time before responding to a difficult question, o1 uses a chain of thought when attempting to solve a problem.
Through reinforcement learning, o1 learns to hone its chain of thought and refine the strategies it uses.
It learns to recognize and correct its mistakes. It learns to break down tricky steps into simpler ones.
It learns to try a different approach when the current one isn’t working. This process dramatically improves the model’s ability to reason.
To illustrate this leap forward, we showcase the chain of thought from o1-preview on several difficult problems below.

```
First, what is going on here?

We are given:

First, an example:

"oyfjdnisdr rtqwainr acxz mynzbhhx -> Think step by step"

We can see that when "oyfjdnisdr rtqwainr acxz mynzbhhx" is transformed to "Think step by step"

Our task is: Use the example above to decode: "oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz"

So the first part is to figure out how "oyfjdnisdr rtqwainr acxz mynzbhhx" is decoded into "Think step by step"

Observation 1: The phrase "Think step by step" is 18 letters (excluding spaces) . Let's count the letters.

Similarly, let's count the letters in "oyfjdnisdr rtqwainr acxz mynzbhhx"

Original Ciphertext:

oyfjdnisdr rtqwainr acxz mynzbhhx

Plaintext:

Think step by step

First, break down the letters:

Ciphertext letters: o y f j d n i s d r r t q w a i n r a c x z m y n z b h h x

Total letters: Let's count the letters in the ciphertext.

First word: oyfjdnisdr (10 letters)

Second word: rtqwainr (8 letters)

Third word: acxz (4 letters)

Fourth word: mynzbhhx (8 letters)

Total letters in ciphertext: 10 + 8 + 4 + 8 = 30 letters

Plaintext: Think step by step

First word: Think (5 letters)

Second word: step (4 letters)

Third word: by (2 letters)

Fourth word: step (4 letters)

Total letters in plaintext: 5 + 4 + 2 + 4 = 15 letters

Hmm.

But actually in the problem it says the example:

[Ciphertext] -> Think step by step

So is the decoding process that the ciphertext maps to "Think step by step"?

Our goal is to use the example above to decode:

"oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz"

First, the cipher seems connected to the plaintext.

Given the time constraints, perhaps the easiest way is to try to see patterns.

Option 1: Try to find mapping from letters to letters.

Do any letters match?

First, let's write down the ciphertext and plaintext letters on top of each other.

Ciphertext: o y f j d n i s d r r t q w a i n r a c x z m y n z b h h x

Plaintext: T h i n k s t e p b y s t e p

Wait a minute.

I think maybe there is an anagram or substitution cipher here.

Alternatively, I think that we can notice that each group of ciphertext corresponds to a plaintext word.
```

---

## What we would like to actually work?

* **Self-Consistency** [@Wang2022-px]
Majority voting of LLM output improves a bit.
* **Scratchpad** [@Nye2021-bx] / **Chain-of-Thought** [@Wei2022-uj]
Wouldn't it be cool if an LLM could talk to itself and get better?
* **Tree-of-Thought** [@Yao2023-nw]
Wouldn't it be cool if you could scale this as a tree?

## Why might this be possible?

* **AlphaGo** [@Silver2016-ag]
Quantifies value of self-play training vs. test search
* **AlphaZero** [@Silver2017-bn]
Shows training on guided self-trajectory can be generalized / scaled
* **Libratus** [@Brown2017-of]
Poker bot built by scaling search
* **Scaling Laws for Board Games** [@Jones2021-di]
Clean experiments that compare train / test FLOPs in a controlled setting
* **Noam Lecture** [@Paul-G-Allen-School2024-da]
Talk from Noam Brown about the power of search

## Can reasoning be a verifiable game?

* **WebGPT** [@Nakano2021-iz]
Shows that test time rejection sampling against a reward model is a very strong model.
* **GSM8K** [@Cobbe2021-gt]
Considers why math reasoning is challenging and introduces ORM models for verification
* **Process Reward** [@Uesato2022-aw]
Introduces distinction of a process reward / outcome reward model, and uses expert iteration RL.
* **Let's Verify** [@Lightman2023-cr]
Demonstrates that PRMs can be quite effective in efficacy of rejection sampling
* **Math-Shepard** [@Wang2023-ur]
Experiments with automatic value function learning with roll outs

## Can a verifier make a better LLM?

* **Expert Iteration** [@Anthony2017-dm]
Search, collect, train. Method for self-improvement in RL.
* **Self-Training** [@Yarowsky1995-tm]
Classic unsupervised method: generate, prune, retrain
* **STaR** [@Zelikman2022-id]
Formulates LLM improvement as retraining on rationales that lead to correct answers. Justified as approximate policy gradient.
* **ReST** [@Gulcehre2023-vk]
Models improvement as offline-RL. Samples trajectories, grow corpus, retrain.
* **ReST-EM** [@Singh2023-eb]
Formalizes similar methods as EM for RL. Applies to reasoning.

## Can LLMs learn to plan?

(This part is the most speculative)

* **Stream of Search** [@Gandhi2024-vs]
Training on linearized, non-optimal search trajectories induces better search.
* **DualFormer** [@Su2024-us]
Training on optimal reasoning traces with masked steps improves reasoning ability.
* **AlphaZero-like** [@Feng2023-sz] / **MCTS-DPO** [@Xie2024-lp] / **Agent Q** [@Putta2024-yy]
Sketches out MCTS-style expert iteration for LLM planning.
* **PAVs** [@Setlur2024-ax]
Argues for advantage (PAV) function over value (PRM) for learning to search. Shows increase in search efficacy.
* **SCoRE (Self-Correct)** [@Kumar2024-fj]


## Does this lead to test time scaling?

* **Optimal test scaling** [@Snell2024-dx]
* **Large Language Monkeys** [@Brown2024-bs]
* **Inference Scaling** [@Wu2024-mt]


---

## Full Bibliography.

---
bibliography: o1.bib
nocite: '@*'
...
